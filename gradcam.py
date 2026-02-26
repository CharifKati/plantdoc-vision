"""
Grad-CAM heatmap generator for MobileNetV2 with Sequential wrapper
"""

import tensorflow as tf
import numpy as np
import cv2
import base64


def generate_gradcam(model, img_array, class_idx):
    """
    Generate Grad-CAM heatmap for MobileNetV2-based Sequential model.

    Args:
        model: Sequential Keras model
        img_array: Input image array (1, 224, 224, 3) normalized to [0, 1]
        class_idx: Index of the class to visualize

    Returns:
        overlay_base64: Heatmap overlaid on original image as base64 PNG
    """
    try:
        # Convert numpy array to TensorFlow variable (watchable)
        img_variable = tf.Variable(img_array, dtype=tf.float32, trainable=True)
        
        # Get the MobileNetV2 base model
        mobilenet_base = model.get_layer('mobilenetv2_1.00_224')
        last_conv_layer = mobilenet_base.get_layer('Conv_1')
        
        print(f"✓ Using MobileNetV2 layer: {last_conv_layer.name}")

        # Compute gradients
        with tf.GradientTape() as tape:
            # Forward pass through MobileNetV2 base
            conv_output = mobilenet_base(img_variable, training=False)
            
            # Forward pass through rest of model
            x = model.layers[1](conv_output)              # GlobalAveragePooling2D
            x = model.layers[2](x, training=False)        # BatchNormalization
            x = model.layers[3](x)                         # Dense
            x = model.layers[4](x, training=False)        # Dropout
            predictions = model.layers[5](x)              # Dense
            
            # Get loss for target class
            loss = predictions[:, class_idx]

        # Get gradients w.r.t conv_output
        grads = tape.gradient(loss, conv_output)
        
        if grads is None:
            print("⚠ Gradients are None, using activation visualization instead...")
            # Fallback: visualize activation maps
            conv_output_val = mobilenet_base(img_variable, training=False).numpy()
            heatmap = np.mean(np.abs(conv_output_val[0]), axis=-1)
        else:
            print(f"✓ Gradients computed successfully, shape: {grads.shape}")
            
            # Get conv outputs: shape (1, 7, 7, 1280)
            conv_output_val = conv_output[0].numpy()  # (7, 7, 1280)
            grads_val = grads[0].numpy()              # (7, 7, 1280)
            
            # Compute channel-wise gradient weights
            # Average gradients over spatial dimensions
            pooled_grads = np.mean(grads_val, axis=(0, 1))  # (1280,)
            
            print(f"  Conv output shape: {conv_output_val.shape}")
            print(f"  Grads shape: {grads_val.shape}")
            print(f"  Pooled grads shape: {pooled_grads.shape}")
            print(f"  Pooled grads min/max: {pooled_grads.min():.4f} / {pooled_grads.max():.4f}")
            
            # Use absolute values of gradients for importance weighting
            pooled_grads_abs = np.abs(pooled_grads)
            
            # Weight each channel by its gradient importance
            # Broadcasting: (7, 7, 1280) * (1280,) -> (7, 7, 1280)
            weighted_output = conv_output_val * pooled_grads_abs
            
            # Average across channels to get spatial heatmap
            heatmap = np.mean(weighted_output, axis=-1)
            
            print(f"  Heatmap shape: {heatmap.shape}")
            print(f"  Heatmap min/max before ReLU: {heatmap.min():.4f} / {heatmap.max():.4f}")
        
        # Apply ReLU and ensure positive values
        heatmap = np.maximum(heatmap, 0)
        
        print(f"  Heatmap min/max after ReLU: {heatmap.min():.4f} / {heatmap.max():.4f}")
        
        # Normalize to [0, 1]
        heatmap_max = np.max(heatmap)
        if heatmap_max > 1e-5:  # Check for very small values
            heatmap = heatmap / heatmap_max
            print(f"✓ Heatmap normalized")
        else:
            print("⚠ Heatmap is too small, using fallback activation map")
            conv_output_val = mobilenet_base(img_variable, training=False).numpy()
            heatmap = np.mean(np.abs(conv_output_val[0]), axis=-1)
            heatmap = heatmap / np.max(heatmap)

        # Convert image to uint8
        img_uint8 = np.array(img_array[0] * 255, dtype=np.uint8)

        # Resize heatmap to match image size (224, 224)
        heatmap_resized = cv2.resize(heatmap, (img_uint8.shape[1], img_uint8.shape[0]))

        # Apply colormap (JET: blue→green→red)
        heatmap_colored = cv2.applyColorMap(
            np.uint8(255 * heatmap_resized),
            cv2.COLORMAP_JET
        )

        # Blend original + heatmap (70% original, 30% heatmap)
        overlay = cv2.addWeighted(img_uint8, 0.7, heatmap_colored, 0.3, 0)

        # Encode as base64 PNG
        _, buffer = cv2.imencode('.png', overlay)
        overlay_base64 = base64.b64encode(buffer).decode()

        print(f"✓ Grad-CAM generated successfully")
        return overlay_base64

    except Exception as e:
        print(f"✗ Grad-CAM generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
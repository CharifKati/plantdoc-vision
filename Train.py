import os
import json
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# ── Config ────────────────────────────────────────────────────────────────────
DATASET_PATH = "merged_dataset_aug"  
MODEL_SAVE_PATH  = "plantdoc_model_base.pth"
CLASS_NAMES_PATH = "class_names.json"

IMG_SIZE   = 224
BATCH_SIZE = 32
EPOCHS     = 15
LR         = 1e-3  # higher LR for training from scratch

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# ── Dataset ───────────────────────────────────────────────────────────────────
transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
    transforms.RandomGrayscale(p=0.05),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

val_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225]),
])

full_dataset = datasets.ImageFolder(DATASET_PATH)
class_names  = full_dataset.classes
print(f"Found {len(class_names)} classes, {len(full_dataset)} total images")

with open(CLASS_NAMES_PATH, "w") as f:
    json.dump(class_names, f, indent=2)
print(f"Class names saved to {CLASS_NAMES_PATH}")

val_size   = int(0.2 * len(full_dataset))
train_size = len(full_dataset) - val_size
train_ds, val_ds = torch.utils.data.random_split(
    full_dataset, [train_size, val_size],
    generator=torch.Generator().manual_seed(42)
)

train_ds.dataset.transform = transform
val_ds.dataset.transform   = val_transform

train_loader = DataLoader(train_ds, batch_size=64, shuffle=True,  num_workers=4, pin_memory=True, persistent_workers=True)
val_loader   = DataLoader(val_ds,   batch_size=64, shuffle=False, num_workers=4, pin_memory=True, persistent_workers=True)

# ── Model — full MobileNetV2 trainable from scratch ───────────────────────────
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)

# Unfreeze ALL layers — full training
for param in model.parameters():
    param.requires_grad = True

# Replace classifier head
model.classifier = nn.Sequential(
    nn.Dropout(0.4),
    nn.Linear(model.last_channel, 512),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(512, len(class_names)),
)

model = model.to(DEVICE)

total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Trainable parameters: {total_params:,}")

# ── Training ──────────────────────────────────────────────────────────────────
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
optimizer = torch.optim.Adam(model.parameters(), lr=LR, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)

best_acc = 0.0

if __name__ == "__main__":
    print("\nStarting full training from scratch...\n")
    for epoch in range(EPOCHS):
        model.train()
        running_loss, correct, total = 0, 0, 0
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            correct += (outputs.argmax(1) == labels).sum().item()
            total += labels.size(0)
            if i % 100 == 0:
                print(f"Epoch {epoch+1} step {i}/{len(train_loader)} — loss: {loss.item():.4f}")

        train_acc = correct / total
        scheduler.step()

        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                outputs = model(inputs)
                val_correct += (outputs.argmax(1) == labels).sum().item()
                val_total   += labels.size(0)

        val_acc = val_correct / val_total
        current_lr = optimizer.param_groups[0]['lr']
        print(f"\nEpoch {epoch+1}/{EPOCHS} — train_acc: {train_acc:.4f} — val_acc: {val_acc:.4f} — lr: {current_lr:.6f}\n")

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"  ✓ Saved best model (val_acc: {val_acc:.4f})")

    print(f"\nDone! Best val_accuracy: {best_acc:.4f}")
    print(f"Base model saved to {MODEL_SAVE_PATH}")
    print(f"\nNext step: run finetune.py to fine-tune the trained model")
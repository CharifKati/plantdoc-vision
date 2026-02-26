import os
import json
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

# ── Config ────────────────────────────────────────────────────────────────────
DATASET_PATH = DATASET_PATH = "merged_dataset_aug"  # place dataset folder next to this file
MODEL_LOAD_PATH   = "plantdoc_model_base.pth"       # output of Train.py
MODEL_SAVE_PATH   = "plantdoc_model_finetuned.pth"  # final model used by api.py
CLASS_NAMES_PATH  = "class_names.json"

IMG_SIZE   = 224
BATCH_SIZE = 32
EPOCHS     = 10
LR         = 1e-5  # very low LR for fine-tuning

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

val_size   = int(0.2 * len(full_dataset))
train_size = len(full_dataset) - val_size
train_ds, val_ds = torch.utils.data.random_split(
    full_dataset, [train_size, val_size],
    generator=torch.Generator().manual_seed(42)  # same seed as Train.py
)

train_ds.dataset.transform = transform
val_ds.dataset.transform   = val_transform

train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=0, pin_memory=True)
val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=0, pin_memory=True)

# ── Load base model ───────────────────────────────────────────────────────────
print(f"\nLoading base model from {MODEL_LOAD_PATH}...")

model = models.mobilenet_v2(weights=None)
model.classifier = nn.Sequential(
    nn.Dropout(0.4),
    nn.Linear(model.last_channel, 512),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(512, len(class_names)),
)
model.load_state_dict(torch.load(MODEL_LOAD_PATH, map_location=DEVICE))
model = model.to(DEVICE)

# Freeze everything then unfreeze last 10 layers + classifier for fine-tuning
for param in model.parameters():
    param.requires_grad = False

for param in model.features[-10:].parameters():
    param.requires_grad = True

for param in model.classifier.parameters():
    param.requires_grad = True

trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Trainable parameters: {trainable:,}")

# ── Fine-tune ─────────────────────────────────────────────────────────────────
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=LR,
    weight_decay=1e-4
)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=2, factor=0.5)

best_acc = 0.0

if __name__ == "__main__":
    print("\nStarting fine-tuning...\n")
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

        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
                outputs = model(inputs)
                val_correct += (outputs.argmax(1) == labels).sum().item()
                val_total   += labels.size(0)

        val_acc = val_correct / val_total
        print(f"\nEpoch {epoch+1}/{EPOCHS} — train_acc: {train_acc:.4f} — val_acc: {val_acc:.4f}\n")
        scheduler.step(val_acc)

        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"  ✓ Saved best model (val_acc: {val_acc:.4f})")

    print(f"\nDone! Best val_accuracy: {best_acc:.4f}")
    print(f"Fine-tuned model saved to {MODEL_SAVE_PATH}")
    print(f"\nNext step: restart the server with:")
    print(f"  uvicorn api:app --host 127.0.0.1 --port 8001")
import os
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.model_selection import train_test_split

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights

# ✅ Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "dataset")
CSV_PATH = os.path.join(DATA_DIR, "labels.csv")
IMG_DIR = os.path.join(DATA_DIR, "images")
MODEL_PATH = os.path.join(BASE_DIR, "app", "models", "best_state.pth")

# ✅ Dataset
class HCDataset(Dataset):
    def __init__(self, df, img_dir, transform):
        self.df = df.reset_index(drop=True)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(self.img_dir, row["filename"])
        img = Image.open(img_path).convert("RGB")
        x = self.transform(img)
        # log-transform target
        y = torch.tensor([np.log(float(row["head_circumference_mm"]))], dtype=torch.float32)
        return x, y

# ✅ Data loading
df = pd.read_csv(CSV_PATH)
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3),
])

train_ds = HCDataset(train_df, IMG_DIR, transform)
val_ds   = HCDataset(val_df, IMG_DIR, transform)

train_loader = DataLoader(train_ds, batch_size=16, shuffle=True)
val_loader   = DataLoader(val_ds, batch_size=16, shuffle=False)

# ✅ Model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
backbone = resnet18(weights=ResNet18_Weights.DEFAULT)
in_feats = backbone.fc.in_features
backbone.fc = nn.Sequential(
    nn.Linear(in_feats, 128),
    nn.ReLU(),
    nn.Linear(128, 1)  # regression (log HC)
)
model = backbone.to(device)

loss_fn = nn.MSELoss()
optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)

# ✅ Training
def evaluate(loader):
    model.eval()
    mse_sum, n = 0.0, 0
    with torch.no_grad():
        for imgs, hc_log in loader:
            imgs, hc_log = imgs.to(device), hc_log.to(device)
            pred = model(imgs)
            mse_sum += loss_fn(pred, hc_log).item() * imgs.size(0)
            n += imgs.size(0)
    return (mse_sum / n) ** 0.5

best_val = 1e9
patience, patience_counter = 5, 0

EPOCHS = 30
for epoch in range(1, EPOCHS+1):
    model.train()
    running_loss, count = 0.0, 0

    for imgs, hc_log in train_loader:
        imgs, hc_log = imgs.to(device), hc_log.to(device)

        optimizer.zero_grad()
        pred = model(imgs)
        loss = loss_fn(pred, hc_log)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * imgs.size(0)
        count += imgs.size(0)

    train_rmse = (running_loss / count) ** 0.5
    val_rmse = evaluate(val_loader)

    print(f"Epoch {epoch:02d} | Train RMSE: {np.exp(train_rmse):.2f} mm | Val RMSE: {np.exp(val_rmse):.2f} mm")

    if val_rmse < best_val:
        best_val = val_rmse
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"  ✅ Saved best_state.pth (Val RMSE: {np.exp(best_val):.2f} mm)")
        patience_counter = 0
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print("Early stopping.")
            break

print("Training complete. Model saved at:", MODEL_PATH)

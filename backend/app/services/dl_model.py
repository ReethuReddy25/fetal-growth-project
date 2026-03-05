import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

class FetalGrowthModel:
    def __init__(self, model_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        backbone = resnet18(weights=ResNet18_Weights.DEFAULT)

        in_feats = backbone.fc.in_features
        backbone.fc = nn.Sequential(
            nn.Linear(in_feats, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)   # ✅ regression head matches training
        )

        self.model = backbone.to(self.device)
        self.model.eval()

        # load trained weights
        print(f"[DEBUG] Loading model from: {model_path}")
        state_dict = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(state_dict, strict=True)

    def predict(self, img_tensor):
        """img_tensor: preprocessed image [1,3,224,224]"""
        with torch.no_grad():
            pred_log = self.model(img_tensor.to(self.device))
            pred_mm = torch.exp(pred_log).item()  # convert back from log(mm)
        return pred_mm

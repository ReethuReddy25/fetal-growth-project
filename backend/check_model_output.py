import torch
from app.services.dl_model import FetalGrowthModel
import os

# Path to model file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_state.pth")

# Load model
model = FetalGrowthModel(MODEL_PATH)

# Create dummy input to simulate an ultrasound image
dummy_input = torch.randn(1, 3, 224, 224)  # (batch_size, channels, height, width)

# Run model in evaluation mode
model.model.eval()
with torch.no_grad():
    output = model.model(dummy_input)

# Display output
print("\n=== Model Output Analysis ===")
print("Output shape:", output.shape)

# Determine if single or multiple measurements
if output.shape[1] == 1:
    print("This model predicts ONLY Head Circumference (HC).")
elif output.shape[1] == 3:
    print("This model predicts HC, AC, and FL (multi-parameter).")
else:
    print(f"Unexpected output size: {output.shape[1]} – check training configuration.")

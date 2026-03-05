import torch
from app.services.dl_model import FetalGrowthModel

# Path to trained model
MODEL_PATH = "models/best_state.pth"

# Initialize model
model = FetalGrowthModel(MODEL_PATH)

# Test image path (replace with your local test image)
test_image = "test_samples/25weeks_test.jpg"

# Run prediction
predicted_hc = model.predict(test_image)
print(f"Predicted Head Circumference (mm): {predicted_hc:.2f}")

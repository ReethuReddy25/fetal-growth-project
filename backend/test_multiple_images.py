import os
from app.services.dl_model import FetalGrowthModel
from app.services.who_growth import classify_growth

# Path to model
MODEL_PATH = os.path.join("backend", "models", "best_state.pth")

# Initialize model
model = FetalGrowthModel(MODEL_PATH)

# Folder containing test images
IMAGE_FOLDER = "test_samples/"  # Create this folder and put multiple images
GESTATIONAL_AGE = 25  # Example; adjust per case

print(f"--- Predicting for multiple images in '{IMAGE_FOLDER}' ---")

for image_name in os.listdir(IMAGE_FOLDER):
    image_path = os.path.join(IMAGE_FOLDER, image_name)

    if not image_path.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    hc_pred = model.predict(image_path)
    status, z_score = classify_growth(GESTATIONAL_AGE, hc_pred)

    print(f"\nImage: {image_name}")
    print(f"Predicted HC: {hc_pred:.2f} mm")
    print(f"Z-score: {z_score:.3f}" if z_score is not None else "Z-score: Unknown")
    print(f"Growth Status: {status}")

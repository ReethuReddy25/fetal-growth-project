import torch

MODEL_PATH = r"C:\Users\musku\Downloads\fetal_growth\backend\app\models\best_state.pth"

state_dict = torch.load(MODEL_PATH, map_location="cpu")

print("🔎 Keys in state_dict:")
for k in state_dict.keys():
    print(" ", k)

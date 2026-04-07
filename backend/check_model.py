import torch
from torchvision import models

# Load ResNet-18
model = models.resnet18(pretrained=True)

# Print full architecture
print(model)

print("\n--- Counting Layers ---")

count = 0
for name, module in model.named_modules():
    if isinstance(module, torch.nn.Conv2d) or isinstance(module, torch.nn.Linear):
        count += 1
        print(f"{count}: {name} -> {module}")

print("\nTotal Learnable Layers:", count)
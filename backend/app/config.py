# app/config.py

import os

# Absolute path to your trained model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "best_state.pth"
)

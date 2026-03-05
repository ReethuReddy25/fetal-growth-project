import json
import os
import numpy as np

# === WHO reference head circumference medians and SDs (mm) ===
# Extended 14–40 weeks
WHO_REFERENCES = {
    14: {"median": 100, "sd": 4.5},
    15: {"median": 111, "sd": 4.8},
    16: {"median": 123, "sd": 5.1},
    17: {"median": 135, "sd": 5.4},
    18: {"median": 148, "sd": 5.7},
    19: {"median": 161, "sd": 6.0},
    20: {"median": 173, "sd": 6.3},
    21: {"median": 186, "sd": 6.6},
    22: {"median": 198, "sd": 6.8},
    23: {"median": 210, "sd": 7.0},
    24: {"median": 222, "sd": 7.2},
    25: {"median": 233, "sd": 7.4},
    26: {"median": 244, "sd": 7.6},
    27: {"median": 254, "sd": 7.8},
    28: {"median": 264, "sd": 8.0},
    29: {"median": 273, "sd": 8.2},
    30: {"median": 281, "sd": 8.4},
    31: {"median": 289, "sd": 8.6},
    32: {"median": 296, "sd": 8.8},
    33: {"median": 303, "sd": 9.0},
    34: {"median": 309, "sd": 9.2},
    35: {"median": 315, "sd": 9.4},
    36: {"median": 321, "sd": 9.6},
    37: {"median": 326, "sd": 9.8},
    38: {"median": 332, "sd": 10.0},
    39: {"median": 337, "sd": 10.2},
    40: {"median": 342, "sd": 10.4},
}


def compute_z_score(hc_mm: float, ga_weeks: int) -> float:
    """Compute Z-score using WHO growth standards."""
    if ga_weeks not in WHO_REFERENCES:
        raise ValueError(f"Gestational age {ga_weeks} not supported (only 14–40 weeks).")

    ref = WHO_REFERENCES[ga_weeks]
    median, sd = ref["median"], ref["sd"]
    z = (hc_mm - median) / sd
    return float(z)


def classify_growth(z_score: float) -> str:
    """Classify fetal growth based on Z-score."""
    if z_score < -2:
        return "SGA"  # Small for Gestational Age
    elif z_score > 2:
        return "LGA"  # Large for Gestational Age
    else:
        return "AGA"  # Appropriate for Gestational Age

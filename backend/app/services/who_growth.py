# app/services/who_growth.py
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WHO_PATH = os.path.join(BASE_DIR, "who_reference.json")

# Load percentiles JSON like you provided (HC -> week -> percentiles dict)
with open(WHO_PATH, "r") as f:
    WHO_REFERENCE = json.load(f)


def _get_mean_std_from_percentiles(week_data: dict):
    """
    week_data is a dict like {"2.5": 86, "5": 88, "10": 91, "25": 95, "50": 100, ...}
    We'll derive:
      - mean = 50th percentile if present, else use median of available percentiles
      - std ≈ (P90 - P10) / 2.56  if both exist
          else std ≈ (P97.5 - P2.5) / 3.92  (normal approx: 97.5%-2.5% ~= 3.92*sd)
          else fallback to small epsilon to avoid division by zero
    """
    # Coerce keys to strings, values to floats
    pd = {str(k): float(v) for k, v in week_data.items()}

    # mean from 50th percentile when possible
    if "50" in pd:
        mean = pd["50"]
    elif "median" in pd:
        mean = pd["median"]
    else:
        # pick median of all available values
        vals = sorted(pd.values())
        mid = len(vals) // 2
        mean = vals[mid] if vals else 0.0

    # try P90-P10
    if "90" in pd and "10" in pd:
        std = (pd["90"] - pd["10"]) / 2.56  # approximate
    # fallback to P97.5 - P2.5
    elif "97.5" in pd and "2.5" in pd:
        std = (pd["97.5"] - pd["2.5"]) / 3.92  # approx (1.96*2 = 3.92)
    else:
        # fallback using IQR (75-25) -> IQR/1.35 approx SD if normal-ish
        if "75" in pd and "25" in pd:
            std = (pd["75"] - pd["25"]) / 1.35
        else:
            # very last resort: compute std of the listed values
            vals = list(pd.values())
            if len(vals) >= 2:
                import math
                m = sum(vals) / len(vals)
                var = sum((x - m) ** 2 for x in vals) / (len(vals) - 1)
                std = math.sqrt(var)
            else:
                std = 1.0  # avoid div-by-zero; extremely fallback

    # ensure positive
    if std <= 0:
        std = 1.0

    return float(mean), float(std)


def classify_growth(gestational_age: int, head_circumference: float):
    """
    Classify growth based on the WHO percentiles JSON.

    Returns: (status_string, z_score_float_or_None)
      status_string in {"SGA", "AGA", "LGA", "Unknown"}
    """
    ga_key = str(gestational_age)
    hc_ref = WHO_REFERENCE.get("HC", {})

    if ga_key not in hc_ref:
        return "Unknown", None

    week_data = hc_ref[ga_key]
    mean, std = _get_mean_std_from_percentiles(week_data)

    try:
        z_score = (float(head_circumference) - mean) / std
    except Exception:
        return "Unknown", None
        _log_debug(gestational_age, head_circumference, mean, std, z_score)


    # thresholds commonly used: z < -1.28 => approx <10th centile (SGA),
    # z > 1.28 => approx >90th centile (LGA)
    if z_score < -1.28:
        status = "SGA"
    elif z_score > 1.28:
        status = "LGA"
    else:
        status = "AGA"

    return status, float(z_score)
    # --- add inside who_growth.py ---

def _log_debug(ga, hc, mean, std, z):
    try:
        import logging
        logging.getLogger("who").info(
            f"[WHO DEBUG] GA={ga}w  PredHC={hc:.2f} mm  Mean={mean:.2f}  Std={std:.2f}  Z={z:.3f}"
        )
    except Exception:
        print(f"[WHO DEBUG] GA={ga}w  PredHC={hc:.2f} mm  Mean={mean:.2f}  Std={std:.2f}  Z={z:.3f}")


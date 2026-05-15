from typing import Any, Dict

import numpy as np

from models.model_loader import (
    get_stage1_interpreter,
    get_stage2_interpreter,
    get_stage3_plastic_interpreter,
    get_stage3_glass_interpreter,
    get_stage3_metal_interpreter,
    get_stage3_paper_interpreter,
    get_stage3_residual_interpreter,
)

# Labels for each stage – update with your actual labels
STAGE1_LABELS = ["non-recyclable", "recyclable"]
STAGE2_LABELS = ["glass", "metal", "paper", "plastic", "residual"]
STAGE3_PLASTIC_LABELS = ["HDPE", "LDPE", "PET", "Other Plastic", "PP", "PS", "PVC"]
STAGE3_GLASS_LABELS = ["Glass Cullet", "Flat Glass", "Glass Bottle"]
STAGE3_METAL_LABELS = ["Aluminum_Tin", "Copper", "Steel"]
STAGE3_PAPER_LABELS = ["Mixed Paper", "Old Corrugated Cartons", "Old Newspaper", "Selected White Ledger", "Used Beverage Cartons"]
STAGE3_RESIDUAL_LABELS = ["Clean and Dry Flexible Plastic", "Leather", "Rubber", "Textiles"]

# Tunable thresholds for uncertainty handling. Adjust from calibration data.
STAGE1_RECYCLABLE_LOW = 0.40
STAGE1_RECYCLABLE_HIGH = 0.60
STAGE2_MIN_CONFIDENCE = 0.55
STAGE2_MIN_MARGIN = 0.05
STAGE3_MIN_CONFIDENCE = 0.55
STAGE3_MIN_MARGIN = 0.05


def _run_inference(interpreter, input_array: np.ndarray) -> np.ndarray:
    """
    Run a single forward pass on a TFLite interpreter.
    """
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]["index"], input_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])

    return output_data[0]  # remove batch dimension


def _classify_binary_probability(p: float) -> tuple[str, float]:
    # Return label and confidence; 'uncertain' if within gray zone.
    if p >= STAGE1_RECYCLABLE_HIGH:
        return "recyclable", p
    if p <= STAGE1_RECYCLABLE_LOW:
        return "non_recyclable", 1.0 - p
    return "uncertain", max(p, 1.0 - p)


def _classify_multiclass(output: np.ndarray, labels: list[str]) -> tuple[str, float]:
    # Choose top class only if confidence and margin pass thresholds.
    sorted_indices = np.argsort(output)
    top1_idx = int(sorted_indices[-1])
    top2_idx = int(sorted_indices[-2])
    top1_conf = float(output[top1_idx])
    top2_conf = float(output[top2_idx])

    if top1_conf < STAGE2_MIN_CONFIDENCE or (top1_conf - top2_conf) < STAGE2_MIN_MARGIN:
        return "uncertain", top1_conf

    return labels[top1_idx], top1_conf


def classify_image(image_array: np.ndarray) -> Dict[str, Any]:
    """
    Given a preprocessed image array, run all three stages of classification
    and return a dict with stage results only.
    """
    # Stage 1: recyclable vs non_recyclable : single sigmoid output
    stage1_raw = _run_inference(get_stage1_interpreter(), image_array)

    p = float(stage1_raw[0])  # single value in [0, 1]

    stage1_label, stage1_conf = _classify_binary_probability(p)

    if stage1_label != "recyclable":
        return {
            "stage1": {"label": stage1_label, "confidence": stage1_conf},
            "stage2": None,
            "stage3": None,
        }

    # Stage 2: material type
    stage2_out = _run_inference(get_stage2_interpreter(), image_array)
    stage2_sorted = np.argsort(stage2_out)
    stage2_idx = int(stage2_sorted[-1])
    stage2_conf = float(stage2_out[stage2_idx])

    # If top-class confidence is below threshold, mark stage2 uncertain
    if stage2_conf < STAGE2_MIN_CONFIDENCE:
        return {
            "stage1": {"label": stage1_label, "confidence": stage1_conf},
            "stage2": {"label": "uncertain", "confidence": stage2_conf},
            "stage3": None,
        }

    stage2_label = STAGE2_LABELS[stage2_idx]

    # Stage 3: subcategory based on stage2 material
    if stage2_label == "plastic":
        interpreter = get_stage3_plastic_interpreter()
        labels = STAGE3_PLASTIC_LABELS
    elif stage2_label == "glass":
        interpreter = get_stage3_glass_interpreter()
        labels = STAGE3_GLASS_LABELS
    elif stage2_label == "metal":
        interpreter = get_stage3_metal_interpreter()
        labels = STAGE3_METAL_LABELS
    elif stage2_label == "paper":
        interpreter = get_stage3_paper_interpreter()
        labels = STAGE3_PAPER_LABELS
    else:
        interpreter = get_stage3_residual_interpreter()
        labels = STAGE3_RESIDUAL_LABELS

    stage3_out = _run_inference(interpreter, image_array)
    stage3_sorted = np.argsort(stage3_out)
    stage3_idx = int(stage3_sorted[-1])
    stage3_conf = float(stage3_out[stage3_idx])

    # If top-class confidence is below threshold, mark stage3 uncertain
    if stage3_conf < STAGE3_MIN_CONFIDENCE:
        stage3_label = "uncertain"
    else:
        stage3_label = labels[stage3_idx]

    return {
        "stage1": {"label": stage1_label, "confidence": stage1_conf},
        "stage2": {"label": stage2_label, "confidence": stage2_conf},
        "stage3": {"label": stage3_label, "confidence": stage3_conf},
    }
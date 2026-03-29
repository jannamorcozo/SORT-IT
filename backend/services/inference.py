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
STAGE1_LABELS = ["recyclable", "non_recyclable"]
STAGE2_LABELS = ["glass", "metal", "paper", "plastic", "residual"]
STAGE3_PLASTIC_LABELS = ["HDPE", "LDPE", "Other Plastic", "PET", "PP", "PS", "PVC"]
STAGE3_GLASS_LABELS = ["Glass Bottle", "Glass Cullet", "Flat Glass"]
STAGE3_METAL_LABELS = ["Aluminum_Tin", "Copper", "Steel"]
STAGE3_PAPER_LABELS = ["Mixed Paper", "Old Corrugated Cartons", "Old Newspaper", "Selected White Ledger", "Used Beverage Cartons"]
STAGE3_RESIDUAL_LABELS = ["Clean and Dry Flexible Plastic", "Leather", "Rubber", "Textiles"]


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


def classify_image(image_array: np.ndarray) -> Dict[str, Any]:
    """
    Given a preprocessed image array, run all three stages of classification
    and return a dict with stage results only.
    """
    # Stage 1: recyclable vs non_recyclable : single sigmoid output
    stage1_raw = _run_inference(get_stage1_interpreter(), image_array)
    
    print("Stage1 RAW shape:", stage1_raw.shape)
    print("Stage1 RAW values:", stage1_raw)

    p = float(stage1_raw[0])  # single value in [0, 1]
    print("DEBUG Stage1 sigmoid:", p)

    threshold = 0.5
    # TRY VERSION A (most likely correct)
    if p >= threshold:
        stage1_label = "recyclable"
        stage1_conf = p
    else:
        stage1_label = "non_recyclable"
        stage1_conf = 1.0 - p

    print("DEBUG Final Stage1:", stage1_label, stage1_conf)

    if stage1_label != "recyclable":
        return {
            "stage1": {"label": stage1_label, "confidence": stage1_conf},
            "stage2": None,
            "stage3": None,
        }

    # Stage 2: material type
    stage2_out = _run_inference(get_stage2_interpreter(), image_array)
    stage2_idx = int(np.argmax(stage2_out))
    stage2_label = STAGE2_LABELS[stage2_idx]
    stage2_conf = float(stage2_out[stage2_idx])

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
    stage3_idx = int(np.argmax(stage3_out))
    stage3_label = labels[stage3_idx]
    stage3_conf = float(stage3_out[stage3_idx])

    return {
        "stage1": {"label": stage1_label, "confidence": stage1_conf},
        "stage2": {"label": stage2_label, "confidence": stage2_conf},
        "stage3": {"label": stage3_label, "confidence": stage3_conf},
    }
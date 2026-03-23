import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models")
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH", "sort-it_firebase_key.json")
MODEL_DOWNLOAD_TIMEOUT_SECONDS = int(os.getenv("MODEL_DOWNLOAD_TIMEOUT_SECONDS", "120"))

MODEL_FILENAMES = {
    "stage1": "stage1_mobilenetv3f.keras",
    "stage2": "stage2_mobilenetv3f.keras",
    "stage3_plastic": "stage3_plastic_mobilenetv3f.keras",
    "stage3_paper": "stage3_paper_mobilenetv3f.keras",
    "stage3_metal": "stage3_metal_mobilenetv3f.keras",
    "stage3_glass": "stage3_glass_mobilenetv3f.keras",
    "stage3_residual": "stage3_residual_mobilenetv3f.keras",
}

MODEL_URLS = {
    "stage1": os.getenv("MODEL_URL_STAGE1", ""),
    "stage2": os.getenv("MODEL_URL_STAGE2", ""),
    "stage3_plastic": os.getenv("MODEL_URL_STAGE3_PLASTIC", ""),
    "stage3_paper": os.getenv("MODEL_URL_STAGE3_PAPER", ""),
    "stage3_metal": os.getenv("MODEL_URL_STAGE3_METAL", ""),
    "stage3_glass": os.getenv("MODEL_URL_STAGE3_GLASS", ""),
    "stage3_residual": os.getenv("MODEL_URL_STAGE3_RESIDUAL", ""),
}

STAGE1_LABELS = ["non_recyclable", "recyclable"]
STAGE2_LABELS = ["plastic", "glass", "metal", "paper", "residual"]
STAGE3_LABELS = {
    "plastic": ["PET", "HDPE", "PVC", "LDPE", "PP", "PS", "Other"],
    "paper": ["SWL", "ONP", "OCC", "MP", "UBC"],
    "metal": ["Aluminum_Tin", "Copper", "Steel"],
    "glass": ["Bottle", "Flat", "Cullets"],
    "residual": ["Flexible Plastics", "Leather", "Textiles", "Rubber"],
}

import csv
import shutil
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForImageClassification, AutoImageProcessor

import OpenEXR
import Imath
from tqdm import tqdm

# ----------------------------
# CONFIG
# ----------------------------
MODEL_PATH = "./outputs_wrong_images/checkpoint-640"
INPUT_DIR = Path(r"C:\depth")

WRONG_OUTPUT_DIR = Path(r"C:\depth_wrong")
WRONG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = "predictions.csv"

BATCH_SIZE = 16
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ----------------------------
# EXR LOADER
# ----------------------------
def read_exr(path):
    exr = OpenEXR.InputFile(str(path))
    header = exr.header()

    dw = header["dataWindow"]
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1

    pt = Imath.PixelType(Imath.PixelType.FLOAT)

    raw = exr.channel("R", pt)
    img = np.frombuffer(raw, dtype=np.float32).reshape(height, width)

    return img


# ----------------------------
# MODEL
# ----------------------------
processor = AutoImageProcessor.from_pretrained(MODEL_PATH)
model = AutoModelForImageClassification.from_pretrained(MODEL_PATH)

model.to(DEVICE)
model.eval()


# ----------------------------
# PREPROCESS
# ----------------------------
def preprocess(path):
    img = read_exr(path).astype(np.float32)

    # normalize
    img = (img - img.min()) / (img.max() - img.min() + 1e-6)

    # (1, H, W)
    img = np.expand_dims(img, axis=0)

    # ViT expects 3 channels
    img = np.repeat(img, 3, axis=0)

    img = torch.tensor(img).float()

    # resize to 224x224
    img = F.interpolate(
        img.unsqueeze(0),
        size=(224, 224),
        mode="bilinear",
        align_corners=False
    ).squeeze(0)

    return img


# ----------------------------
# COLLECT FILES
# ----------------------------
files = [f for f in INPUT_DIR.iterdir() if f.is_file() and f.suffix == ".exr"]


# ----------------------------
# BATCH INFERENCE
# ----------------------------
results = []

with torch.no_grad():
    for i in tqdm(range(0, len(files), BATCH_SIZE), desc="Inference"):
        batch_files = files[i:i + BATCH_SIZE]

        batch_tensors = []
        batch_names = []

        for f in batch_files:
            batch_tensors.append(preprocess(f))
            batch_names.append(f.name)

        batch = torch.stack(batch_tensors).to(DEVICE)

        outputs = model(pixel_values=batch)
        logits = outputs.logits

        probs = torch.softmax(logits, dim=1)

        preds = torch.argmax(probs, dim=1)

        for j, file_path in enumerate(batch_files):

            pred_id = preds[j].item()
            label = model.config.id2label.get(pred_id, str(pred_id))
            confidence = probs[j, pred_id].item()

            results.append({
                "file": file_path.name,
                "label": label,
                "confidence": confidence
            })

            # ----------------------------
            # COPY WRONG FILES
            # ----------------------------
            if label == "wrong":
                target_path = WRONG_OUTPUT_DIR / file_path.name

                # avoid overwrite
                if target_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    target_path = WRONG_OUTPUT_DIR / f"{stem}_{i+j}{suffix}"

                shutil.copy2(file_path, target_path)

# ----------------------------
# SAVE CSV
# ----------------------------
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["file", "label", "confidence"])
    writer.writeheader()
    writer.writerows(results)

print(f"Saved predictions to {OUTPUT_CSV}")
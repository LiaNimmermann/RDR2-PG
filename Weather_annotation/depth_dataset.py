import os
import numpy as np
import OpenEXR
import Imath
import torch

from datasets import Dataset, DatasetDict, Features, ClassLabel, Value

# -----------------------------
# EXR READER (robust + fast)
# -----------------------------
def read_exr(path):
    exr = OpenEXR.InputFile(path)
    header = exr.header()

    dw = header["dataWindow"]
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1

    pt = Imath.PixelType(Imath.PixelType.FLOAT)

    # Most depth maps use "R"
    if "R" in header["channels"]:
        raw = exr.channel("R", pt)
        img = np.frombuffer(raw, dtype=np.float32)
        img = img.reshape(height, width)
    else:
        # fallback: try RGB average
        channels = []
        for c in ["R", "G", "B"]:
            if c in header["channels"]:
                raw = exr.channel(c, pt)
                channels.append(np.frombuffer(raw, dtype=np.float32).reshape(height, width))

        img = np.mean(channels, axis=0)

    return img


# -----------------------------
# BUILD DATASET FROM FOLDERS
# -----------------------------
def build_exr_dataset(root_dir):
    class_names = sorted([
        d for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d))
    ])

    class_to_id = {c: i for i, c in enumerate(class_names)}

    samples = []

    for cls in class_names:
        class_path = os.path.join(root_dir, cls)

        for file in os.listdir(class_path):
            if file.endswith(".exr"):
                samples.append({
                    "image": os.path.join(class_path, file),
                    "label": cls   # IMPORTANT: store STRING, not int
                })

    features = Features({
        "image": Value("string"),
        "label": ClassLabel(names=class_names)
    })

    dataset = Dataset.from_list(samples, features=features)

    return dataset

# -----------------------------
# TRANSFORM (called during training)
# -----------------------------
_cache = {}

def exr_transform(example):
    path = example["image"]

    if path in _cache:
        img = _cache[path]
    else:
        img = read_exr(path)

        img = img.astype(np.float32)
        img = (img - img.min()) / (img.max() - img.min() + 1e-6)

        img = np.expand_dims(img, axis=0)
        img = np.repeat(img, 3, axis=0)
        _cache[path] = img
    return {
        "image": torch.tensor(img, dtype=torch.float32),
        "labels": example["label"]  # already int from ClassLabel
    }

# -----------------------------
# CREATE DATASETDICT
# -----------------------------
def load_dataset(train_dir, val_dir=None):
    train_ds = build_exr_dataset(train_dir)

    dataset = DatasetDict({
        "train": train_ds
    })

    if val_dir:
        dataset["validation"] = build_exr_dataset(val_dir)

    dataset = dataset.with_transform(exr_transform)

    return dataset
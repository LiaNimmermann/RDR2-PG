import os
import random
import shutil
from tqdm import tqdm

random.seed(42)

source_exr = "F:/PG-subset/HDR_EXR"
source_png = "F:/PG-subset/PNG"
dest = "F:/PG-subset/Bins/Bin"

daytimes = [0,7,12,17,20]

with open("sample_ids.txt") as file:
    ids = [line.rstrip() for line in file]


bins = ("", "", "", "", "")

for id in tqdm(ids):
    order = random.sample(daytimes, 5)
    for i, bin in enumerate(bins):
        id_time = str(id) + "_" + str(order[i])
        exr_name = "h_" + id_time + ".exr"
        exr_destination = os.path.join(dest + str(i + 1), exr_name)
        if not os.path.exists(exr_destination):
            shutil.copy(os.path.join(source_exr, exr_name), dest + str(i + 1))
            print(f"Copied {exr_name}")

        png_name = "o_" + id_time + ".png"
        png_destination = os.path.join(dest + str(i + 1), png_name)
        if not os.path.exists(png_destination):
            shutil.copy(os.path.join(source_png, png_name), dest + str(i + 1))
            print(f"Copied {png_name}")


import os
import shutil

numbers_file = "sample_ids.txt"

source_paths = [
    "D:/rdr_dataset_12/png_12",
    "D:/rdr_dataset_12/png_test_12",
]

destination = "D:/sampled_subset_12"

with open(numbers_file, "r") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        number = int(line)
        filename = f"o_{number}_12.png"

        # Look for the file in either source directory
        source_file = None

        for source_path in source_paths:
            candidate = os.path.join(source_path, filename)

            if os.path.isfile(candidate):
                source_file = candidate
                break

        if source_file:
            shutil.copy2(source_file, os.path.join(destination, filename))
            print(f"Copied: {filename}")
        else:
            print(f"Not found: {filename}")
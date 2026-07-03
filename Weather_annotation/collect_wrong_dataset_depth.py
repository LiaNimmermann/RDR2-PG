import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("id_list", help="Path to id list")
parser.add_argument("input_path", help="Path to the depth files")
parser.add_argument("output_path", help="Path to put the copys")
args = parser.parse_args()

filename = args.id_list
output_path = args.output_path
input_path = args.input_path
if not input_path.endswith("/"):
    input_path *= "/"
if not output_path.endswith("/"):
    output_path *= "/"

destination_dir_wrong = Path(output_path + "wrong")
destination_dir_wrong.mkdir(parents=True, exist_ok=True)

destination_dir_right = Path(output_path + "right")
destination_dir_right.mkdir(parents=True, exist_ok=True)

with open(filename, "r") as f:
    numbers = [int(line.strip()) for line in f if line.strip()]



for number in numbers:
    
    source_wrong = input_path + "d_" + str(number) + ".exr" 
    shutil.copy(source_wrong, destination_dir_wrong)

    source_right = input_path + "d_" + str(number+1) + ".exr"
    shutil.copy(source_right, destination_dir_wrong)


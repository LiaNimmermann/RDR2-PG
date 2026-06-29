import json
import tqdm
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
import shutil



dict_all_captures = {}

with open("D:/rdr_dataset_12/all_captures_with_weather.json", 'r+') as json_file:
    dict_all_captures = json.load(json_file)
    ids = dict_all_captures.keys()
    for id in tqdm.tqdm(ids):
        weather = dict_all_captures[id]["Capture"]["Weather"]
        origin_path = "D:/rdr_dataset_12/png_12/o_" + id + "_12.png"
        target_path = "D:/WeatherDataset_pngs/"
        
        pred_weather = dict_all_captures[id]["Capture"]["Weather_Predicted"]
        if weather == "fog":
            target_path += "fog"
        elif pred_weather == "overcast":
            target_path += "pred_overcast"
        else:
            continue

        shutil.copy(origin_path, target_path)
    
#with open("D:/rdr_dataset_12/all_captures_test_with_weather.json", 'r+') as json_file:
#    json.dump(dict_all_captures, json_file)

print("*"*50)
print("Done")
print("*"*50)

import json
import tqdm
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification


processor = AutoImageProcessor.from_pretrained("./outputs")
model = AutoModelForImageClassification.from_pretrained("./outputs/checkpoint-3000")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

dict_all_captures = {}

with open("D:/rdr_dataset_12/all_captures_test.json", 'r+') as json_file:
    dict_all_captures = json.load(json_file)
    ids = dict_all_captures.keys()
    for id in tqdm.tqdm(ids):
        image = Image.open("D:/rdr_dataset_12/png_test_12/o_" + id + "_12.png").convert("RGB")

        inputs = processor(images=image, return_tensors="pt")

        
        inputs.to(device)
        with torch.no_grad():   
            outputs = model(**inputs)
        
        logits = outputs.logits
        
        predicted_class_idx = logits.argmax(-1).item()

        label = model.config.id2label[predicted_class_idx]

        dict_all_captures[id]["Capture"]["Weather_Predicted"] = label
    
with open("D:/rdr_dataset_12/all_captures_test_with_weather.json", 'r+') as json_file:
    json.dump(dict_all_captures, json_file)

print("*"*50)
print("Done")
print("*"*50)

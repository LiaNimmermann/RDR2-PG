import json
import tqdm
from PIL import Image
import torch
from collections import Counter
from transformers import AutoImageProcessor, AutoModelForImageClassification

if True:
    processor = AutoImageProcessor.from_pretrained("./outputs_august_3")
    model = AutoModelForImageClassification.from_pretrained("./outputs_august_3/checkpoint-1300")
if False:
    processor = AutoImageProcessor.from_pretrained("./outputs_august")
    model = AutoModelForImageClassification.from_pretrained("./outputs_august/checkpoint-500")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

dict_all_captures = {}

with open("D:/rdr_dataset_12/all_captures_with_weather_2.json", 'r+') as json_file:
    dict_all_captures = json.load(json_file)
    ids = dict_all_captures.keys()
    for id in tqdm.tqdm(ids):
        image = Image.open("D:/rdr_dataset_12/png_12/o_" + id + "_12.png").convert("RGB")

        inputs = processor(images=image, return_tensors="pt")

        
        inputs.to(device)
        with torch.no_grad():   
            outputs = model(**inputs)
        
        logits = outputs.logits
        
        predicted_class_idx = logits.argmax(-1).item()

        label = model.config.id2label[predicted_class_idx]

        dict_all_captures[id]["Capture"]["Weather_Predicted_3"] = label

        if True:
            label1 = dict_all_captures[id]["Capture"]["Weather_Predicted"]
            label2 = dict_all_captures[id]["Capture"]["Weather_Predicted_2"]
            
            dict_all_captures[id]["Capture"]["Weather_Predicted_1"] = label1

            labels = [label1, label2, label]
            counts = Counter(labels)

            if counts.most_common(1)[0][1] >= 2:
                final_label = counts.most_common(1)[0][0]
            else:
                final_label = "uncertain"
        

            dict_all_captures[id]["Capture"]["Weather_Predicted"] = final_label

    
with open("D:/rdr_dataset_12/all_captures_with_weather_3.json", 'w') as json_file:
    json.dump(dict_all_captures, json_file, indent=4)

print("*"*50)
print("Done")
print("*"*50)

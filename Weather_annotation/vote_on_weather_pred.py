import json
import tqdm
from collections import Counter


with open("D:/rdr_dataset_12/all_captures_test_with_weather_3.json", 'r+') as json_file:
    dict_all_captures = json.load(json_file)
    ids = dict_all_captures.keys()
    for id in tqdm.tqdm(ids):

        label1 = dict_all_captures[id]["Capture"]["Weather_Predicted"]
        label2 = dict_all_captures[id]["Capture"]["Weather_Predicted_2"]
        label3 = dict_all_captures[id]["Capture"]["Weather_Predicted_3"]

        dict_all_captures[id]["Capture"]["Weather_Predicted_1"] = label1

        labels = [label1, label2, label3]

        final_label = Counter(labels).most_common(1)[0][0]


    
with open("D:/rdr_dataset_12/all_captures_test_with_weather_voted.json", 'w') as json_file:
    json.dump(dict_all_captures, json_file, indent=4)

print("*"*50)
print("Done")
print("*"*50)

import random
from collections import defaultdict
import json
import argparse

def load_json(path):
    with open(path, 'r') as f:
        captures = json.load(f)

    return captures

def filter_one_small_entity(captures, size=50):
    filtered = {i:captures[i] for i in captures if captures[i]["Capture"]["EntityCount"]==1 and is_entity_smaller_than(captures[i]['Entities'][0],size=size)}
    return filtered

def collect_captures_for_weather(captures, weather):
    filtered = {i:captures[i] for i in captures if captures[i]["Capture"]["Weather_Predicted"]==weather}
    return filtered

def is_entity_smaller_than(entity, size):
    w1,h1,w2,h2 = entity["BoundingBoxCalculated"]
    return (w2-w1<size) or (h2-h1<size)


def sample(path, size=50):
    captures = load_json(path)        
    captures = filter_one_small_entity(captures, size=size)
    print(f"{len(captures.items())} Captures with one entity.")
    weathers = ["clear", "cloudy", "overcast"]
    daytimes = ["0", "7", "12", "17", "20"]

    ids = []

    weatherbins = []
    for weather in weathers:
        filtered = collect_captures_for_weather(captures, weather=weather)
        weatherbins.append((weather, filtered))
        print(f"{len(filtered.items())} captures with {weather} weather")

    print(f"{len(ids.items())} samples")



    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an RDR2 dataset subset.")
    parser.add_argument("--size", nargs="?", type=int, default=50, help="Threshold Size for filtering only small animals")
    parser.add_argument("--src_root", nargs="?", default="D:/rdr_dataset_12/all_captures_with_weather_3.json", help="Source dataset root")
    args = parser.parse_args()
    sample(args.src_root, args.size)
    print("DONE")
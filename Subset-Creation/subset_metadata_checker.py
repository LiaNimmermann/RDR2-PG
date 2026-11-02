import json

with open("F:/PG-subset/all_captures.json", "r") as f:
    data = json.load(f)


bboxes = {}

with open("sample_ids.txt", "r") as ids:
    for id in ids:
        id = id.strip()
        try:
            capture = data[id]
        except KeyError:
            print(f"ID not found: {id}")
            continue
        bbox = capture["Entities"][0]["BoundingBoxCalculated"]
        bboxes[id] = bbox

with open("bboxes.json", "w") as output:
    json.dump(bboxes, output, indent=4)

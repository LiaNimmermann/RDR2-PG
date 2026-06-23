
from PIL import Image
import json
from torch.utils.data import Dataset


class WeatherDataset(Dataset):
    def __init__(self, data, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        # Load data from JSON file
        self.data = []
        with open(data, 'r') as f:
            self.data = json.load(f)


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image_path, label = self.data[idx]["image"], self.data[idx]["labels"]
        
        image = Image.open(self.image_dir + "/" + image_path).convert("RGB")
        
        if self.transform:
            image = self.transform(image)
        
        return image, label, image_path
    

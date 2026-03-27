import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

class MedicalClassifier:
    def __init__(self):
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def predict(self, img_path):
        if not os.path.exists(img_path):
            return "File not found", 0.0
        
        img = Image.open(img_path).convert('RGB')
        img_t = self.transform(img).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(img_t)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, index = torch.max(probabilities, 0)
            
        return index.item(), confidence.item()

if __name__ == "__main__":
    clf = MedicalClassifier()
    images = ["images/xray_chest.png", "images/attacked_xray_neck.png"]
    
    print(f"{'Image':<30} | {'Class ID':<10} | {'Confidence':<10}")
    print("-" * 55)
    
    for img_p in images:
        if os.path.exists(img_p):
            idx, conf = clf.predict(img_p)
            print(f"{img_p:<30} | {idx:<10} | {conf:.2%}")
        else:
            print(f"{img_p:<30} | Not Found  | N/A")

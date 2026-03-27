import torch
from torchvision import models, transforms
from PIL import Image
import os

class MedicalCNN:
    def __init__(self):
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def diagnose(self, img_path):
        if not os.path.exists(img_path):
            return None, 0.0
        img = Image.open(img_path).convert('RGB')
        img_t = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            outputs = self.model(img_t)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            conf, idx = torch.max(probs, 0)
        return idx.item(), conf.item()

if __name__ == "__main__":
    scanner = MedicalCNN()
    target_images = ["images/xray_chest.png", "images/attacked_xray_neck.png"]
    print(f"\n{'Target Image':<30} | {'Class ID':<10} | {'AI Confidence'}")
    print("-" * 65)
    for path in target_images:
        idx, conf = scanner.diagnose(path)
        if idx is not None:
            print(f"{path:<30} | {idx:<10} | {conf:.2%}")
        else:
            print(f"{path:<30} | Not Found  | ---")

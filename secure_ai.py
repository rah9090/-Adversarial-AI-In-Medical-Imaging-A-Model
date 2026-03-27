import torch
import hashlib
from torchvision import models, transforms
from PIL import Image
import os

class MedicalSecuritySystem:
    def __init__(self):
       
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
   
        self.blockchain_ledger = {
            "images/xray_chest.png": "4d5c94dbf3221ea59a07fa6a03ee9051"
        }

    def get_hash(self, img_path):
        with open(img_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def secure_diagnose(self, img_path):
        if not os.path.exists(img_path):
            return None, "FILE_NOT_FOUND"

        current_hash = self.get_hash(img_path)
        original_hash = self.blockchain_ledger.get(img_path)

      
        if original_hash and current_hash != original_hash:
            return None, "ATTACK_DETECTED"

        img = Image.open(img_path).convert('RGB')
        img_t = self.transform(img).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(img_t)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            conf, idx = torch.max(probs, 0)
        return (idx.item(), conf.item()), "SECURE_VERIFIED"

if __name__ == "__main__":
    system = MedicalSecuritySystem()
    test_images = ["images/xray_chest.png", "images/attacked_xray_neck.png"]
    
    print(f"\n{'Path':<30} | {'Status':<20} | {'Diagnosis'}")
    print("-" * 75)
    for path in test_images:
        res, status = system.secure_diagnose(path)
        output = f"ID:{res[0]} ({res[1]:.2%})" if res else "BLOCKED"
        print(f"{path:<30} | {status:<20} | {output}")

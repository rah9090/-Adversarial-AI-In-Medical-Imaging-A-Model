import torch
import hashlib
from torchvision import models, transforms
from PIL import Image
import os
import matplotlib.pyplot as plt


model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def get_file_hash(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


blockchain_ledger = {
    "images/xray_chest.png": get_file_hash("images/xray_chest.png"),
    "images/xray_neck.png": get_file_hash("images/xray_neck.png")
}

def secure_diagnosis(img_path, original_key):
    current_hash = get_file_hash(img_path)
    original_hash = blockchain_ledger.get(original_key)
    
   
    is_secure = (current_hash == original_hash and current_hash is not None)
    
  
    img = Image.open(img_path).convert('RGB')
    img_t = transform(img).unsqueeze(0)
    with torch.no_grad():
        out = model(img_t)
        _, idx = torch.max(out, 1)
    
    return idx.item(), is_secure


test_cases = [
    ("images/xray_chest.png", "images/xray_chest.png", "Original Chest"),
    ("images/attacked_chest.png", "images/xray_chest.png", "Attacked Chest"),
    ("images/xray_neck.png", "images/xray_neck.png", "Original Neck"),
    ("images/attacked_neck.png", "images/xray_neck.png", "Attacked Neck")
]

plt.figure(figsize=(15, 10))
for i, (path, key, label) in enumerate(test_cases):
    if os.path.exists(path):
        plt.subplot(2, 2, i+1)
        diag_id, secure = secure_diagnosis(path, key)
        
        status = "SECURE (Verified)" if secure else "ATTACK DETECTED (Blocked)"
        color = "green" if secure else "red"
        
        plt.imshow(Image.open(path))
        plt.title(f"{label}\nAI ID: {diag_id}\n{status}", color=color, fontweight='bold', fontsize=12)
        plt.axis('off')

plt.tight_layout()
plt.savefig('blockchain_security_result.png')
print("--- Success! Showing the Security Comparison ---")
plt.show()

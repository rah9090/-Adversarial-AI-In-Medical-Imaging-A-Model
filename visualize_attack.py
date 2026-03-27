import torch
import matplotlib.pyplot as plt
from torchvision import models, transforms
from PIL import Image
import os


model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def get_prediction(img_path):
    if not os.path.exists(img_path):
        return "N/A"
    img = Image.open(img_path).convert('RGB')
    img_t = transform(img).unsqueeze(0)
    with torch.no_grad():
        out = model(img_t)
        _, idx = torch.max(out, 1)
    return idx.item()


images = ["images/xray_chest.png", "images/attacked_xray_neck.png"]
titles = ["Original (Safe)", "Attacked (PGD)"]

plt.figure(figsize=(10, 5))
for i, path in enumerate(images):
    if os.path.exists(path):
        plt.subplot(1, 2, i+1)
        plt.imshow(Image.open(path))
        pred_id = get_prediction(path)
        plt.title(f"{titles[i]}\nAI Sees Class ID: {pred_id}")
        plt.axis('off')
    else:
        print(f"File not found: {path}")

print("Displaying comparison window...")
plt.show()

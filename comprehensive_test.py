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

def process_and_attack(path):
    if not os.path.exists(path):
        return None, None, "N/A", "N/A"
    

    img = Image.open(path).convert('RGB')
    img_t = transforms.ToTensor()(transforms.Resize((224, 224))(img)).unsqueeze(0)
    img_t.requires_grad = True
    
    orig_out = model(transform(img).unsqueeze(0))
    orig_idx = torch.max(orig_out, 1)[1].item()
    
  
    out = model(img_t)
    loss = out.sum()
    model.zero_grad(); loss.backward()
    
    
    attacked_t = torch.clamp(img_t + 0.02 * img_t.grad.sign(), 0, 1)
    attacked_img = transforms.ToPILImage()(attacked_t.squeeze())
    
    
    attack_out = model(transform(attacked_img).unsqueeze(0))
    attack_idx = torch.max(attack_out, 1)[1].item()
    
    return img, attacked_img, orig_idx, attack_idx


targets = [('images/xray_chest.png', 'Chest'), ('images/xray_neck.png', 'Neck')]
plt.figure(figsize=(12, 8))

for i, (path, name) in enumerate(targets):
    orig, atk, o_id, a_id = process_and_attack(path)
    if orig:
        plt.subplot(2, 2, i*2 + 1)
        plt.imshow(orig); plt.title(f"Original {name}\nAI ID: {o_id}"); plt.axis('off')
        
        plt.subplot(2, 2, i*2 + 2)
        plt.imshow(atk); plt.title(f"Attacked {name}\nAI ID: {a_id}"); plt.axis('off')

plt.tight_layout()
plt.savefig('final_comparison_result.png')
print("--- Done! ---")
print("Check the pop-up window or 'final_comparison_result.png'")
plt.show()

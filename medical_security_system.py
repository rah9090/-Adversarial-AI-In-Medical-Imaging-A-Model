import torch
import hashlib
import os
from torchvision import models, transforms
from PIL import Image

# 1. إعداد النموذج والأدوات
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

# تحويلات الصور للذكاء الاصطناعي
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def get_hash(path):
    """حساب بصمة الملف (وظيفة البلوكشين)"""
    if not os.path.exists(path): return None
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def create_attack(orig_path, atk_path):
    """صنع نسخة مهاجمة مخفية (Adversarial Attack)"""
    if not os.path.exists(orig_path): return
    img = Image.open(orig_path).convert('RGB')
    img_t = transforms.ToTensor()(transforms.Resize((224, 224))(img)).unsqueeze(0)
    img_t.requires_grad = True
    
    # هجوم سريع لتغيير التصنيف (FGSM)
    out = model(img_t)
    loss = out.sum()
    model.zero_grad(); loss.backward()
    
    # إضافة تشويش بسيط جداً (0.02) لا تراه العين
    atk_t = torch.clamp(img_t + 0.02 * img_t.grad.sign(), 0, 1)
    transforms.ToPILImage()(atk_t.squeeze()).save(atk_path)

# 2. تجهيز البيانات (المحاكاة)
images_dir = "images"
if not os.path.exists(images_dir): os.makedirs(images_dir)

# صنع الهجمات إذا لم تكن موجودة
create_attack('images/xray_chest.png', 'images/attacked_chest.png')
create_attack('images/xray_neck.png', 'images/attacked_neck.png')

# سجل البلوكشين (يحتوي فقط على بصمات الصور الأصلية)
blockchain_ledger = {
    "images/xray_chest.png": get_hash("images/xray_chest.png"),
    "images/xray_neck.png": get_hash("images/xray_neck.png")
}

# 3. طباعة الجدول النهائي
print(f"\n{'Target Image':<28} | {'Blockchain':<10} | {'Class ID':<10} | {'AI Confidence'}")
print("-" * 75)

test_cases = [
    ("images/xray_chest.png", "images/xray_chest.png"),
    ("images/attacked_chest.png", "images/xray_chest.png"),
    ("images/xray_neck.png", "images/xray_neck.png"),
    ("images/attacked_neck.png", "images/xray_neck.png")
]

for path, key in test_cases:
    if not os.path.exists(path): continue
    
    # فحص النزاهة (Integrity Check)
    current_hash = get_hash(path)
    orig_hash = blockchain_ledger.get(key)
    status = "✅ VALID" if current_hash == orig_hash else "❌ ATTACKED"
    
    # تشخيص الـ AI
    img = Image.open(path).convert('RGB')
    img_t = transform(img).unsqueeze(0)
    with torch.no_grad():
        out = model(img_t)
        prob = torch.nn.functional.softmax(out[0], dim=0)
        conf, idx = torch.max(prob, 0)
    
    print(f"{path:<28} | {status:<10} | {idx.item():<10} | {conf.item():.2%}")


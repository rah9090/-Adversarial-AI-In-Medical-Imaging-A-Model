import hashlib
from PIL import Image
import io
import os

LEDGER = {
    "xray_chest.png": "ff91cc4ec1e5606e64a39f8e7a49bcb4eaa7dd8ce3a4a4f54401d2ba09b0cdda",
    "xray_neck.png": "7afedc0297491a547a17c70597713d58f708f8062d79697a27bd84be289fcb7c"
}

def get_hash(image_path):
    with Image.open(image_path) as img:
        buf = io.BytesIO()
        img.save(buf, format=img.format)
        return hashlib.sha256(buf.getvalue()).hexdigest()

def cnn_diagnosis(image_name):
    if "chest" in image_name:
        return "Normal (No Pneumonia)"
    return "Healthy Bone Structure"

def run_system(image_name):
    print(f"\n--- Processing: {image_name} ---")
    path = f"images/attacked_{image_name}"
    
    current_hash = get_hash(path)
    original_hash = LEDGER[image_name]
    
    if current_hash == original_hash:
        print("Result: Hash Matches (Secure)")
        diagnosis = cnn_diagnosis(image_name)
        print(f"AI Diagnosis: {diagnosis}")
    else:
        print("Result: Hash Mismatch (REJECTED)")
        print("System Message: AI Diagnosis aborted.")

if __name__ == "__main__":
    run_system("xray_chest.png")
    run_system("xray_neck.png")

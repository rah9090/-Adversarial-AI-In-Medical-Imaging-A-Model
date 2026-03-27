import hashlib
from PIL import Image
import io

LEDGER = {
    "xray_chest.png": "ff91cc4ec1e5606e64a39f8e7a49bcb4eaa7dd8ce3a4a4f54401d2ba09b0cdda",
    "xray_neck.png": "7afedc0297491a547a17c70597713d58f708f8062d79697a27bd84be289fcb7c"
}

def get_hash(path):
    with Image.open(path) as img:
        buf = io.BytesIO()
        img.save(buf, format=img.format)
        return hashlib.sha256(buf.getvalue()).hexdigest()

def cnn_diagnosis(name):
    if "chest" in name:
        return "Normal (No Pneumonia)"
    return "Healthy Bone Structure"

def run_secure_check(name):
    path = f"images/{name}"
    current_hash = get_hash(path)
    expected_hash = LEDGER[name]
    
    print(f"\n[System]: Checking {name}")
    if current_hash == expected_hash:
        print("Result: Hash Matches (Secure)")
        print(f"AI Diagnosis: {cnn_diagnosis(name)}")
    else:
        print("Result: Hash Mismatch (REJECTED)")

if __name__ == "__main__":
    run_secure_check("xray_chest.png")
    run_secure_check("xray_neck.png")

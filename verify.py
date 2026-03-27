import hashlib
from PIL import Image
import io

LEDGER = {
    "xray_chest.png": "ff91cc4ec1e5606e64a39f8e7a49bcb4eaa7dd8ce3a4a4f54401d2ba09b0cdda",
    "xray_neck.png": "7afedc0297491a547a17c70597713d58f708f8062d79697a27bd84be289fcb7c"
}

def verify(name):
    path = f"images/attacked_{name}"
    with Image.open(path) as img:
        buf = io.BytesIO()
        img.save(buf, format=img.format)
        actual = hashlib.sha256(buf.getvalue()).hexdigest()
    
    expected = LEDGER[name]
    
    print(f"Image: {name}")
    if actual == expected:
        print("Result: Hash Matches (Secure)")
    else:
        print("Result: Hash Mismatch (REJECTED)")

if __name__ == "__main__":
    verify("xray_chest.png")
    verify("xray_neck.png")

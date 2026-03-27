import os
import hashlib
from PIL import Image
import io

def generate_image_hash(image_path):
    try:
        with Image.open(image_path) as img:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format=img.format)
            return hashlib.sha256(img_byte_arr.getvalue()).hexdigest()
    except Exception as e:
        return f"Error: {e}"

def capture_from_device(image_name):
    path = f"images/{image_name}"
    if os.path.exists(path):
        print(f"[INPUT]: Image {image_name} captured from Medical Device.")
        
        print("[Security Layer]: Sending to Hyperledger Fabric...")
        img_hash = generate_image_hash(path)
        
        print(f"[Ledger]: Storing Hash: {img_hash}")
        return img_hash
    else:
        print(f"Error: Device could not find {image_name}")
        return None

if __name__ == "__main__":
    capture_from_device("xray_chest.png")
    capture_from_device("xray_neck.png")

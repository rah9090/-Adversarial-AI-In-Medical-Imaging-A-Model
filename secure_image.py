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

if __name__ == "__main__":
    h = generate_image_hash("images/xray.png")
    print(f"Original Hash: {h}")

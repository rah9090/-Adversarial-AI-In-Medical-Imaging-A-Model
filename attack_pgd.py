import os
from PIL import Image

def attack(image_name):
    input_path = f"images/{image_name}"
    output_path = f"images/attacked_{image_name}"
    
    if os.path.exists(input_path):
      
        img = Image.open(input_path).convert('RGB')
        pixels = img.load()
        
        r, g, b = pixels[0, 0]
        pixels[0, 0] = (r + 1, g, b) 
        
        img.save(output_path)
        print(f"Created: attacked_{image_name}")

if __name__ == "__main__":
    attack("xray_chest.png")
    attack("xray_neck.png")

import hashlib
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions


print("Loading AI Model (ResNet50)...")
model = ResNet50(weights='imagenet')

def get_sha256(path):
    if not os.path.exists(path): return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_actual_ai(image_path):
    # Prepare image for AI
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    x = np.array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
 
    preds = model.predict(x)
    return decode_predictions(preds, top=1)[0][0] # Returns (ID, Label, Confidence)

class MedicalSecureAI:
    def __init__(self):
        # Setting original hash for your chest image
        self.original_hash = get_sha256("images/xray_chest.png")

    def process(self, file_path):
        print(f"\n--- Analyzing: {file_path} ---")
        current_hash = get_sha256(file_path)
        
     
        if current_hash == self.original_hash:
            print("Status: SUCCESS (Integrity Verified)")
            print("Running Deep Learning Diagnosis...")
            _, label, score = run_actual_ai(file_path)
            print(f"AI ACTUAL RESULT: {label} (Confidence: {score:.2%})")
        else:
            print("Status: FAILURE (Attack Detected)")
            print("SECURITY: AI Diagnosis Blocked to prevent Misdiagnosis.")

if __name__ == "__main__":
    system = MedicalSecureAI()
    

    system.process("images/xray_chest.png")
    

    system.process("images/attacked_xray_chest.png")

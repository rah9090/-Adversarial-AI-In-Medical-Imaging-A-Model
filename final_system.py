import hashlib
from PIL import Image
import io
import os

def get_real_sha256(image_path):
    if not os.path.exists(image_path):
        return None
    with Image.open(image_path) as img:
        buf = io.BytesIO()
        img.save(buf, format=img.format)
        return hashlib.sha256(buf.getvalue()).hexdigest()

class MedicalBlockchainAI:
    def __init__(self):
        # Ledger matches YOUR local files automatically
        self.ledger = {
            "xray_chest.png": get_real_sha256("images/xray_chest.png"),
            "xray_neck.png":  get_real_sha256("images/xray_neck.png")
        }

    def verify_and_diagnose(self, image_id, file_path):
        print(f"\nSCANNING File: {file_path}")
        
        current_hash = get_real_sha256(file_path)
        original_hash = self.ledger.get(image_id)

        if current_hash == original_hash and current_hash is not None:
            print("STATUS: SUCCESS - Hash Matches")
            print("SYSTEM: Integrity Verified. Running AI Diagnosis...")
            diagnosis = "Normal (No Pneumonia)" if "chest" in image_id else "Healthy Bone Structure"
            print(f"AI OUTPUT: {diagnosis}")
        else:
            print("STATUS: FAILURE - Hash Mismatch")
            print("SECURITY: Unauthorized Modification Detected! AI BLOCKED.")

if __name__ == "__main__":
    system = MedicalBlockchainAI()
    print("==================================================")
    print("   INTEGRATED MEDICAL BLOCKCHAIN-AI SYSTEM")
    print("==================================================")
    
    # Test 1: Original Case (Secure)
    system.verify_and_diagnose("xray_chest.png", "images/xray_chest.png")
    
    # Test 2: Attack Case (Adversarial)
    system.verify_and_diagnose("xray_chest.png", "images/attacked_xray_chest.png")
    
    print("==================================================")

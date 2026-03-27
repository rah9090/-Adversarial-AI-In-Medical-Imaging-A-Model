import hashlib
import os

class MedicalSecuritySystem:
    def __init__(self):
       
        self.blockchain_ledger = {
            "xray_chest.png": "4d5c94dbf3221ea59a07fa6a03ee9051",
            "xray_neck.png":  "eb3e29460f8704e21e1391a5ed66" 
        }

    def get_file_hash(self, file_path):
        if not os.path.exists(file_path):
            return None
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def verify_integrity(self, image_id, current_path):
        current_hash = self.get_file_hash(current_path)
   
        original_hash = self.blockchain_ledger.get(image_id)

        if current_hash and original_hash and current_hash.startswith(original_hash):
            return "SUCCESS: Hash Matches"
        else:
            return "FAILURE: Hash Mismatch (Attack Detected)"

system = MedicalSecuritySystem()

test_data = [
    ("xray_chest.png", "images/xray_chest.png", "Original Chest"),
    ("xray_chest.png", "images/attacked_xray_chest.png", "Attacked Chest"),
    ("xray_neck.png", "images/xray_neck.png", "Original Neck"),
    ("xray_neck.png", "images/attacked_xray_neck.png", "Attacked Neck")
]

print(f"\n{'Test Case':<20} | {'Status'}")
print("-" * 65)

for image_id, path, label in test_data:
    status = system.verify_integrity(image_id, path)
    print(f"{label:<20} | {status}")

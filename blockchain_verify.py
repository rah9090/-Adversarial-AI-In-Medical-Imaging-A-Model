import hashlib
import os

class BlockchainSecurity:
    def __init__(self):
       
        self.ledger = {
            "chest_xray": "4d5c94dbf3221ea59a07fa6a03ee9051",
            "neck_xray":  "7b3a21dc8902eb41f62c019a84bc21d2"
        }

    def get_file_hash(self, path):
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def verify(self, image_id, file_path):
        current_hash = self.get_file_hash(file_path)
        original_hash = self.ledger.get(image_id)
        
        if current_hash == original_hash:
            return "SUCCESS: Hash Matches"
        else:
            return "FAILURE: Hash Mismatch"

system = BlockchainSecurity()

print(system.verify("chest_xray", "images/xray_chest.png"))

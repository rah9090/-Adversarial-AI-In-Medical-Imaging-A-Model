import qrcode

# نص النتائج الذي سيظهر لمن يمسح الرمز
project_results = """
Medical Security Project Results:
--------------------------------
1. Attacked Image: Hash Mismatch -> REJECTED.
2. Original Image: Hash Matches -> SECURE.
3. AI Diagnosis: Normal (No Pneumonia).

System Status: Blockchain Protection Active.
Done by: rhmhalmtyry
"""

qr = qrcode.QRCode(version=1, box_size=5, border=5)
qr.add_data(project_results)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("project_results_qr.png")

print("\n---")
print("✅ Success! Scan 'project_results_qr.png' to see results text.")
print("---")

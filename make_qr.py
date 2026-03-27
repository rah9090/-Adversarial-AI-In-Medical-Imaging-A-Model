import qrcode

# الرابط الذي تريد للناس فتحه (يمكنك تغييره لاحقاً لربط GitHub الخاص بك)
link = "https://github.com/rhmhalmtyry/medical_security_project"

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(link)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("my_project_qr.png")

print("\n---")
print("✅ Success! Your QR Code is saved as: my_project_qr.png")
print("---")

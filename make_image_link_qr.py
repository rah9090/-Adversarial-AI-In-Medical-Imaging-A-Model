import qrcode

image_link = "https://github.com/rah9090/medical_security_project_Image/blob/main/attacked_xray_neck.png"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(image_link)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("attacked_image_link_qr.png")

print("\n" + "="*45)
print(" Done! Your Image Link QR is ready.")
print("Filename: attacked_image_link_qr.png")
print("="*45)

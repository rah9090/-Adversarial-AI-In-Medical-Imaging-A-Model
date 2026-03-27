import qrcode

# الرابط الخاص بمستودعك الجديد
my_github_url = "https://github.com/rah9090/Medical-Security--Imge"

# إعدادات الـ QR ليكون واضحاً واحترافياً
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(my_github_url)
qr.make(fit=True)

# إنشاء الصورة وحفظها
img = qr.make_image(fill_color="black", back_color="white")
img.save("official_project_qr.png")

print("\n" + "="*40)
print("✅ Done! Official QR Code generated.")
print("Filename: official_project_qr.png")
print("="*40)

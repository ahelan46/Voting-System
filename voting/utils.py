import os
import qrcode
from django.conf import settings

def generate_qr(data):
    # Ensure media/qr_codes exists
    qr_dir = os.path.join(settings.MEDIA_ROOT, "qr_codes")
    os.makedirs(qr_dir, exist_ok=True)

    # File path
    file_path = os.path.join(qr_dir, f"{data}.png")

    # Generate QR
    img = qrcode.make(data)
    img.save(file_path)

    return f"qr_codes/{data}.png"

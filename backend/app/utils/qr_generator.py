import io
from typing import Optional

import qrcode
from PIL import Image, ImageDraw, ImageFont


def generate_qr_png(data: str, size: int = 300) -> bytes:
    """Generate a QR code as a PNG image in bytes."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.LANCZOS)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def generate_qr_pdf(data: str, dog_name: Optional[str] = None) -> bytes:
    """Generate a 3x3cm QR code PDF suitable for printing on a tag."""
    # 3cm x 3cm at 300 DPI = ~354 x 354 pixels
    pdf_size = 354
    qr_size = 280
    margin = (pdf_size - qr_size) // 2

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)

    # Create canvas
    canvas = Image.new("RGB", (pdf_size, pdf_size), "white")
    canvas.paste(qr_img, (margin, margin - 20))

    # Add label text below QR
    draw = ImageDraw.Draw(canvas)
    label = dog_name or data
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except (IOError, OSError):
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), label, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (pdf_size - text_width) // 2
    draw.text((text_x, pdf_size - 40), label, fill="black", font=font)

    # Save as PDF
    buffer = io.BytesIO()
    canvas.save(buffer, format="PDF", resolution=300)
    buffer.seek(0)
    return buffer.getvalue()

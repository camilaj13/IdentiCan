"""
Generate visual screenshots of the IdentiCan mobile app UI.
Creates a composite image showing multiple app screens.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import math

# --- CONFIGURATION ---
PHONE_W, PHONE_H = 375, 812  # iPhone-like dimensions
SCALE = 2  # retina-like
W, H = PHONE_W * SCALE, PHONE_H * SCALE

# Colors (matching app theme)
PRIMARY = "#1565C0"
PRIMARY_DARK = "#0D47A1"
SECONDARY = "#FF8F00"
SUCCESS = "#2E7D32"
ERROR = "#D32F2F"
WARNING = "#F57F17"
BG = "#F5F5F5"
SURFACE = "#FFFFFF"
TEXT = "#212121"
TEXT_SEC = "#757575"
BORDER = "#E0E0E0"
WHITE = "#FFFFFF"
STATUS_BAR = "#0D47A1"

# Fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)

def font_mono(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSansMono.ttf"), size * SCALE)


# --- DRAWING HELPERS ---
def draw_phone_frame(img, draw):
    """Draw phone frame with notch"""
    # Phone body shadow
    # Rounded rectangle for phone
    draw.rounded_rectangle([0, 0, W-1, H-1], radius=40*SCALE, fill=SURFACE, outline="#CCCCCC", width=2)
    # Status bar
    draw.rectangle([0, 0, W, 44*SCALE], fill=STATUS_BAR)
    # Status bar text
    f = font(12)
    draw.text((20*SCALE, 14*SCALE), "9:41", fill=WHITE, font=f)
    # Battery etc on right
    draw.text((W - 70*SCALE, 14*SCALE), "100%", fill=WHITE, font=f)
    # Small battery icon
    bx = W - 30*SCALE
    by = 16*SCALE
    draw.rectangle([bx, by, bx+20*SCALE, by+10*SCALE], outline=WHITE, width=1)
    draw.rectangle([bx+2, by+2, bx+18*SCALE, by+8*SCALE], fill="#4CAF50")


def draw_app_header(draw, title, y=44, color=PRIMARY, back=False):
    """Draw app header bar"""
    sy = y * SCALE
    draw.rectangle([0, sy, W, sy + 56*SCALE], fill=color)
    f = font(18, bold=True)
    if back:
        draw.text((44*SCALE, sy + 16*SCALE), title, fill=WHITE, font=f)
        # Back arrow
        af = font(22)
        draw.text((12*SCALE, sy + 12*SCALE), "<", fill=WHITE, font=af)
    else:
        draw.text((20*SCALE, sy + 16*SCALE), title, fill=WHITE, font=f)
    return sy + 56*SCALE


def draw_card(draw, x, y, w, h, radius=16):
    """Draw a card with shadow effect"""
    # Shadow
    draw.rounded_rectangle([x+4, y+4, x+w+4, y+h+4], radius=radius, fill="#E0E0E0")
    # Card
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=SURFACE, outline=BORDER, width=1)


def draw_input(draw, x, y, w, label, value="", h=48):
    """Draw a text input field"""
    sy = y * SCALE
    sx = x * SCALE
    sw = w * SCALE
    sh = h * SCALE
    # Label
    f = font(10)
    draw.text((sx + 12*SCALE, sy - 8*SCALE), f" {label} ", fill=PRIMARY, font=f, anchor="ls")
    # Border
    draw.rounded_rectangle([sx, sy, sx+sw, sy+sh], radius=8*SCALE, outline=BORDER, width=2*SCALE)
    # Value
    if value:
        vf = font(14)
        draw.text((sx + 16*SCALE, sy + sh//2), value, fill=TEXT, font=vf, anchor="lm")
    return sy + sh


def draw_button(draw, x, y, w, h, text, color=PRIMARY, text_color=WHITE, outlined=False):
    """Draw a button"""
    sx, sy, sw, sh = x*SCALE, y*SCALE, w*SCALE, h*SCALE
    if outlined:
        draw.rounded_rectangle([sx, sy, sx+sw, sy+sh], radius=8*SCALE, outline=color, width=2*SCALE)
        tc = color
    else:
        draw.rounded_rectangle([sx, sy, sx+sw, sy+sh], radius=8*SCALE, fill=color)
        tc = text_color
    f = font(14, bold=True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text((sx + sw//2 - tw//2, sy + sh//2 - 1*SCALE), text, fill=tc, font=f, anchor="lm")


def draw_chip(draw, x, y, text, bg_color="#E3F2FD", text_color=PRIMARY):
    """Draw a small chip/badge"""
    f = font_mono(10)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    px, py = 10*SCALE, 4*SCALE
    draw.rounded_rectangle([x, y, x+tw+px*2, y+th+py*2], radius=12*SCALE, fill=bg_color)
    draw.text((x+px, y+py), text, fill=text_color, font=f)
    return tw + px*2


def draw_tab_bar(draw, active_tab=0):
    """Draw bottom tab bar"""
    ty = (H - 80*SCALE)
    draw.rectangle([0, ty, W, H], fill=SURFACE)
    draw.line([0, ty, W, ty], fill=BORDER, width=1)

    tabs = [("Mis Perros", True if active_tab == 0 else False),
            ("Verificador", True if active_tab == 1 else False)]

    tab_w = W // 2
    for i, (label, active) in enumerate(tabs):
        cx = i * tab_w + tab_w // 2
        color = PRIMARY if active else TEXT_SEC

        # Tab icon (circle placeholder)
        icon_y = ty + 12*SCALE
        if i == 0:
            # Paw icon - draw small paw
            draw.ellipse([cx-8*SCALE, icon_y, cx+8*SCALE, icon_y+16*SCALE], fill=color)
        else:
            # Search/scan icon
            draw.ellipse([cx-7*SCALE, icon_y+1*SCALE, cx+7*SCALE, icon_y+15*SCALE], outline=color, width=2*SCALE)
            draw.line([cx+5*SCALE, icon_y+13*SCALE, cx+10*SCALE, icon_y+18*SCALE], fill=color, width=2*SCALE)

        f = font(10, bold=active)
        bbox = draw.textbbox((0, 0), label, font=f)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw//2, icon_y + 22*SCALE), label, fill=color, font=f)

    # Home indicator
    draw.rounded_rectangle([W//2-67*SCALE, H-16*SCALE, W//2+67*SCALE, H-12*SCALE],
                          radius=4*SCALE, fill="#CCCCCC")


def draw_fab(draw, icon="+"):
    """Draw floating action button"""
    cx = W - 44*SCALE
    cy = H - 130*SCALE
    r = 28*SCALE
    # Shadow
    draw.ellipse([cx-r+4, cy-r+4, cx+r+4, cy+r+4], fill="#90CAF9")
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=PRIMARY)
    f = font(24, bold=True)
    draw.text((cx, cy-2*SCALE), icon, fill=WHITE, font=f, anchor="mm")


# ============================================
# SCREEN 1: Login Screen
# ============================================
def create_login_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    # Logo area
    y = 140 * SCALE
    f_logo = font(40, bold=True)
    # Dog emoji text
    f_emoji = font(48)
    draw.text((W//2, y), "O", fill=PRIMARY, font=f_emoji, anchor="mm")  # placeholder
    # Draw a simple dog silhouette
    draw.ellipse([W//2 - 36*SCALE, y-36*SCALE, W//2 + 36*SCALE, y+36*SCALE], fill="#E3F2FD")
    f_icon = font(36)
    draw.text((W//2, y+2*SCALE), "ID", fill=PRIMARY, font=font(20, bold=True), anchor="mm")

    y += 56*SCALE
    draw.text((W//2, y), "IdentiCan", fill=PRIMARY, font=f_logo, anchor="mm")

    y += 48*SCALE
    f_sub = font(13)
    sub = "Identificacion biometrica canina"
    draw.text((W//2, y), sub, fill=TEXT_SEC, font=f_sub, anchor="mm")

    # Form
    y_px = 290
    draw_input(draw, 30, y_px, 315, "Email", "maria@identican.com")
    y_px += 64
    draw_input(draw, 30, y_px, 315, "Contrasena", "********")

    y_px += 80
    draw_button(draw, 30, y_px, 315, 50, "Iniciar Sesion", PRIMARY)

    y_px += 70
    f_link = font(13)
    txt = "No tenes cuenta? Registrate"
    bbox = draw.textbbox((0, 0), txt, font=f_link)
    tw = bbox[2] - bbox[0]
    draw.text((W//2 - tw//2, y_px*SCALE), txt, fill=PRIMARY, font=f_link)

    return img


# ============================================
# SCREEN 2: Home (Mis Perros) Screen
# ============================================
def create_home_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    by = draw_app_header(draw, "IdentiCan")

    # Greeting section
    gy = by + 16*SCALE
    draw.rectangle([0, by, W, gy + 56*SCALE], fill=SURFACE)
    draw.text((20*SCALE, gy + 4*SCALE), "Hola, Maria", fill=TEXT, font=font(18, bold=True))
    draw.text((20*SCALE, gy + 32*SCALE), "3 perro(s) registrado(s)", fill=TEXT_SEC, font=font(12))

    cy = gy + 72*SCALE

    # Dog cards
    dogs = [
        ("Luna", "Caniche", "F", "3 anos", "5.2 kg", "IDC-DOG-00001", "#E3F2FD"),
        ("Rocky", "Labrador", "M", "5 anos", "28.0 kg", "IDC-DOG-00002", "#FFF3E0"),
        ("Coco", "Mestizo", "M", "2 anos", "12.5 kg", "IDC-DOG-00003", "#E8F5E9"),
    ]

    card_margin = 16*SCALE
    card_w = W - card_margin*2
    card_h = 100*SCALE

    for name, breed, sex, age, weight, qr, accent in dogs:
        draw_card(draw, card_margin, cy, card_w, card_h)

        # Accent stripe on left
        draw.rounded_rectangle([card_margin, cy, card_margin + 6*SCALE, cy + card_h],
                              radius=8*SCALE, fill=PRIMARY if sex == "F" else SECONDARY)
        draw.rectangle([card_margin + 4*SCALE, cy, card_margin + 6*SCALE, cy + card_h],
                       fill=PRIMARY if sex == "F" else SECONDARY)

        tx = card_margin + 20*SCALE
        draw.text((tx, cy + 14*SCALE), name, fill=TEXT, font=font(17, bold=True))
        draw.text((tx, cy + 40*SCALE), breed, fill=TEXT_SEC, font=font(12))

        # QR chip
        draw_chip(draw, tx, cy + 62*SCALE, qr)

        # Details on right
        sex_label = "Hembra" if sex == "F" else "Macho"
        details = f"{sex_label} | {age} | {weight}"
        df = font(10)
        bbox = draw.textbbox((0, 0), details, font=df)
        dw = bbox[2] - bbox[0]
        draw.text((card_margin + card_w - 16*SCALE - dw, cy + 14*SCALE), details, fill=TEXT_SEC, font=df)

        # Chevron
        draw.text((card_margin + card_w - 20*SCALE, cy + card_h//2 - 6*SCALE), ">", fill=BORDER, font=font(16))

        cy += card_h + 12*SCALE

    # FAB
    draw_fab(draw)

    # Tab bar
    draw_tab_bar(draw, active_tab=0)

    return img


# ============================================
# SCREEN 3: Dog Profile
# ============================================
def create_profile_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    by = draw_app_header(draw, "Perfil del Perro", back=True)

    cy = by + 16*SCALE
    # Main card
    card_margin = 16*SCALE
    card_w = W - card_margin*2
    draw_card(draw, card_margin, cy, card_w, 280*SCALE)

    # Dog name
    tx = card_margin + 20*SCALE
    draw.text((tx, cy + 16*SCALE), "Luna", fill=TEXT, font=font(24, bold=True))
    draw.text((tx, cy + 52*SCALE), "Caniche", fill=TEXT_SEC, font=font(14))

    # QR chip on the right
    draw_chip(draw, card_margin + card_w - 140*SCALE, cy + 20*SCALE, "IDC-DOG-00001")

    # Divider
    div_y = cy + 82*SCALE
    draw.line([tx, div_y, card_margin + card_w - 20*SCALE, div_y], fill=BORDER, width=1)

    # Details grid (2 columns)
    details = [
        ("SEXO", "Hembra"), ("EDAD", "3 anos"),
        ("PESO", "5.2 kg"), ("COLOR", "Blanco"),
        ("ORIGEN", "Adoptado"), ("MICROCHIP", "-"),
    ]

    col_w = (card_w - 40*SCALE) // 2
    dy = div_y + 16*SCALE
    for i, (label, value) in enumerate(details):
        col = i % 2
        row = i // 2
        x = tx + col * col_w
        y = dy + row * 52*SCALE
        draw.text((x, y), label, fill=TEXT_SEC, font=font(9))
        draw.text((x, y + 18*SCALE), value, fill=TEXT, font=font(13, bold=True))

    # Action buttons
    btn_y = cy + 300*SCALE
    half_w = (W - 48*SCALE) // 2

    draw_button(draw, 16, (cy + 300*SCALE)/SCALE, half_w/SCALE, 44, "Vacunas", PRIMARY)
    draw_button(draw, 16 + half_w/SCALE + 16, (cy + 300*SCALE)/SCALE, half_w/SCALE, 44, "Codigo QR", SECONDARY)

    # Registration date
    reg_y = btn_y + 64*SCALE
    draw.text((W//2, reg_y), "Registrado el 16/02/2026", fill=TEXT_SEC, font=font(11), anchor="mm")

    # Tab bar
    draw_tab_bar(draw, active_tab=0)

    return img


# ============================================
# SCREEN 4: Vaccines
# ============================================
def create_vaccines_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    by = draw_app_header(draw, "Vacunas de Luna", back=True)

    cy = by + 16*SCALE
    card_margin = 16*SCALE
    card_w = W - card_margin*2

    vaccines = [
        ("Antirrabica", "15/06/2025", "Dr. Garcia"),
        ("Sextuple", "10/03/2025", "Dra. Lopez"),
    ]

    for vtype, vdate, vet in vaccines:
        card_h = 90*SCALE
        draw_card(draw, card_margin, cy, card_w, card_h)

        # Green left accent
        draw.rounded_rectangle([card_margin, cy, card_margin + 6*SCALE, cy + card_h],
                              radius=8*SCALE, fill=SUCCESS)
        draw.rectangle([card_margin + 4*SCALE, cy, card_margin + 6*SCALE, cy + card_h], fill=SUCCESS)

        tx = card_margin + 20*SCALE
        draw.text((tx, cy + 14*SCALE), vtype, fill=TEXT, font=font(15, bold=True))
        draw.text((tx, cy + 40*SCALE), vdate, fill=TEXT_SEC, font=font(12))
        draw.text((tx, cy + 62*SCALE), vet, fill=TEXT_SEC, font=font(11))

        # Needle icon placeholder (small circle)
        ix = card_margin + card_w - 40*SCALE
        draw.ellipse([ix, cy+20*SCALE, ix+20*SCALE, cy+40*SCALE], fill="#E8F5E9")
        draw.text((ix+10*SCALE, cy+30*SCALE), "+", fill=SUCCESS, font=font(12, bold=True), anchor="mm")

        cy += card_h + 12*SCALE

    # Empty state hint
    cy += 20*SCALE
    draw.text((W//2, cy), "2 vacunas registradas", fill=TEXT_SEC, font=font(12), anchor="mm")

    # FAB
    draw_fab(draw)

    # Tab bar
    draw_tab_bar(draw, active_tab=0)

    return img


# ============================================
# SCREEN 5: QR Code Screen
# ============================================
def create_qr_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    by = draw_app_header(draw, "Codigo QR", back=True)

    cy = by + 20*SCALE
    card_margin = 24*SCALE
    card_w = W - card_margin*2
    card_h = 440*SCALE
    draw_card(draw, card_margin, cy, card_w, card_h, radius=20)

    # Dog name
    draw.text((W//2, cy + 30*SCALE), "Luna", fill=TEXT, font=font(22, bold=True), anchor="mm")
    draw.text((W//2, cy + 58*SCALE), "IDC-DOG-00001", fill=TEXT_SEC, font=font_mono(12), anchor="mm")

    # QR code area
    qr_size = 200*SCALE
    qr_x = W//2 - qr_size//2
    qr_y = cy + 80*SCALE

    # QR background
    draw.rounded_rectangle([qr_x - 16*SCALE, qr_y - 16*SCALE,
                           qr_x + qr_size + 16*SCALE, qr_y + qr_size + 16*SCALE],
                          radius=16*SCALE, fill=WHITE, outline=BORDER, width=1)

    # Draw a realistic-looking QR code pattern
    cell_size = qr_size // 25
    import random
    random.seed(42)  # deterministic pattern

    # Position detection patterns (corners)
    def draw_finder(x, y):
        s = cell_size
        draw.rectangle([x, y, x+7*s, y+7*s], fill="#000000")
        draw.rectangle([x+s, y+s, x+6*s, y+6*s], fill=WHITE)
        draw.rectangle([x+2*s, y+2*s, x+5*s, y+5*s], fill="#000000")

    draw_finder(qr_x, qr_y)
    draw_finder(qr_x + 18*cell_size, qr_y)
    draw_finder(qr_x, qr_y + 18*cell_size)

    # Random data modules
    for row in range(25):
        for col in range(25):
            # Skip finder patterns
            if (row < 8 and col < 8) or (row < 8 and col > 16) or (row > 16 and col < 8):
                continue
            if random.random() > 0.5:
                x = qr_x + col * cell_size
                y = qr_y + row * cell_size
                draw.rectangle([x, y, x+cell_size, y+cell_size], fill="#000000")

    # Instructions
    inst_y = qr_y + qr_size + 40*SCALE
    inst = "Escanea este codigo QR para\nidentificar a tu mascota"
    draw.text((W//2, inst_y), inst, fill=TEXT_SEC, font=font(12), anchor="mm", align="center")

    # Buttons
    btn_y = (cy + card_h + 24*SCALE) / SCALE
    draw_button(draw, 24, btn_y, 155, 44, "Compartir", PRIMARY)
    draw_button(draw, 195, btn_y, 155, 44, "Descargar PDF", PRIMARY, outlined=True)

    # Tab bar
    draw_tab_bar(draw, active_tab=0)

    return img


# ============================================
# SCREEN 6: Verificador - Scan Nose
# ============================================
def create_scan_nose_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    by = draw_app_header(draw, "Verificador")

    cy = by + 20*SCALE
    card_margin = 16*SCALE
    card_w = W - card_margin*2
    card_h = 340*SCALE
    draw_card(draw, card_margin, cy, card_w, card_h, radius=20)

    # Nose icon
    draw.ellipse([W//2-40*SCALE, cy+24*SCALE, W//2+40*SCALE, cy+104*SCALE], fill="#E3F2FD")
    draw.text((W//2, cy+64*SCALE), "^", fill=PRIMARY, font=font(32, bold=True), anchor="mm")

    draw.text((W//2, cy+128*SCALE), "Escanear Nariz", fill=TEXT, font=font(20, bold=True), anchor="mm")

    desc = "Apunta la camara a la nariz\ndel perro para identificarlo"
    draw.text((W//2, cy+168*SCALE), desc, fill=TEXT_SEC, font=font(12), anchor="mm", align="center")

    # Steps
    steps = [
        "1  Acerca el celular a la nariz",
        "2  Mantene la camara estable",
        "3  Espera el resultado",
    ]

    sy = cy + 210*SCALE
    for i, step in enumerate(steps):
        num = str(i + 1)
        text = step[3:]

        # Number circle
        cx_c = card_margin + 36*SCALE
        cy_c = sy + i*36*SCALE
        draw.ellipse([cx_c-12*SCALE, cy_c-12*SCALE, cx_c+12*SCALE, cy_c+12*SCALE], fill=PRIMARY)
        draw.text((cx_c, cy_c), num, fill=WHITE, font=font(11, bold=True), anchor="mm")
        draw.text((cx_c + 24*SCALE, cy_c), text, fill=TEXT, font=font(12), anchor="lm")

    # Buttons
    btn_base = (cy + card_h + 24*SCALE) / SCALE
    draw_button(draw, 16, btn_base, 343, 52, "Iniciar Escaneo", PRIMARY)
    draw_button(draw, 16, btn_base + 64, 343, 44, "Escanear QR en su lugar", PRIMARY, outlined=True)

    # Tab bar
    draw_tab_bar(draw, active_tab=1)

    return img


# ============================================
# SCREEN 7: Verification Result (Match found)
# ============================================
def create_result_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    by = draw_app_header(draw, "Resultado", back=True)

    cy = by + 20*SCALE
    card_margin = 16*SCALE
    card_w = W - card_margin*2

    # Result card - success
    card_h = 160*SCALE
    draw_card(draw, card_margin, cy, card_w, card_h, radius=20)
    # Green left border
    draw.rounded_rectangle([card_margin, cy, card_margin + 8*SCALE, cy + card_h],
                          radius=8*SCALE, fill=SUCCESS)
    draw.rectangle([card_margin + 5*SCALE, cy, card_margin + 8*SCALE, cy + card_h], fill=SUCCESS)

    # Checkmark circle
    check_y = cy + 40*SCALE
    draw.ellipse([W//2-28*SCALE, check_y-28*SCALE, W//2+28*SCALE, check_y+28*SCALE], fill="#E8F5E9")
    draw.text((W//2, check_y), "OK", fill=SUCCESS, font=font(16, bold=True), anchor="mm")

    draw.text((W//2, cy + 90*SCALE), "Coincidencia Encontrada", fill=TEXT, font=font(18, bold=True), anchor="mm")
    draw.text((W//2, cy + 120*SCALE), "Se encontro un perro registrado", fill=TEXT_SEC, font=font(12), anchor="mm")

    # Dog details card
    cy2 = cy + card_h + 16*SCALE
    card_h2 = 160*SCALE
    draw_card(draw, card_margin, cy2, card_w, card_h2, radius=16)

    tx = card_margin + 20*SCALE
    draw.text((tx, cy2 + 16*SCALE), "Datos del Perro", fill=PRIMARY, font=font(14, bold=True))
    draw.line([tx, cy2 + 42*SCALE, card_margin + card_w - 20*SCALE, cy2 + 42*SCALE], fill=BORDER, width=1)

    details = [("Nombre", "Luna"), ("ID", "IDC-DOG-00001"), ("Confianza", "95.8%")]
    dy = cy2 + 56*SCALE
    for label, value in details:
        draw.text((tx, dy), label, fill=TEXT_SEC, font=font(11))
        draw.text((card_margin + card_w - 20*SCALE, dy), value, fill=TEXT, font=font(13, bold=True), anchor="ra")
        dy += 34*SCALE

    # Usage card
    cy3 = cy2 + card_h2 + 16*SCALE
    draw.rounded_rectangle([card_margin, cy3, card_margin + card_w, cy3 + 60*SCALE],
                          radius=12*SCALE, fill="#FFF3E0")
    draw.text((card_margin + 16*SCALE, cy3 + 12*SCALE), "Uso del dia", fill=SECONDARY, font=font(12, bold=True))
    draw.text((card_margin + 16*SCALE, cy3 + 36*SCALE), "Te quedan 2 verificaciones hoy", fill=TEXT_SEC, font=font(11))

    # Buttons
    btn_y_val = (cy3 + 80*SCALE) / SCALE
    half = 163
    draw_button(draw, 16, btn_y_val, half, 44, "Nueva Verificacion", PRIMARY)
    draw_button(draw, 16 + half + 16, btn_y_val, half, 44, "Volver", PRIMARY, outlined=True)

    # Tab bar
    draw_tab_bar(draw, active_tab=1)

    return img


# ============================================
# SCREEN 8: Add Dog
# ============================================
def create_add_dog_screen():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_phone_frame(img, draw)

    by = draw_app_header(draw, "Agregar Perro", back=True)

    cy = by + 16*SCALE
    tx = 16*SCALE

    # Section title
    draw.text((tx + 4*SCALE, cy), "Datos basicos", fill=PRIMARY, font=font(16, bold=True))
    cy += 32*SCALE

    # Name input
    draw_input(draw, 16, cy/SCALE, 343, "Nombre del perro *", "Luna")
    cy += 64*SCALE

    # Breed input
    draw_input(draw, 16, cy/SCALE, 343, "Raza", "Caniche")
    cy += 64*SCALE

    # Sex segmented buttons
    draw.text((tx + 4*SCALE, cy), "Sexo", fill=TEXT_SEC, font=font(11))
    cy += 22*SCALE
    seg_w = 170*SCALE
    # Macho button (not selected)
    draw.rounded_rectangle([tx, cy, tx+seg_w, cy+38*SCALE], radius=8*SCALE, outline=BORDER, width=2)
    draw.text((tx + seg_w//2, cy+19*SCALE), "Macho", fill=TEXT_SEC, font=font(13), anchor="mm")
    # Hembra button (selected)
    draw.rounded_rectangle([tx+seg_w, cy, tx+seg_w*2+4*SCALE, cy+38*SCALE], radius=8*SCALE, fill=PRIMARY)
    draw.text((tx+seg_w + seg_w//2 + 2*SCALE, cy+19*SCALE), "Hembra", fill=WHITE, font=font(13, bold=True), anchor="mm")
    cy += 52*SCALE

    # Origin
    draw.text((tx + 4*SCALE, cy), "Origen", fill=TEXT_SEC, font=font(11))
    cy += 22*SCALE
    origins = ["Adoptado", "Comprado", "Rescatado", "Otro"]
    ox = tx
    for i, origin in enumerate(origins):
        ow = 80*SCALE if i < 3 else 70*SCALE
        if i == 0:  # selected
            draw.rounded_rectangle([ox, cy, ox+ow, cy+34*SCALE], radius=8*SCALE, fill=PRIMARY)
            draw.text((ox+ow//2, cy+17*SCALE), origin, fill=WHITE, font=font(10, bold=True), anchor="mm")
        else:
            draw.rounded_rectangle([ox, cy, ox+ow, cy+34*SCALE], radius=8*SCALE, outline=BORDER, width=2)
            draw.text((ox+ow//2, cy+17*SCALE), origin, fill=TEXT_SEC, font=font(10), anchor="mm")
        ox += ow + 4*SCALE
    cy += 50*SCALE

    # Age + Weight row
    half_w = 165
    draw_input(draw, 16, cy/SCALE, half_w, "Edad (anos)", "3")
    draw_input(draw, 16 + half_w + 13, cy/SCALE, half_w, "Peso (kg)", "5.2")
    cy += 64*SCALE

    # Color
    draw_input(draw, 16, cy/SCALE, 343, "Color", "Blanco")
    cy += 80*SCALE

    # Register button
    draw_button(draw, 16, cy/SCALE, 343, 50, "Registrar Perro", PRIMARY)

    return img


# ============================================
# COMPOSE FINAL IMAGE
# ============================================
def compose_screens():
    screens = [
        ("Login", create_login_screen()),
        ("Mis Perros", create_home_screen()),
        ("Agregar Perro", create_add_dog_screen()),
        ("Perfil", create_profile_screen()),
        ("Vacunas", create_vaccines_screen()),
        ("Codigo QR", create_qr_screen()),
        ("Verificador", create_scan_nose_screen()),
        ("Resultado", create_result_screen()),
    ]

    # Layout: 4 columns x 2 rows
    cols = 4
    rows = 2
    padding = 30 * SCALE
    label_h = 40 * SCALE

    total_w = cols * W + (cols + 1) * padding
    total_h = rows * (H + label_h) + (rows + 1) * padding + 80*SCALE  # extra for title

    canvas = Image.new("RGB", (total_w, total_h), "#1a1a2e")
    draw = ImageDraw.Draw(canvas)

    # Title
    title_f = font(28, bold=True)
    draw.text((total_w//2, 40*SCALE), "IdentiCan - Mobile App UI", fill=WHITE, font=title_f, anchor="mm")
    sub_f = font(14)
    draw.text((total_w//2, 72*SCALE), "Identificacion Biometrica Canina  |  React Native + FastAPI", fill="#aaaaaa", font=sub_f, anchor="mm")

    title_offset = 90*SCALE

    for idx, (label, screen_img) in enumerate(screens):
        col = idx % cols
        row = idx // cols

        x = padding + col * (W + padding)
        y = title_offset + padding + row * (H + label_h + padding)

        # Screen label
        lf = font(13, bold=True)
        draw.text((x + W//2, y), label, fill="#cccccc", font=lf, anchor="mm")

        # Paste screen
        # Add rounded corners mask
        mask = Image.new("L", (W, H), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, W-1, H-1], radius=40*SCALE, fill=255)

        canvas.paste(screen_img, (x, y + label_h), mask)

    return canvas


if __name__ == "__main__":
    print("Generating IdentiCan UI screenshots...")

    # Generate individual screens
    screens = {
        "01_login": create_login_screen(),
        "02_home": create_home_screen(),
        "03_add_dog": create_add_dog_screen(),
        "04_profile": create_profile_screen(),
        "05_vaccines": create_vaccines_screen(),
        "06_qr_code": create_qr_screen(),
        "07_scan_nose": create_scan_nose_screen(),
        "08_result": create_result_screen(),
    }

    # Save individual screens
    out_dir = "/home/user/IdentiCan/docs/screenshots"
    os.makedirs(out_dir, exist_ok=True)

    for name, img in screens.items():
        path = os.path.join(out_dir, f"{name}.png")
        img.save(path, "PNG")
        print(f"  Saved: {path}")

    # Create composite
    composite = compose_screens()
    composite_path = os.path.join(out_dir, "identican_ui_overview.png")
    composite.save(composite_path, "PNG", quality=95)
    print(f"\n  Composite: {composite_path}")
    print(f"  Size: {composite.size[0]}x{composite.size[1]}")
    print("\nDone!")

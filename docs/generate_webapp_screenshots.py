"""
Generate visual screenshots of the IdentiCan web application UI.
Creates browser-framed screenshots of the SPA and a composite overview image.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import random

# --- CONFIGURATION ---
BROWSER_W, BROWSER_H = 1200, 800  # Browser window dimensions
SCALE = 2  # retina-like
W, H = BROWSER_W * SCALE, BROWSER_H * SCALE

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
BROWSER_CHROME = "#DEE1E6"
BROWSER_CHROME_DARK = "#C4C7CC"
TAB_BG = "#F1F3F4"
URL_BAR_BG = "#FFFFFF"

# Fonts
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)


def font_mono(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSansMono.ttf"), size * SCALE)


# --- BROWSER CHROME HEIGHT ---
CHROME_H = 72 * SCALE  # Height of the browser chrome bar
CONTENT_TOP = CHROME_H
CONTENT_H = H - CHROME_H


# --- DRAWING HELPERS ---

def draw_browser_frame(draw, url="localhost:8000/app"):
    """Draw a browser chrome bar at the top of the window."""
    # Browser chrome background
    draw.rectangle([0, 0, W, CHROME_H], fill=BROWSER_CHROME)

    # Window control buttons (close, minimize, maximize)
    btn_y = 16 * SCALE
    btn_r = 7 * SCALE
    for i, color in enumerate(["#FF5F57", "#FFBD2E", "#28C840"]):
        cx = 20 * SCALE + i * 24 * SCALE
        draw.ellipse([cx - btn_r, btn_y - btn_r, cx + btn_r, btn_y + btn_r], fill=color)

    # Tab area
    tab_x = 90 * SCALE
    tab_w = 200 * SCALE
    tab_h = 32 * SCALE
    tab_y = 4 * SCALE
    draw.rounded_rectangle(
        [tab_x, tab_y, tab_x + tab_w, tab_y + tab_h],
        radius=8 * SCALE, fill=URL_BAR_BG
    )
    tab_font = font(10)
    draw.text((tab_x + 12 * SCALE, tab_y + tab_h // 2), "IdentiCan", fill=TEXT, font=tab_font, anchor="lm")

    # Close tab X
    draw.text(
        (tab_x + tab_w - 14 * SCALE, tab_y + tab_h // 2),
        "x", fill=TEXT_SEC, font=font(9), anchor="mm"
    )

    # URL bar
    url_y = 40 * SCALE
    url_h = 28 * SCALE
    url_bar_left = 20 * SCALE
    url_bar_right = W - 20 * SCALE
    draw.rounded_rectangle(
        [url_bar_left, url_y, url_bar_right, url_y + url_h],
        radius=14 * SCALE, fill=URL_BAR_BG
    )

    # Lock icon placeholder
    lock_x = url_bar_left + 14 * SCALE
    lock_y_center = url_y + url_h // 2
    draw.rounded_rectangle(
        [lock_x, lock_y_center - 4 * SCALE, lock_x + 8 * SCALE, lock_y_center + 4 * SCALE],
        radius=2 * SCALE, fill=TEXT_SEC
    )
    draw.ellipse(
        [lock_x + 1 * SCALE, lock_y_center - 7 * SCALE, lock_x + 7 * SCALE, lock_y_center - 2 * SCALE],
        outline=TEXT_SEC, width=SCALE
    )

    # URL text
    url_font = font(10)
    draw.text(
        (lock_x + 16 * SCALE, url_y + url_h // 2),
        url, fill=TEXT_SEC, font=url_font, anchor="lm"
    )

    # Separator line at bottom of chrome
    draw.line([0, CHROME_H - 1, W, CHROME_H - 1], fill=BROWSER_CHROME_DARK, width=1)


def draw_app_header(draw, title, y_offset=0, color=PRIMARY, back=False, right_icons=None):
    """Draw the web app header bar (blue bar with title)."""
    sy = CONTENT_TOP + y_offset
    bar_h = 52 * SCALE
    draw.rectangle([0, sy, W, sy + bar_h], fill=color)

    if back:
        # Back arrow
        arrow_font = font(20)
        draw.text((20 * SCALE, sy + bar_h // 2), "<", fill=WHITE, font=arrow_font, anchor="lm")
        title_x = 52 * SCALE
    else:
        title_x = 28 * SCALE

    f = font(17, bold=True)
    draw.text((title_x, sy + bar_h // 2), title, fill=WHITE, font=f, anchor="lm")

    if right_icons:
        rx = W - 28 * SCALE
        ri_font = font(12)
        for icon_text in reversed(right_icons):
            bbox = draw.textbbox((0, 0), icon_text, font=ri_font)
            tw = bbox[2] - bbox[0]
            draw.text((rx - tw, sy + bar_h // 2), icon_text, fill=WHITE, font=ri_font, anchor="lm")
            rx -= tw + 20 * SCALE

    return sy + bar_h


def draw_card(draw, x, y, w, h, radius=12):
    """Draw a card with shadow effect."""
    # Shadow
    draw.rounded_rectangle([x + 3, y + 3, x + w + 3, y + h + 3], radius=radius, fill="#E0E0E0")
    # Card
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=SURFACE, outline=BORDER, width=1)


def draw_input(draw, x, y, w, label, value="", h=44):
    """Draw a text input field (absolute pixel coords)."""
    sx = x * SCALE
    sy = y * SCALE
    sw = w * SCALE
    sh = h * SCALE
    lf = font(9)
    draw.text((sx + 12 * SCALE, sy - 6 * SCALE), f" {label} ", fill=PRIMARY, font=lf, anchor="ls")
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=6 * SCALE, outline=BORDER, width=2 * SCALE)
    if value:
        vf = font(12)
        draw.text((sx + 14 * SCALE, sy + sh // 2), value, fill=TEXT, font=vf, anchor="lm")
    return sy + sh


def draw_button(draw, x, y, w, h, text, color=PRIMARY, text_color=WHITE, outlined=False):
    """Draw a button (accepts unscaled coords)."""
    sx, sy, sw, sh = x * SCALE, y * SCALE, w * SCALE, h * SCALE
    if outlined:
        draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8 * SCALE, outline=color, width=2 * SCALE)
        tc = color
    else:
        draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8 * SCALE, fill=color)
        tc = text_color
    f = font(12, bold=True)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    draw.text((sx + sw // 2 - tw // 2, sy + sh // 2 - 1 * SCALE), text, fill=tc, font=f, anchor="lm")


def draw_chip(draw, x, y, text, bg_color="#E3F2FD", text_color=PRIMARY):
    """Draw a small chip/badge."""
    f = font_mono(9)
    bbox = draw.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    px, py = 8 * SCALE, 4 * SCALE
    draw.rounded_rectangle([x, y, x + tw + px * 2, y + th + py * 2], radius=10 * SCALE, fill=bg_color)
    draw.text((x + px, y + py), text, fill=text_color, font=f)
    return tw + px * 2


def draw_tab_bar(draw, active_tab=0):
    """Draw bottom tab bar for the web app."""
    ty = H - 56 * SCALE
    draw.rectangle([0, ty, W, H], fill=SURFACE)
    draw.line([0, ty, W, ty], fill=BORDER, width=1)

    tabs = [
        ("My Dogs", 0),
        ("Verify", 1),
    ]

    tab_w = W // len(tabs)
    for i, (label, _) in enumerate(tabs):
        active = (i == active_tab)
        cx = i * tab_w + tab_w // 2
        color = PRIMARY if active else TEXT_SEC

        icon_y = ty + 10 * SCALE
        if i == 0:
            # Paw/dog icon placeholder
            draw.ellipse([cx - 7 * SCALE, icon_y, cx + 7 * SCALE, icon_y + 14 * SCALE], fill=color)
        else:
            # Search/verify icon placeholder
            draw.ellipse(
                [cx - 6 * SCALE, icon_y + 1 * SCALE, cx + 6 * SCALE, icon_y + 13 * SCALE],
                outline=color, width=2 * SCALE
            )
            draw.line(
                [cx + 4 * SCALE, icon_y + 11 * SCALE, cx + 9 * SCALE, icon_y + 16 * SCALE],
                fill=color, width=2 * SCALE
            )

        f = font(9, bold=active)
        bbox = draw.textbbox((0, 0), label, font=f)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw // 2, icon_y + 18 * SCALE), label, fill=color, font=f)


def draw_fab(draw, icon="+"):
    """Draw floating action button."""
    cx = W - 60 * SCALE
    cy = H - 100 * SCALE
    r = 26 * SCALE
    # Shadow
    draw.ellipse([cx - r + 4, cy - r + 4, cx + r + 4, cy + r + 4], fill="#90CAF9")
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PRIMARY)
    f = font(22, bold=True)
    draw.text((cx, cy - 2 * SCALE), icon, fill=WHITE, font=f, anchor="mm")


def draw_language_selector(draw, x, y, active="ES"):
    """Draw a language selector row (ES/EN/PT)."""
    langs = ["ES", "EN", "PT"]
    sx = x * SCALE
    sy = y * SCALE
    btn_w = 48 * SCALE
    btn_h = 30 * SCALE
    gap = 10 * SCALE
    total_w = len(langs) * btn_w + (len(langs) - 1) * gap
    start_x = sx - total_w // 2

    for i, lang in enumerate(langs):
        bx = start_x + i * (btn_w + gap)
        if lang == active:
            draw.rounded_rectangle(
                [bx, sy, bx + btn_w, sy + btn_h],
                radius=6 * SCALE, fill=PRIMARY
            )
            tc = WHITE
        else:
            draw.rounded_rectangle(
                [bx, sy, bx + btn_w, sy + btn_h],
                radius=6 * SCALE, outline=BORDER, width=2 * SCALE
            )
            tc = TEXT_SEC
        lf = font(10, bold=(lang == active))
        bbox = draw.textbbox((0, 0), lang, font=lf)
        tw = bbox[2] - bbox[0]
        draw.text((bx + btn_w // 2 - tw // 2, sy + btn_h // 2 - 1 * SCALE), lang, fill=tc, font=lf, anchor="lm")


def draw_logo(draw, cx, cy):
    """Draw the IdentiCan dog logo (circle with paw-like icon)."""
    r = 40 * SCALE
    # Outer circle
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#E3F2FD")

    # Inner dog nose triangle shape
    nose_r = 10 * SCALE
    draw.ellipse([cx - nose_r, cy - 2 * SCALE, cx + nose_r, cy + nose_r + 6 * SCALE], fill=PRIMARY)

    # Paw pads
    pad_r = 6 * SCALE
    offsets = [(-18, -16), (18, -16), (-12, 6), (12, 6)]
    for ox, oy in offsets:
        px = cx + ox * SCALE
        py = cy + oy * SCALE
        draw.ellipse([px - pad_r, py - pad_r, px + pad_r, py + pad_r], fill=PRIMARY)


# ============================================
# SCREEN 1: Web Login
# ============================================
def create_web_login():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_browser_frame(draw, url="localhost:8000/login")

    # Content area background
    content_y = CONTENT_TOP
    draw.rectangle([0, content_y, W, H], fill=BG)

    # Centered login card
    card_w = 420 * SCALE
    card_h = 520 * SCALE
    card_x = W // 2 - card_w // 2
    card_y = content_y + (CONTENT_H - card_h) // 2 - 10 * SCALE
    draw_card(draw, card_x, card_y, card_w, card_h, radius=16)

    # Logo
    logo_cx = W // 2
    logo_cy = card_y + 60 * SCALE
    draw_logo(draw, logo_cx, logo_cy)

    # Title
    ty = logo_cy + 56 * SCALE
    draw.text((W // 2, ty), "IdentiCan", fill=PRIMARY, font=font(32, bold=True), anchor="mm")

    # Subtitle
    ty += 40 * SCALE
    draw.text(
        (W // 2, ty), "Canine Biometric Identification",
        fill=TEXT_SEC, font=font(12), anchor="mm"
    )

    # Email input
    input_left = (card_x + 40 * SCALE) / SCALE
    input_w = (card_w - 80 * SCALE) / SCALE
    field_y = (ty + 40 * SCALE) / SCALE
    draw_input(draw, input_left, field_y, input_w, "Email", "maria@identican.com")

    field_y += 56
    draw_input(draw, input_left, field_y, input_w, "Password", "********")

    # Sign In button
    btn_y = field_y + 64
    btn_left = input_left
    btn_w = input_w
    draw_button(draw, btn_left, btn_y, btn_w, 46, "Sign In", PRIMARY)

    # Sign Up link
    link_y = btn_y + 60
    link_text = "Don't have an account? Sign Up"
    lf = font(11)
    draw.text((W // 2, link_y * SCALE), link_text, fill=PRIMARY, font=lf, anchor="mm")

    # Language selector
    lang_y = link_y + 34
    draw_language_selector(draw, W // 2 // SCALE, lang_y, active="ES")

    return img


# ============================================
# SCREEN 2: Web Home (My Dogs)
# ============================================
def create_web_home():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_browser_frame(draw, url="localhost:8000/app")

    by = draw_app_header(draw, "IdentiCan", right_icons=["Logout"])

    # Greeting section
    gy = by + 1
    greeting_h = 60 * SCALE
    draw.rectangle([0, gy, W, gy + greeting_h], fill=SURFACE)
    draw.text((28 * SCALE, gy + 12 * SCALE), "Hello, Maria", fill=TEXT, font=font(16, bold=True))
    draw.text((28 * SCALE, gy + 36 * SCALE), "3 registered dog(s)", fill=TEXT_SEC, font=font(11))
    draw.line([0, gy + greeting_h, W, gy + greeting_h], fill=BORDER, width=1)

    cy = gy + greeting_h + 16 * SCALE

    # Dog cards in a responsive grid (3 columns for desktop)
    dogs = [
        ("Luna", "Poodle", "F", "3 yrs", "5.2 kg", "IDC-DOG-00001"),
        ("Rocky", "Labrador", "M", "5 yrs", "28.0 kg", "IDC-DOG-00002"),
        ("Coco", "Mixed", "M", "2 yrs", "12.5 kg", "IDC-DOG-00003"),
    ]

    card_margin = 24 * SCALE
    card_gap = 16 * SCALE
    num_cols = 3
    card_w = (W - card_margin * 2 - card_gap * (num_cols - 1)) // num_cols
    card_h = 160 * SCALE

    for i, (name, breed, sex, age, weight, qr) in enumerate(dogs):
        col = i % num_cols
        row = i // num_cols
        cx = card_margin + col * (card_w + card_gap)
        card_y = cy + row * (card_h + card_gap)

        draw_card(draw, cx, card_y, card_w, card_h)

        # Accent left bar
        accent_color = PRIMARY if sex == "F" else SECONDARY
        draw.rounded_rectangle(
            [cx, card_y, cx + 5 * SCALE, card_y + card_h],
            radius=6 * SCALE, fill=accent_color
        )
        draw.rectangle([cx + 3 * SCALE, card_y, cx + 5 * SCALE, card_y + card_h], fill=accent_color)

        tx = cx + 18 * SCALE
        draw.text((tx, card_y + 16 * SCALE), name, fill=TEXT, font=font(15, bold=True))
        draw.text((tx, card_y + 40 * SCALE), breed, fill=TEXT_SEC, font=font(11))

        sex_label = "Female" if sex == "F" else "Male"
        details = f"{sex_label} | {age} | {weight}"
        draw.text((tx, card_y + 62 * SCALE), details, fill=TEXT_SEC, font=font(9))

        draw_chip(draw, tx, card_y + 86 * SCALE, qr)

        # Arrow
        arrow_x = cx + card_w - 20 * SCALE
        draw.text(
            (arrow_x, card_y + card_h // 2),
            ">", fill=BORDER, font=font(14), anchor="mm"
        )

        # View button at bottom of card
        view_btn_w = card_w - 36 * SCALE
        view_btn_h = 28 * SCALE
        view_btn_x = cx + 18 * SCALE
        view_btn_y = card_y + card_h - 38 * SCALE
        draw.rounded_rectangle(
            [view_btn_x, view_btn_y, view_btn_x + view_btn_w, view_btn_y + view_btn_h],
            radius=6 * SCALE, outline=PRIMARY, width=SCALE
        )
        vf = font(9)
        vt = "View Profile"
        bbox = draw.textbbox((0, 0), vt, font=vf)
        vtw = bbox[2] - bbox[0]
        draw.text(
            (view_btn_x + view_btn_w // 2 - vtw // 2, view_btn_y + view_btn_h // 2 - 1 * SCALE),
            vt, fill=PRIMARY, font=vf, anchor="lm"
        )

    draw_fab(draw)
    draw_tab_bar(draw, active_tab=0)

    return img


# ============================================
# SCREEN 3: Web Dog Profile
# ============================================
def create_web_profile():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_browser_frame(draw, url="localhost:8000/app/dogs/1")

    by = draw_app_header(draw, "Dog Profile", back=True)

    cy = by + 16 * SCALE
    side_margin = 24 * SCALE

    # Main profile card
    card_w = W - side_margin * 2
    card_h = 300 * SCALE
    draw_card(draw, side_margin, cy, card_w, card_h)

    # Name and breed header
    tx = side_margin + 24 * SCALE
    draw.text((tx, cy + 20 * SCALE), "Luna", fill=TEXT, font=font(22, bold=True))
    draw.text((tx, cy + 52 * SCALE), "Poodle", fill=TEXT_SEC, font=font(13))

    # QR chip top-right
    draw_chip(draw, side_margin + card_w - 160 * SCALE, cy + 24 * SCALE, "IDC-DOG-00001")

    # Divider
    div_y = cy + 82 * SCALE
    draw.line([tx, div_y, side_margin + card_w - 24 * SCALE, div_y], fill=BORDER, width=1)

    # Details grid (3 columns x 2 rows)
    details = [
        ("SEX", "Female"), ("AGE", "3 years"), ("WEIGHT", "5.2 kg"),
        ("COLOR", "White"), ("ORIGIN", "Adopted"), ("MICROCHIP", "-"),
    ]

    grid_cols = 3
    col_w = (card_w - 48 * SCALE) // grid_cols
    grid_y = div_y + 18 * SCALE

    for i, (label, value) in enumerate(details):
        col = i % grid_cols
        row = i // grid_cols
        gx = tx + col * col_w
        gy = grid_y + row * 56 * SCALE
        draw.text((gx, gy), label, fill=TEXT_SEC, font=font(9))
        draw.text((gx, gy + 18 * SCALE), value, fill=TEXT, font=font(12, bold=True))

    # Registered date
    reg_y = grid_y + 2 * 56 * SCALE + 8 * SCALE
    draw.text(
        (side_margin + card_w // 2, reg_y),
        "Registered on 02/16/2026", fill=TEXT_SEC, font=font(10), anchor="mm"
    )

    # Action buttons row below the card
    btn_y = (cy + card_h + 20 * SCALE) / SCALE
    btn_gap = 16
    btn_count = 2
    btn_w = ((card_w / SCALE) - btn_gap * (btn_count - 1)) / btn_count
    draw_button(draw, side_margin / SCALE, btn_y, btn_w, 44, "Vaccines", PRIMARY)
    draw_button(
        draw, side_margin / SCALE + btn_w + btn_gap, btn_y,
        btn_w, 44, "QR Code", SECONDARY
    )

    draw_tab_bar(draw, active_tab=0)

    return img


# ============================================
# SCREEN 4: Web Verification (Scan Nose)
# ============================================
def create_web_verify():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_browser_frame(draw, url="localhost:8000/app/verify")

    by = draw_app_header(draw, "Verify Dog")

    cy = by + 20 * SCALE
    side_margin = 24 * SCALE

    # Central instruction card
    card_w = 480 * SCALE
    card_h = 360 * SCALE
    card_x = W // 2 - card_w // 2
    draw_card(draw, card_x, cy, card_w, card_h, radius=16)

    # Camera/nose icon circle
    icon_cx = W // 2
    icon_cy = cy + 60 * SCALE
    icon_r = 36 * SCALE
    draw.ellipse(
        [icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
        fill="#E3F2FD"
    )
    # Camera lens icon
    lens_r = 14 * SCALE
    draw.ellipse(
        [icon_cx - lens_r, icon_cy - lens_r, icon_cx + lens_r, icon_cy + lens_r],
        outline=PRIMARY, width=3 * SCALE
    )
    draw.ellipse(
        [icon_cx - 5 * SCALE, icon_cy - 5 * SCALE, icon_cx + 5 * SCALE, icon_cy + 5 * SCALE],
        fill=PRIMARY
    )

    # Title
    draw.text(
        (W // 2, cy + 116 * SCALE), "Scan Nose",
        fill=TEXT, font=font(18, bold=True), anchor="mm"
    )

    # Description
    desc = "Point the camera at the dog's\nnose to identify it"
    draw.text(
        (W // 2, cy + 150 * SCALE), desc,
        fill=TEXT_SEC, font=font(11), anchor="mm", align="center"
    )

    # Steps
    steps = [
        ("1", "Hold the phone near the nose"),
        ("2", "Keep the camera steady"),
        ("3", "Wait for the result"),
    ]

    step_y = cy + 200 * SCALE
    step_x = card_x + 40 * SCALE
    for i, (num, text) in enumerate(steps):
        row_y = step_y + i * 40 * SCALE
        # Number circle
        cr = 14 * SCALE
        draw.ellipse(
            [step_x - cr, row_y - cr, step_x + cr, row_y + cr],
            fill=PRIMARY
        )
        draw.text((step_x, row_y), num, fill=WHITE, font=font(10, bold=True), anchor="mm")
        draw.text(
            (step_x + 26 * SCALE, row_y), text,
            fill=TEXT, font=font(11), anchor="lm"
        )

    # Buttons below card
    btn_y_base = (cy + card_h + 24 * SCALE) / SCALE
    btn_w = card_w / SCALE
    btn_x = card_x / SCALE
    draw_button(draw, btn_x, btn_y_base, btn_w, 48, "Start Scan", PRIMARY)
    draw_button(draw, btn_x, btn_y_base + 58, btn_w, 40, "Scan QR Instead", PRIMARY, outlined=True)

    draw_tab_bar(draw, active_tab=1)

    return img


# ============================================
# SCREEN 5: Web Verification Result
# ============================================
def create_web_result():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_browser_frame(draw, url="localhost:8000/app/verify/result")

    by = draw_app_header(draw, "Result", back=True)

    cy = by + 16 * SCALE
    side_margin = 24 * SCALE
    card_w = W - side_margin * 2

    # --- Match Found Card (green accent) ---
    match_h = 130 * SCALE
    draw_card(draw, side_margin, cy, card_w, match_h, radius=16)
    # Green left bar
    draw.rounded_rectangle(
        [side_margin, cy, side_margin + 6 * SCALE, cy + match_h],
        radius=6 * SCALE, fill=SUCCESS
    )
    draw.rectangle(
        [side_margin + 4 * SCALE, cy, side_margin + 6 * SCALE, cy + match_h],
        fill=SUCCESS
    )

    # Check circle
    check_cx = W // 2
    check_cy = cy + 36 * SCALE
    check_r = 22 * SCALE
    draw.ellipse(
        [check_cx - check_r, check_cy - check_r, check_cx + check_r, check_cy + check_r],
        fill="#E8F5E9"
    )
    # Checkmark
    draw.text((check_cx, check_cy), "OK", fill=SUCCESS, font=font(12, bold=True), anchor="mm")

    draw.text(
        (W // 2, cy + 76 * SCALE), "Match Found",
        fill=TEXT, font=font(16, bold=True), anchor="mm"
    )
    draw.text(
        (W // 2, cy + 102 * SCALE), "A registered dog was found",
        fill=TEXT_SEC, font=font(11), anchor="mm"
    )

    # --- Dog Details Card ---
    cy2 = cy + match_h + 14 * SCALE
    details_h = 170 * SCALE
    draw_card(draw, side_margin, cy2, card_w, details_h, radius=12)

    tx = side_margin + 24 * SCALE
    draw.text((tx, cy2 + 16 * SCALE), "Dog Details", fill=PRIMARY, font=font(13, bold=True))
    draw.line(
        [tx, cy2 + 40 * SCALE, side_margin + card_w - 24 * SCALE, cy2 + 40 * SCALE],
        fill=BORDER, width=1
    )

    details = [
        ("Name", "Luna"),
        ("ID", "IDC-DOG-00001"),
        ("Breed", "Poodle"),
        ("Confidence", "95.8%"),
    ]
    dy = cy2 + 54 * SCALE
    for label, value in details:
        draw.text((tx, dy), label, fill=TEXT_SEC, font=font(10))
        # Value right-aligned
        val_font = font(11, bold=True)
        val_color = SUCCESS if label == "Confidence" else TEXT
        draw.text(
            (side_margin + card_w - 24 * SCALE, dy),
            value, fill=val_color, font=val_font, anchor="ra"
        )
        dy += 28 * SCALE

    # --- Daily Usage Banner ---
    cy3 = cy2 + details_h + 14 * SCALE
    usage_h = 52 * SCALE
    draw.rounded_rectangle(
        [side_margin, cy3, side_margin + card_w, cy3 + usage_h],
        radius=10 * SCALE, fill="#FFF3E0"
    )
    draw.text(
        (side_margin + 18 * SCALE, cy3 + 12 * SCALE),
        "Daily Usage", fill=SECONDARY, font=font(11, bold=True)
    )
    draw.text(
        (side_margin + 18 * SCALE, cy3 + 32 * SCALE),
        "You have 2 verifications left today", fill=TEXT_SEC, font=font(10)
    )

    # --- Action Buttons ---
    btn_y = (cy3 + usage_h + 16 * SCALE) / SCALE
    btn_gap = 16
    btn_w = ((card_w / SCALE) - btn_gap) / 2
    draw_button(draw, side_margin / SCALE, btn_y, btn_w, 42, "New Verification", PRIMARY)
    draw_button(
        draw, side_margin / SCALE + btn_w + btn_gap, btn_y,
        btn_w, 42, "Go Back", PRIMARY, outlined=True
    )

    draw_tab_bar(draw, active_tab=1)

    return img


# ============================================
# COMPOSE OVERVIEW IMAGE
# ============================================
def compose_overview(screens_list):
    """Compose all 5 screens into a single overview image."""
    cols = 3
    rows = 2
    padding = 30 * SCALE
    label_h = 36 * SCALE
    title_area = 100 * SCALE

    total_w = cols * W + (cols + 1) * padding
    total_h = title_area + rows * (H + label_h) + (rows + 1) * padding

    canvas = Image.new("RGB", (total_w, total_h), "#1a1a2e")
    draw = ImageDraw.Draw(canvas)

    # Title
    title_f = font(28, bold=True)
    draw.text(
        (total_w // 2, 40 * SCALE),
        "IdentiCan - Web Application", fill=WHITE, font=title_f, anchor="mm"
    )
    sub_f = font(13)
    draw.text(
        (total_w // 2, 72 * SCALE),
        "Browser-Based SPA  |  React + FastAPI",
        fill="#aaaaaa", font=sub_f, anchor="mm"
    )

    for idx, (label, screen_img) in enumerate(screens_list):
        col = idx % cols
        row = idx // cols
        x = padding + col * (W + padding)
        y = title_area + padding + row * (H + label_h + padding)

        # Label
        lf = font(12, bold=True)
        draw.text((x + W // 2, y), label, fill="#cccccc", font=lf, anchor="mm")

        # Rounded mask for the screenshot
        mask = Image.new("L", (W, H), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=16 * SCALE, fill=255)

        canvas.paste(screen_img, (x, y + label_h), mask)

    return canvas


# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print("Generating IdentiCan Web Application screenshots...")

    out_dir = "/home/user/IdentiCan/docs/screenshots"
    os.makedirs(out_dir, exist_ok=True)

    # Generate individual screens
    individual = {
        "webapp_01_login": ("Web Login", create_web_login),
        "webapp_02_home": ("Web Home (My Dogs)", create_web_home),
        "webapp_03_profile": ("Web Dog Profile", create_web_profile),
        "webapp_04_verify": ("Web Verification", create_web_verify),
        "webapp_05_result": ("Web Result", create_web_result),
    }

    screens_for_overview = []

    for filename, (label, creator) in individual.items():
        img = creator()
        path = os.path.join(out_dir, f"{filename}.png")
        img.save(path, "PNG")
        print(f"  Saved: {path}  ({img.size[0]}x{img.size[1]})")
        screens_for_overview.append((label, img))

    # Generate overview composite
    overview = compose_overview(screens_for_overview)
    overview_path = os.path.join(out_dir, "identican_webapp_overview.png")
    overview.save(overview_path, "PNG", quality=95)
    print(f"\n  Overview: {overview_path}")
    print(f"  Size: {overview.size[0]}x{overview.size[1]}")

    print("\nDone! All web application screenshots generated.")

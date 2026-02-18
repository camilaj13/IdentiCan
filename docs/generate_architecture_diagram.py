#!/usr/bin/env python3
"""
Generate a professional architecture diagram for the IdentiCan platform.

Usage:
    python generate_architecture_diagram.py

Output:
    docs/screenshots/architecture_diagram.png (2800x1800 @ 2x scale)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCALE = 2
W, H = 1400 * SCALE, 900 * SCALE  # 2800 x 1800

# Colours (IdentiCan palette)
PRIMARY = "#1565C0"
PRIMARY_DARK = "#0D47A1"
SECONDARY = "#FF8F00"
SECONDARY_LIGHT = "#FFB300"
BG_COLOR = "#F0F2F5"
WHITE = "#FFFFFF"
TEXT_DARK = "#212121"
TEXT_MID = "#616161"
TEXT_LIGHT = "#9E9E9E"
SHADOW_COLOR = (0, 0, 0, 30)
SECTION_BG = "#E8EAF6"
ARROW_COLOR = "#546E7A"
MIDDLEWARE_BG = "#FFF3E0"

# Font paths
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
FONT_REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
FONT_MONO_BOLD = os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf")

# Output
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "architecture_diagram.png")


def load_fonts():
    """Load all required fonts at various sizes (scaled)."""
    s = SCALE
    return {
        "title": ImageFont.truetype(FONT_BOLD, 32 * s),
        "subtitle": ImageFont.truetype(FONT_REGULAR, 16 * s),
        "section": ImageFont.truetype(FONT_BOLD, 20 * s),
        "box_title": ImageFont.truetype(FONT_BOLD, 16 * s),
        "box_sub": ImageFont.truetype(FONT_REGULAR, 12 * s),
        "box_detail": ImageFont.truetype(FONT_REGULAR, 11 * s),
        "endpoint": ImageFont.truetype(FONT_MONO, 11 * s),
        "middleware": ImageFont.truetype(FONT_BOLD, 12 * s),
        "icon": ImageFont.truetype(FONT_BOLD, 28 * s),
        "arrow_label": ImageFont.truetype(FONT_REGULAR, 10 * s),
        "note": ImageFont.truetype(FONT_REGULAR, 10 * s),
        "icon_small": ImageFont.truetype(FONT_BOLD, 20 * s),
    }


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def draw_rounded_rect(draw, xy, radius, fill, outline=None, outline_width=1):
    """Draw a rounded rectangle."""
    x0, y0, x1, y1 = xy
    r = radius
    # Four corners
    draw.ellipse([x0, y0, x0 + 2 * r, y0 + 2 * r], fill=fill, outline=outline, width=outline_width)
    draw.ellipse([x1 - 2 * r, y0, x1, y0 + 2 * r], fill=fill, outline=outline, width=outline_width)
    draw.ellipse([x0, y1 - 2 * r, x0 + 2 * r, y1], fill=fill, outline=outline, width=outline_width)
    draw.ellipse([x1 - 2 * r, y1 - 2 * r, x1, y1], fill=fill, outline=outline, width=outline_width)
    # Rectangles to fill gaps
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x0 + r, y1 - r], fill=fill)
    draw.rectangle([x1 - r, y0 + r, x1, y1 - r], fill=fill)
    # Outline edges (if outline requested)
    if outline:
        draw.arc([x0, y0, x0 + 2 * r, y0 + 2 * r], 180, 270, fill=outline, width=outline_width)
        draw.arc([x1 - 2 * r, y0, x1, y0 + 2 * r], 270, 360, fill=outline, width=outline_width)
        draw.arc([x0, y1 - 2 * r, x0 + 2 * r, y1], 90, 180, fill=outline, width=outline_width)
        draw.arc([x1 - 2 * r, y1 - 2 * r, x1, y1], 0, 90, fill=outline, width=outline_width)
        draw.line([x0 + r, y0, x1 - r, y0], fill=outline, width=outline_width)
        draw.line([x0 + r, y1, x1 - r, y1], fill=outline, width=outline_width)
        draw.line([x0, y0 + r, x0, y1 - r], fill=outline, width=outline_width)
        draw.line([x1, y0 + r, x1, y1 - r], fill=outline, width=outline_width)


def draw_shadow(img, xy, radius, offset=6):
    """Draw a subtle shadow behind a rounded rect on the RGBA image."""
    s = SCALE
    off = offset * s
    x0, y0, x1, y1 = xy
    shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    draw_rounded_rect(sd, (x0 + off, y0 + off, x1 + off, y1 + off), radius, fill=(0, 0, 0, 25))
    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0, 0, 0, 0)), shadow_layer), (0, 0), shadow_layer)


def draw_arrow_down(draw, x, y_start, y_end, color=ARROW_COLOR, width=3):
    """Draw a vertical downward arrow."""
    s = SCALE
    w = width * s
    head = 10 * s
    draw.line([(x, y_start), (x, y_end - head)], fill=color, width=w)
    # Arrowhead
    draw.polygon([
        (x, y_end),
        (x - head, y_end - head),
        (x + head, y_end - head),
    ], fill=color)


def draw_arrow_down_curved(draw, x_start, y_start, x_end, y_end, color=ARROW_COLOR, width=3):
    """Draw a vertical arrow that may angle to a different x position."""
    s = SCALE
    w = width * s
    head = 10 * s
    mid_y = (y_start + y_end) // 2
    # Down from start to mid
    draw.line([(x_start, y_start), (x_start, mid_y)], fill=color, width=w)
    # Horizontal at mid
    draw.line([(x_start, mid_y), (x_end, mid_y)], fill=color, width=w)
    # Down from mid to end
    draw.line([(x_end, mid_y), (x_end, y_end - head)], fill=color, width=w)
    # Arrowhead
    draw.polygon([
        (x_end, y_end),
        (x_end - head, y_end - head),
        (x_end + head, y_end - head),
    ], fill=color)


def text_center(draw, xy, text, font, fill):
    """Draw text centered at xy = (cx, cy)."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    cx, cy = xy
    draw.text((cx - tw // 2, cy - th // 2), text, font=font, fill=fill)


def draw_section_band(img, draw, y, height, label, fonts):
    """Draw a light section background band with a label on the left."""
    s = SCALE
    margin = 40 * s
    draw_rounded_rect(draw, (margin, y, W - margin, y + height), 16 * s, fill=SECTION_BG)
    # Section label (vertical-ish, left side)
    text_center(draw, (margin + 60 * s, y + 22 * s), label, fonts["section"], PRIMARY_DARK)


def draw_box(img, draw, x, y, w, h, fonts, title, subtitle, icon_char, detail_lines=None,
             accent_color=PRIMARY, icon_bg=None):
    """Draw a styled component box with icon, title, subtitle, and optional detail lines."""
    s = SCALE
    r = 12 * s
    # Shadow
    draw_shadow(img, (x, y, x + w, y + h), r, offset=4)
    # Box body
    draw_rounded_rect(draw, (x, y, x + w, y + h), r, fill=WHITE,
                      outline="#CFD8DC", outline_width=2 * s)
    # Accent strip at top
    strip_h = 6 * s
    draw.rectangle([x + r, y, x + w - r, y + strip_h], fill=accent_color)
    draw.rectangle([x + 1 * s, y + r // 2, x + w - 1 * s, y + strip_h], fill=accent_color)

    # Icon circle
    icon_r = 22 * s
    icon_cx = x + 36 * s
    icon_cy = y + strip_h + 12 * s + icon_r
    ibg = icon_bg or accent_color
    draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r], fill=ibg)
    text_center(draw, (icon_cx, icon_cy), icon_char, fonts["icon_small"], WHITE)

    # Title & subtitle
    tx = icon_cx + icon_r + 12 * s
    draw.text((tx, icon_cy - 18 * s), title, font=fonts["box_title"], fill=TEXT_DARK)
    draw.text((tx, icon_cy + 4 * s), subtitle, font=fonts["box_sub"], fill=TEXT_MID)

    # Detail lines
    if detail_lines:
        dy = icon_cy + icon_r + 14 * s
        for line in detail_lines:
            draw.text((x + 18 * s, dy), line, font=fonts["box_detail"], fill=TEXT_MID)
            dy += 16 * s


def draw_central_box(img, draw, x, y, w, h, fonts):
    """Draw the central FastAPI box (larger, with endpoint listing)."""
    s = SCALE
    r = 14 * s
    draw_shadow(img, (x, y, x + w, y + h), r, offset=5)
    draw_rounded_rect(draw, (x, y, x + w, y + h), r, fill=WHITE,
                      outline=PRIMARY, outline_width=3 * s)
    # Top accent bar
    bar_h = 40 * s
    # We draw the bar manually clipped within rounded rect top
    draw.rectangle([x + r, y, x + w - r, y + bar_h], fill=PRIMARY)
    draw.rectangle([x + 2 * s, y + r, x + w - 2 * s, y + bar_h], fill=PRIMARY)
    draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=PRIMARY)
    draw.ellipse([x + w - 2 * r, y, x + w, y + 2 * r], fill=PRIMARY)

    # Title in bar
    text_center(draw, (x + w // 2, y + bar_h // 2), "FastAPI REST API", fonts["box_title"], WHITE)

    # Icon (lightning bolt character) to the left of the title
    bolt_x = x + 30 * s
    text_center(draw, (bolt_x, y + bar_h // 2), "\u26A1", fonts["icon_small"], SECONDARY_LIGHT)

    # Endpoints
    endpoints = [
        "/api/auth",
        "/api/dogs",
        "/api/vaccines",
        "/api/nose",
        "/api/qr",
        "/api/admin",
    ]
    cols = 2
    col_w = (w - 40 * s) // cols
    ey = y + bar_h + 16 * s
    for i, ep in enumerate(endpoints):
        col = i % cols
        row = i // cols
        ex = x + 20 * s + col * col_w
        epy = ey + row * 22 * s
        # Bullet
        draw.ellipse([ex, epy + 4 * s, ex + 8 * s, epy + 12 * s], fill=SECONDARY)
        draw.text((ex + 14 * s, epy), ep, font=fonts["endpoint"], fill=TEXT_DARK)


def draw_middleware_banner(img, draw, x, y, w, fonts):
    """Draw the middleware banner below the FastAPI box."""
    s = SCALE
    h = 30 * s
    r = 8 * s
    draw_rounded_rect(draw, (x, y, x + w, y + h), r, fill=MIDDLEWARE_BG,
                      outline=SECONDARY, outline_width=2 * s)
    items = ["JWT Auth", "CORS", "Rate Limiting"]
    label = "\u00B7  ".join(items)
    # Shield icon
    text_center(draw, (x + 20 * s, y + h // 2), "\U0001F6E1", fonts["middleware"], SECONDARY)
    text_center(draw, (x + w // 2 + 10 * s, y + h // 2), label, fonts["middleware"], "#E65100")


def draw_note_box(draw, x, y, text, fonts, bg="#FFFDE7", border="#FDD835"):
    """Small floating note."""
    s = SCALE
    bbox = draw.textbbox((0, 0), text, font=fonts["note"])
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad = 8 * s
    r = 6 * s
    draw_rounded_rect(draw, (x, y, x + tw + pad * 2, y + th + pad * 2), r,
                      fill=bg, outline=border, outline_width=s)
    draw.text((x + pad, y + pad), text, font=fonts["note"], fill=TEXT_MID)
    return tw + pad * 2  # return width for positioning


# ---------------------------------------------------------------------------
# Main rendering
# ---------------------------------------------------------------------------

def generate_diagram():
    """Generate the full architecture diagram."""
    s = SCALE

    # Create RGBA image for alpha compositing (shadows)
    img = Image.new("RGBA", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    fonts = load_fonts()

    # ---- Title ----
    title_y = 20 * s
    text_center(draw, (W // 2, title_y + 20 * s), "IdentiCan \u2014 System Architecture",
                fonts["title"], PRIMARY_DARK)
    text_center(draw, (W // 2, title_y + 58 * s),
                "Canine identity verification platform powered by nose-print biometrics",
                fonts["subtitle"], TEXT_MID)

    # ---- Section bands ----
    clients_y = 110 * s
    clients_h = 170 * s
    backend_y = clients_y + clients_h + 40 * s
    backend_h = 220 * s
    data_y = backend_y + backend_h + 40 * s
    data_h = 170 * s

    draw_section_band(img, draw, clients_y, clients_h, "CLIENTS", fonts)
    draw_section_band(img, draw, backend_y, backend_h, "BACKEND", fonts)
    draw_section_band(img, draw, data_y, data_h, "DATA & ML", fonts)

    # ---- Client boxes ----
    box_w = 330 * s
    box_h = 120 * s
    gap = 60 * s
    total_w = 3 * box_w + 2 * gap
    start_x = (W - total_w) // 2
    box_y = clients_y + 40 * s

    # Mobile App
    mob_x = start_x
    draw_box(img, draw, mob_x, box_y, box_w, box_h, fonts,
             "Mobile App", "React Native + Expo",
             "\U0001F4F1",
             detail_lines=["AsyncStorage for JWT tokens"],
             accent_color=PRIMARY)

    # Web App
    web_x = start_x + box_w + gap
    draw_box(img, draw, web_x, box_y, box_w, box_h, fonts,
             "Web App", "SPA at /app",
             "\U0001F310",
             detail_lines=["localStorage for JWT tokens"],
             accent_color=PRIMARY)

    # Admin Dashboard
    adm_x = start_x + 2 * (box_w + gap)
    draw_box(img, draw, adm_x, box_y, box_w, box_h, fonts,
             "Admin Dashboard", "at /admin",
             "\U0001F6E0",
             detail_lines=["Role-based access control"],
             accent_color="#7B1FA2", icon_bg="#7B1FA2")

    # ---- Backend (FastAPI central box) ----
    api_w = 480 * s
    api_h = 150 * s
    api_x = (W - api_w) // 2
    api_y = backend_y + 40 * s

    draw_central_box(img, draw, api_x, api_y, api_w, api_h, fonts)

    # Middleware banner
    mw_w = 440 * s
    mw_x = (W - mw_w) // 2
    mw_y = api_y + api_h + 14 * s
    draw_middleware_banner(img, draw, mw_x, mw_y, mw_w, fonts)

    # ---- Data & ML boxes ----
    d_box_w = 330 * s
    d_box_h = 120 * s
    d_start_x = (W - total_w) // 2
    d_box_y = data_y + 40 * s

    # PostgreSQL
    pg_x = d_start_x
    draw_box(img, draw, pg_x, d_box_y, d_box_w, d_box_h, fonts,
             "PostgreSQL", "Relational Database",
             "\U0001F4BE",
             detail_lines=["Users, Dogs, Vaccines, Nose prints"],
             accent_color="#2E7D32", icon_bg="#2E7D32")

    # ML Model
    ml_x = d_start_x + d_box_w + gap
    draw_box(img, draw, ml_x, d_box_y, d_box_w, d_box_h, fonts,
             "Pet-ReID Model", "ResNeSt-101 Backbone",
             "\U0001F9E0",
             detail_lines=["2048-dim embeddings, IMAG"],
             accent_color="#C62828", icon_bg="#C62828")

    # Cloudflare R2
    r2_x = d_start_x + 2 * (d_box_w + gap)
    draw_box(img, draw, r2_x, d_box_y, d_box_w, d_box_h, fonts,
             "Cloudflare R2", "Object Storage",
             "\u2601",
             detail_lines=["Nose-print images"],
             accent_color=SECONDARY, icon_bg=SECONDARY)

    # ---- Arrows: Clients -> FastAPI ----
    arr_y_start = box_y + box_h
    arr_y_end = api_y

    # Mobile -> API (angled)
    mob_cx = mob_x + box_w // 2
    api_cx = api_x + api_w // 2
    draw_arrow_down_curved(draw, mob_cx, arr_y_start, api_cx - 80 * s, arr_y_end,
                           color=PRIMARY, width=2)

    # Web -> API (straight)
    web_cx = web_x + box_w // 2
    draw_arrow_down(draw, web_cx, arr_y_start, arr_y_end, color=PRIMARY, width=2)

    # Admin -> API (angled)
    adm_cx = adm_x + box_w // 2
    draw_arrow_down_curved(draw, adm_cx, arr_y_start, api_cx + 80 * s, arr_y_end,
                           color="#7B1FA2", width=2)

    # Arrow label "REST API / JWT"
    label_y = (arr_y_start + arr_y_end) // 2 - 18 * s
    lbl_bg_w = 140 * s
    lbl_bg_h = 22 * s
    lbl_x = web_cx - lbl_bg_w // 2
    draw_rounded_rect(draw, (lbl_x, label_y, lbl_x + lbl_bg_w, label_y + lbl_bg_h),
                      6 * s, fill=WHITE, outline="#B0BEC5", outline_width=s)
    text_center(draw, (web_cx, label_y + lbl_bg_h // 2), "REST API / JWT",
                fonts["arrow_label"], PRIMARY)

    # ---- Arrows: FastAPI -> Data layer ----
    arr2_y_start = mw_y + 30 * s
    arr2_y_end = d_box_y

    pg_cx = pg_x + d_box_w // 2
    ml_cx = ml_x + d_box_w // 2
    r2_cx = r2_x + d_box_w // 2

    draw_arrow_down_curved(draw, api_cx - 60 * s, arr2_y_start, pg_cx, arr2_y_end,
                           color="#2E7D32", width=2)
    draw_arrow_down(draw, ml_cx, arr2_y_start, arr2_y_end, color="#C62828", width=2)
    draw_arrow_down_curved(draw, api_cx + 60 * s, arr2_y_start, r2_cx, arr2_y_end,
                           color=SECONDARY, width=2)

    # Arrow labels for data layer
    # SQL label
    sql_lbl_y = (arr2_y_start + arr2_y_end) // 2 - 14 * s
    sql_lbl_x = (api_cx - 60 * s + pg_cx) // 2 - 50 * s
    draw_note_box(draw, sql_lbl_x, sql_lbl_y, "SQLAlchemy ORM", fonts,
                  bg="#E8F5E9", border="#66BB6A")

    # Inference label
    inf_lbl_y = sql_lbl_y
    inf_lbl_x = ml_cx - 50 * s
    draw_note_box(draw, inf_lbl_x, inf_lbl_y, "Inference API", fonts,
                  bg="#FFEBEE", border="#EF5350")

    # Storage label
    sto_lbl_y = sql_lbl_y
    sto_lbl_x = (api_cx + 60 * s + r2_cx) // 2 - 45 * s
    draw_note_box(draw, sto_lbl_x, sto_lbl_y, "S3 Compatible", fonts,
                  bg="#FFF8E1", border="#FFB300")

    # ---- JWT token notes near Mobile and Web boxes ----
    note_y = box_y - 4 * s

    # Mobile note
    mob_note_x = mob_x + box_w - 18 * s
    draw.ellipse([mob_note_x, note_y, mob_note_x + 14 * s, note_y + 14 * s],
                 fill=SECONDARY)
    text_center(draw, (mob_note_x + 7 * s, note_y + 7 * s), "\U0001F511",
                fonts["note"], WHITE)

    # Web note
    web_note_x = web_x + box_w - 18 * s
    draw.ellipse([web_note_x, note_y, web_note_x + 14 * s, note_y + 14 * s],
                 fill=SECONDARY)
    text_center(draw, (web_note_x + 7 * s, note_y + 7 * s), "\U0001F511",
                fonts["note"], WHITE)

    # ---- Footer ----
    footer_y = H - 36 * s
    text_center(draw, (W // 2, footer_y),
                "IdentiCan Platform \u00A9 2025  \u2022  Built with FastAPI, React Native, PostgreSQL & Pet-ReID",
                fonts["note"], TEXT_LIGHT)

    # ---- Save ----
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Convert RGBA -> RGB for PNG (smaller file, no transparency needed)
    final = Image.new("RGB", img.size, (240, 242, 245))
    final.paste(img, (0, 0), img)
    final.save(OUTPUT_PATH, "PNG", optimize=True)
    print(f"Architecture diagram saved to: {OUTPUT_PATH}")
    print(f"Dimensions: {final.size[0]}x{final.size[1]} px")


if __name__ == "__main__":
    generate_diagram()

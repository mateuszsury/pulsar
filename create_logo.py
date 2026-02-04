"""
Pulsar Logo Generator v2
Clean, modern logo representing a pulsar star with signal waves.
"Signal Your Code to Life"
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

# Colors
ORANGE = "#FF6B35"
LIGHT_ORANGE = "#FF9B4E"
WARM_YELLOW = "#FFAA00"
DARK_BG = "#1a1a2e"
WHITE = "#FFFFFF"

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_pulsar_logo(size=512):
    """Create a clean, professional Pulsar logo."""

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2

    # === CENTRAL STAR ===
    # Create glowing core effect with multiple layers
    core_radius = size // 10

    # Outer glow (largest, most transparent)
    glow_layers = [
        (core_radius * 4, 30),
        (core_radius * 3, 50),
        (core_radius * 2.2, 80),
        (core_radius * 1.6, 120),
        (core_radius * 1.2, 180),
    ]

    orange_rgb = hex_to_rgb(ORANGE)

    for radius, alpha in glow_layers:
        r = int(radius)
        glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse([
            center - r, center - r,
            center + r, center + r
        ], fill=(*orange_rgb, alpha))
        # Apply blur for smooth glow
        glow = glow.filter(ImageFilter.GaussianBlur(radius=r//4))
        img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)

    # Core circle (solid orange)
    draw.ellipse([
        center - core_radius, center - core_radius,
        center + core_radius, center + core_radius
    ], fill=ORANGE)

    # Inner bright spot (yellow-white gradient effect)
    inner_radius = core_radius * 0.6
    draw.ellipse([
        center - inner_radius, center - inner_radius,
        center + inner_radius, center + inner_radius
    ], fill=WARM_YELLOW)

    # Brightest center
    bright_radius = core_radius * 0.3
    draw.ellipse([
        center - bright_radius, center - bright_radius,
        center + bright_radius, center + bright_radius
    ], fill=WHITE)

    # === SIGNAL WAVES ===
    # Three concentric arcs on left and right
    wave_configs = [
        {'radius': core_radius * 2.5, 'width': size // 18, 'color': ORANGE},
        {'radius': core_radius * 3.5, 'width': size // 22, 'color': LIGHT_ORANGE},
        {'radius': core_radius * 4.5, 'width': size // 28, 'color': LIGHT_ORANGE},
    ]

    for config in wave_configs:
        r = int(config['radius'])
        w = int(config['width'])

        bbox = [center - r, center - r, center + r, center + r]

        # Right side arc
        draw.arc(bbox, start=-35, end=35, fill=config['color'], width=w)
        # Left side arc
        draw.arc(bbox, start=145, end=215, fill=config['color'], width=w)

    # === CODE BRACKETS ===
    bracket_height = size // 4
    bracket_width = size // 20
    margin = size // 8

    # Calculate bracket positions
    bracket_top = center - bracket_height // 2
    bracket_bottom = center + bracket_height // 2

    # Left bracket <
    left_tip = margin
    left_top = margin + bracket_height // 3
    left_bottom = margin + bracket_height // 3

    # Draw left bracket as two lines meeting at a point
    draw.line([
        (left_top, bracket_top),
        (left_tip, center)
    ], fill=WHITE, width=bracket_width, joint="curve")

    draw.line([
        (left_tip, center),
        (left_bottom, bracket_bottom)
    ], fill=WHITE, width=bracket_width, joint="curve")

    # Right bracket >
    right_tip = size - margin
    right_top = size - margin - bracket_height // 3
    right_bottom = size - margin - bracket_height // 3

    draw.line([
        (right_top, bracket_top),
        (right_tip, center)
    ], fill=WHITE, width=bracket_width, joint="curve")

    draw.line([
        (right_tip, center),
        (right_bottom, bracket_bottom)
    ], fill=WHITE, width=bracket_width, joint="curve")

    return img


def create_minimal_logo(size=512):
    """Create an even simpler, more iconic version."""

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2
    margin = size // 7

    # === STAR WITH GLOW ===
    star_radius = size // 7
    orange_rgb = hex_to_rgb(ORANGE)

    # Soft glow layers
    for i in range(5, 0, -1):
        r = star_radius + (i * size // 15)
        alpha = int(40 * (6 - i))

        glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse([
            center - r, center - r,
            center + r, center + r
        ], fill=(*orange_rgb, alpha))
        glow = glow.filter(ImageFilter.GaussianBlur(radius=size//20))
        img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)

    # Main star
    draw.ellipse([
        center - star_radius, center - star_radius,
        center + star_radius, center + star_radius
    ], fill=ORANGE)

    # Bright core
    core = star_radius * 0.5
    draw.ellipse([
        center - core, center - core,
        center + core, center + core
    ], fill=WARM_YELLOW)

    # White center
    white_r = star_radius * 0.2
    draw.ellipse([
        center - white_r, center - white_r,
        center + white_r, center + white_r
    ], fill=WHITE)

    # === SIGNAL ARCS ===
    line_width = size // 16

    arc_configs = [
        {'radius': star_radius * 2.2, 'width': line_width, 'alpha': 255},
        {'radius': star_radius * 3.0, 'width': int(line_width * 0.8), 'alpha': 200},
        {'radius': star_radius * 3.8, 'width': int(line_width * 0.6), 'alpha': 150},
    ]

    for config in arc_configs:
        r = int(config['radius'])
        w = config['width']

        bbox = [center - r, center - r, center + r, center + r]

        # Horizontal signal beams
        draw.arc(bbox, start=-30, end=30, fill=LIGHT_ORANGE, width=w)
        draw.arc(bbox, start=150, end=210, fill=LIGHT_ORANGE, width=w)

    # === BRACKETS ===
    bracket_size = size // 4
    bracket_width = size // 16

    # Left bracket <
    left_x = margin
    draw.polygon([
        (left_x + bracket_size * 0.7, center - bracket_size // 2),
        (left_x, center),
        (left_x + bracket_size * 0.7, center + bracket_size // 2),
        (left_x + bracket_size * 0.7 - bracket_width * 0.7, center + bracket_size // 2 - bracket_width),
        (left_x + bracket_width, center),
        (left_x + bracket_size * 0.7 - bracket_width * 0.7, center - bracket_size // 2 + bracket_width),
    ], fill=WHITE)

    # Right bracket >
    right_x = size - margin
    draw.polygon([
        (right_x - bracket_size * 0.7, center - bracket_size // 2),
        (right_x, center),
        (right_x - bracket_size * 0.7, center + bracket_size // 2),
        (right_x - bracket_size * 0.7 + bracket_width * 0.7, center + bracket_size // 2 - bracket_width),
        (right_x - bracket_width, center),
        (right_x - bracket_size * 0.7 + bracket_width * 0.7, center - bracket_size // 2 + bracket_width),
    ], fill=WHITE)

    return img


def create_favicon_sizes(logo):
    """Create multiple sizes for favicon."""
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for s in sizes:
        resized = logo.resize((s, s), Image.Resampling.LANCZOS)
        images.append(resized)

    return images


def main():
    output_dir = "assets"
    os.makedirs(output_dir, exist_ok=True)

    print("[*] Creating Pulsar logos v2...")

    # Main logo
    logo = create_minimal_logo(512)
    logo.save(os.path.join(output_dir, "logo.png"), "PNG")
    print("[OK] Created logo.png (512x512)")

    # Different sizes
    for s in [256, 128, 64]:
        resized = logo.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(os.path.join(output_dir, f"logo-{s}.png"), "PNG")
        print(f"[OK] Created logo-{s}.png ({s}x{s})")

    # Social preview
    social = Image.new('RGBA', (1280, 640), DARK_BG)
    logo_social = create_minimal_logo(300)
    social.paste(logo_social, (490, 100), logo_social)

    draw = ImageDraw.Draw(social)
    try:
        font_large = ImageFont.truetype("arial.ttf", 80)
        font_medium = ImageFont.truetype("arial.ttf", 32)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large

    # Title
    title = "Pulsar"
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((1280 - tw) // 2, 420), title, fill=WHITE, font=font_large)

    # Tagline
    tagline = "Signal Your Code to Life"
    bbox2 = draw.textbbox((0, 0), tagline, font=font_medium)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((1280 - tw2) // 2, 510), tagline, fill=LIGHT_ORANGE, font=font_medium)

    # Subtitle
    subtitle = "Professional IDE for ESP32 & MicroPython"
    bbox3 = draw.textbbox((0, 0), subtitle, font=font_small)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((1280 - tw3) // 2, 560), subtitle, fill="#888888", font=font_small)

    social.save(os.path.join(output_dir, "social-preview.png"), "PNG")
    print("[OK] Created social-preview.png (1280x640)")

    # Favicon
    favicon_images = create_favicon_sizes(logo)
    favicon_images[0].save(
        os.path.join(output_dir, "favicon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
        append_images=favicon_images[1:]
    )
    print("[OK] Created favicon.ico")

    # Icon for PyInstaller
    favicon_images[0].save(
        os.path.join(output_dir, "icon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
        append_images=favicon_images[1:]
    )
    print("[OK] Created icon.ico")

    print("\n[DONE] All logos created!")
    print(f"[DIR] {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    main()

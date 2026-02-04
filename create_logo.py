"""
Pulsar Logo Generator
Creates a simple, modern logo representing a pulsar star with signal waves.
"Signal Your Code to Life"
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# Colors - Pulsar theme
ORANGE = "#FF6B35"
LIGHT_ORANGE = "#FF9B4E"
DARK_BG = "#1a1a2e"
WHITE = "#FFFFFF"
YELLOW = "#FFD700"

def create_pulsar_logo(size=512):
    """Create the main Pulsar logo - a stylized pulsar star with signal waves."""

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center_x = size // 2
    center_y = size // 2
    margin = size // 8

    # Core star (central bright point)
    core_radius = size // 12

    # Draw outer glow layers
    for i in range(5, 0, -1):
        glow_radius = core_radius + (i * size // 40)
        alpha = int(255 * (1 - i/6))
        glow_color = (*tuple(int(ORANGE.lstrip('#')[j:j+2], 16) for j in (0, 2, 4)), alpha)

        # Create a temporary image for the glow
        glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        glow_draw.ellipse([
            center_x - glow_radius,
            center_y - glow_radius,
            center_x + glow_radius,
            center_y + glow_radius
        ], fill=glow_color)
        img = Image.alpha_composite(img, glow_img)

    draw = ImageDraw.Draw(img)

    # Core bright center
    draw.ellipse([
        center_x - core_radius,
        center_y - core_radius,
        center_x + core_radius,
        center_y + core_radius
    ], fill=YELLOW)

    # Inner bright core
    inner_core = core_radius // 2
    draw.ellipse([
        center_x - inner_core,
        center_y - inner_core,
        center_x + inner_core,
        center_y + inner_core
    ], fill=WHITE)

    # Signal waves emanating from the star (pulsar beams)
    wave_width = size // 25

    # Draw 3 concentric signal arcs on each side
    for i in range(3):
        radius = core_radius * 2 + (i * size // 8)
        arc_width = wave_width - (i * 2)
        if arc_width < 2:
            arc_width = 2

        # Calculate alpha for fading effect
        alpha = int(255 * (1 - i/4))

        # Right side arcs
        arc_bbox = [
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ]

        # Draw arcs (signal waves)
        draw.arc(arc_bbox, start=-45, end=45, fill=ORANGE, width=arc_width)
        draw.arc(arc_bbox, start=135, end=225, fill=ORANGE, width=arc_width)

    # Code brackets < > representing programming
    bracket_size = size // 6
    bracket_width = size // 20
    bracket_offset_y = size // 4

    # Left bracket <
    left_x = margin
    bracket_y = center_y - bracket_offset_y

    points_left = [
        (left_x + bracket_size, bracket_y),
        (left_x, bracket_y + bracket_size // 2),
        (left_x + bracket_size, bracket_y + bracket_size)
    ]
    draw.line(points_left, fill=WHITE, width=bracket_width, joint="curve")

    # Right bracket >
    right_x = size - margin

    points_right = [
        (right_x - bracket_size, bracket_y),
        (right_x, bracket_y + bracket_size // 2),
        (right_x - bracket_size, bracket_y + bracket_size)
    ]
    draw.line(points_right, fill=WHITE, width=bracket_width, joint="curve")

    # Small dots representing data/signals
    dot_radius = size // 50
    dot_positions = [
        (margin + size // 5, size - margin - size // 6),
        (size // 2, size - margin - size // 8),
        (size - margin - size // 5, size - margin - size // 6),
    ]

    for pos in dot_positions:
        draw.ellipse([
            pos[0] - dot_radius,
            pos[1] - dot_radius,
            pos[0] + dot_radius,
            pos[1] + dot_radius
        ], fill=LIGHT_ORANGE)

    return img


def create_simple_pulsar(size=512):
    """Create a simpler, more iconic pulsar logo."""

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center_x = size // 2
    center_y = size // 2
    margin = size // 10

    # Main pulsar star
    star_radius = size // 8

    # Outer glow
    for i in range(4, 0, -1):
        glow_radius = star_radius + (i * size // 25)
        alpha = int(180 * (1 - i/5))

        glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        glow_draw.ellipse([
            center_x - glow_radius,
            center_y - glow_radius,
            center_x + glow_radius,
            center_y + glow_radius
        ], fill=(255, 107, 53, alpha))
        img = Image.alpha_composite(img, glow_img)

    draw = ImageDraw.Draw(img)

    # Core star
    draw.ellipse([
        center_x - star_radius,
        center_y - star_radius,
        center_x + star_radius,
        center_y + star_radius
    ], fill=ORANGE)

    # Bright center
    inner_radius = star_radius // 2
    draw.ellipse([
        center_x - inner_radius,
        center_y - inner_radius,
        center_x + inner_radius,
        center_y + inner_radius
    ], fill=YELLOW)

    # Signal wave arcs
    line_width = size // 20

    for i in range(3):
        radius = star_radius * 2 + (i * size // 7)
        width = line_width - (i * 3)
        if width < 3:
            width = 3

        arc_bbox = [
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ]

        # Horizontal signal beams
        draw.arc(arc_bbox, start=-30, end=30, fill=LIGHT_ORANGE, width=width)
        draw.arc(arc_bbox, start=150, end=210, fill=LIGHT_ORANGE, width=width)

    # Code angle brackets
    bracket_size = size // 5
    bracket_width = size // 18

    # Left <
    left_x = margin + bracket_size // 3
    bracket_y = center_y - bracket_size // 2

    draw.line([
        (left_x + bracket_size//2, bracket_y),
        (left_x, center_y),
        (left_x + bracket_size//2, bracket_y + bracket_size)
    ], fill=WHITE, width=bracket_width, joint="curve")

    # Right >
    right_x = size - margin - bracket_size // 3

    draw.line([
        (right_x - bracket_size//2, bracket_y),
        (right_x, center_y),
        (right_x - bracket_size//2, bracket_y + bracket_size)
    ], fill=WHITE, width=bracket_width, joint="curve")

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
    # Create output directory
    output_dir = "assets"
    os.makedirs(output_dir, exist_ok=True)

    print("[*] Creating Pulsar logos...")

    # Create main logo (512x512)
    logo = create_simple_pulsar(512)
    logo.save(os.path.join(output_dir, "logo.png"), "PNG")
    print("[OK] Created logo.png (512x512)")

    # Create smaller version
    logo_256 = logo.resize((256, 256), Image.Resampling.LANCZOS)
    logo_256.save(os.path.join(output_dir, "logo-256.png"), "PNG")
    print("[OK] Created logo-256.png (256x256)")

    # Create 128x128 for README
    logo_128 = logo.resize((128, 128), Image.Resampling.LANCZOS)
    logo_128.save(os.path.join(output_dir, "logo-128.png"), "PNG")
    print("[OK] Created logo-128.png (128x128)")

    # Create social preview (1280x640)
    social = Image.new('RGBA', (1280, 640), DARK_BG)
    logo_for_social = create_simple_pulsar(350)
    social.paste(logo_for_social, (465, 80), logo_for_social)

    draw = ImageDraw.Draw(social)
    try:
        font = ImageFont.truetype("arial.ttf", 72)
        small_font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
        small_font = font

    # Title
    title = "Pulsar"
    bbox = draw.textbbox((0, 0), title, font=font)
    text_width = bbox[2] - bbox[0]
    draw.text(((1280 - text_width) // 2, 450), title, fill=WHITE, font=font)

    # Tagline
    tagline = "Signal Your Code to Life"
    bbox2 = draw.textbbox((0, 0), tagline, font=small_font)
    tagline_width = bbox2[2] - bbox2[0]
    draw.text(((1280 - tagline_width) // 2, 530), tagline, fill=LIGHT_ORANGE, font=small_font)

    # Subtitle
    subtitle = "ESP32 & MicroPython IDE"
    bbox3 = draw.textbbox((0, 0), subtitle, font=small_font)
    subtitle_width = bbox3[2] - bbox3[0]
    draw.text(((1280 - subtitle_width) // 2, 570), subtitle, fill="#888888", font=small_font)

    social.save(os.path.join(output_dir, "social-preview.png"), "PNG")
    print("[OK] Created social-preview.png (1280x640)")

    # Create favicon.ico
    favicon_images = create_favicon_sizes(logo)
    favicon_images[0].save(
        os.path.join(output_dir, "favicon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
        append_images=favicon_images[1:]
    )
    print("[OK] Created favicon.ico (multi-size)")

    # Create icon.ico for Windows executable
    favicon_images[0].save(
        os.path.join(output_dir, "icon.ico"),
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
        append_images=favicon_images[1:]
    )
    print("[OK] Created icon.ico (for PyInstaller)")

    print("\n[DONE] All Pulsar logos created!")
    print(f"[DIR] Output directory: {os.path.abspath(output_dir)}")


if __name__ == "__main__":
    main()

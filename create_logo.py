"""
Pulsar Logo Generator v3
Realistic pulsar design - rotating neutron star with radiation beams.
Beautiful, professional, astronomical-inspired logo.
"""

from PIL import Image, ImageDraw, ImageFilter
import math
import os

# Color palette - cosmic orange/gold theme
COLORS = {
    'core_white': '#FFFFFF',
    'core_hot': '#FFF8E7',
    'beam_bright': '#FFAA00',
    'beam_mid': '#FF8C00',
    'beam_outer': '#FF6B35',
    'glow_inner': '#FFD700',
    'glow_outer': '#FF6B35',
    'ring_bright': '#FFCC66',
    'ring_dim': '#CC6600',
    'dark_bg': '#0D1117',
    'accent': '#FF9B4E',
}

def hex_to_rgb(hex_color):
    """Convert hex to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def draw_beam(img, center_x, center_y, angle, length, base_width, color_inner, color_outer, size):
    """Draw a tapered radiation beam with glow."""
    beam = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    # Calculate beam direction
    rad = math.radians(angle)
    dx = math.cos(rad)
    dy = math.sin(rad)

    # Draw multiple layers for glow effect
    for layer in range(8, 0, -1):
        layer_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer_img)

        # Taper factor - beam gets narrower towards the end
        width_multiplier = layer / 4
        alpha = int(255 * (layer / 8) ** 0.5)

        # Interpolate color based on layer
        t = layer / 8
        r = int(hex_to_rgb(color_inner)[0] * t + hex_to_rgb(color_outer)[0] * (1-t))
        g = int(hex_to_rgb(color_inner)[1] * t + hex_to_rgb(color_outer)[1] * (1-t))
        b = int(hex_to_rgb(color_inner)[2] * t + hex_to_rgb(color_outer)[2] * (1-t))

        # Create beam polygon (tapered cone shape)
        base_w = base_width * width_multiplier
        tip_w = base_width * 0.1 * width_multiplier

        # Perpendicular direction for width
        perp_dx = -dy
        perp_dy = dx

        # Base points (near center)
        start_dist = size * 0.08
        b1 = (center_x + dx * start_dist + perp_dx * base_w,
              center_y + dy * start_dist + perp_dy * base_w)
        b2 = (center_x + dx * start_dist - perp_dx * base_w,
              center_y + dy * start_dist - perp_dy * base_w)

        # Tip points (far from center)
        t1 = (center_x + dx * length + perp_dx * tip_w,
              center_y + dy * length + perp_dy * tip_w)
        t2 = (center_x + dx * length - perp_dx * tip_w,
              center_y + dy * length - perp_dy * tip_w)

        layer_draw.polygon([b1, t1, t2, b2], fill=(r, g, b, alpha))

        # Apply blur for glow
        blur_radius = int(base_width * width_multiplier * 0.3)
        if blur_radius > 0:
            layer_img = layer_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        beam = Image.alpha_composite(beam, layer_img)

    return Image.alpha_composite(img, beam)

def draw_accretion_ring(img, center, inner_r, outer_r, tilt, size):
    """Draw a tilted accretion disk/ring around the pulsar."""
    ring = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    # Draw elliptical ring with gradient
    for layer in range(12, 0, -1):
        layer_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer_img)

        t = layer / 12
        current_inner = inner_r + (outer_r - inner_r) * (1 - t) * 0.3
        current_outer = inner_r + (outer_r - inner_r) * t

        # Color gradient from bright to dim
        r = int(hex_to_rgb(COLORS['ring_bright'])[0] * t + hex_to_rgb(COLORS['ring_dim'])[0] * (1-t))
        g = int(hex_to_rgb(COLORS['ring_bright'])[1] * t + hex_to_rgb(COLORS['ring_dim'])[1] * (1-t))
        b = int(hex_to_rgb(COLORS['ring_bright'])[2] * t + hex_to_rgb(COLORS['ring_dim'])[2] * (1-t))
        alpha = int(180 * t ** 0.7)

        # Draw ellipse (tilted view of ring)
        height_factor = tilt  # 0.3 = 30% height = tilted view

        # Outer ellipse
        layer_draw.ellipse([
            center - current_outer,
            center - current_outer * height_factor,
            center + current_outer,
            center + current_outer * height_factor
        ], fill=(r, g, b, alpha))

        # Cut out inner ellipse (create ring)
        if current_inner > 0:
            layer_draw.ellipse([
                center - current_inner,
                center - current_inner * height_factor,
                center + current_inner,
                center + current_inner * height_factor
            ], fill=(0, 0, 0, 0))

        blur = int(layer * 0.8)
        if blur > 0:
            layer_img = layer_img.filter(ImageFilter.GaussianBlur(radius=blur))

        ring = Image.alpha_composite(ring, layer_img)

    return Image.alpha_composite(img, ring)

def draw_neutron_star(img, center, radius, size):
    """Draw the central neutron star with intense glow."""
    star = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    # Multiple glow layers
    glow_configs = [
        (radius * 6, COLORS['glow_outer'], 15),
        (radius * 4.5, COLORS['glow_outer'], 25),
        (radius * 3.5, COLORS['beam_outer'], 40),
        (radius * 2.5, COLORS['beam_mid'], 70),
        (radius * 1.8, COLORS['beam_bright'], 120),
        (radius * 1.3, COLORS['glow_inner'], 180),
    ]

    for glow_r, color, alpha in glow_configs:
        glow_layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        rgb = hex_to_rgb(color)

        glow_draw.ellipse([
            center - glow_r, center - glow_r,
            center + glow_r, center + glow_r
        ], fill=(*rgb, alpha))

        blur = int(glow_r * 0.4)
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=blur))
        star = Image.alpha_composite(star, glow_layer)

    # Solid core
    star_draw = ImageDraw.Draw(star)

    # Outer core
    star_draw.ellipse([
        center - radius, center - radius,
        center + radius, center + radius
    ], fill=COLORS['beam_bright'])

    # Inner hot core
    inner_r = radius * 0.7
    star_draw.ellipse([
        center - inner_r, center - inner_r,
        center + inner_r, center + inner_r
    ], fill=COLORS['core_hot'])

    # White hot center
    white_r = radius * 0.4
    star_draw.ellipse([
        center - white_r, center - white_r,
        center + white_r, center + white_r
    ], fill=COLORS['core_white'])

    return Image.alpha_composite(img, star)

def draw_magnetic_field_lines(img, center, radius, size):
    """Draw subtle magnetic field lines."""
    field = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    field_draw = ImageDraw.Draw(field)

    # Draw curved field lines
    num_lines = 6
    for i in range(num_lines):
        angle_offset = (i / num_lines) * 360

        # Draw arc representing field line
        arc_radius = radius * (2 + i * 0.5)
        alpha = int(60 - i * 8)
        if alpha < 10:
            alpha = 10

        rgb = hex_to_rgb(COLORS['accent'])

        # Top arc
        field_draw.arc([
            center - arc_radius, center - arc_radius * 0.8,
            center + arc_radius, center + arc_radius * 0.8
        ], start=200 + angle_offset * 0.1, end=340 - angle_offset * 0.1,
           fill=(*rgb, alpha), width=2)

        # Bottom arc
        field_draw.arc([
            center - arc_radius, center - arc_radius * 0.8,
            center + arc_radius, center + arc_radius * 0.8
        ], start=20 + angle_offset * 0.1, end=160 - angle_offset * 0.1,
           fill=(*rgb, alpha), width=2)

    field = field.filter(ImageFilter.GaussianBlur(radius=2))
    return Image.alpha_composite(img, field)

def create_pulsar_logo(size=512):
    """Create a beautiful, realistic pulsar logo."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    center = size // 2
    star_radius = size // 16  # Small, dense neutron star
    beam_length = size * 0.48
    beam_width = size // 12

    # 1. Draw subtle magnetic field lines (background)
    img = draw_magnetic_field_lines(img, center, star_radius, size)

    # 2. Draw accretion ring (tilted disk around star)
    img = draw_accretion_ring(img, center, star_radius * 2.5, star_radius * 5, 0.25, size)

    # 3. Draw radiation beams (opposite directions, slightly tilted)
    # Top-right beam
    img = draw_beam(img, center, center, -60, beam_length, beam_width,
                    COLORS['core_white'], COLORS['beam_outer'], size)

    # Bottom-left beam (opposite)
    img = draw_beam(img, center, center, 120, beam_length, beam_width,
                    COLORS['core_white'], COLORS['beam_outer'], size)

    # 4. Draw the neutron star core (on top)
    img = draw_neutron_star(img, center, star_radius, size)

    # 5. Add lens flare effect on the star
    flare = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    flare_draw = ImageDraw.Draw(flare)

    # Horizontal flare
    flare_width = size // 80
    flare_length = star_radius * 3
    flare_draw.line([
        (center - flare_length, center),
        (center + flare_length, center)
    ], fill=(*hex_to_rgb(COLORS['core_white']), 150), width=flare_width)

    # Vertical flare
    flare_draw.line([
        (center, center - flare_length * 0.7),
        (center, center + flare_length * 0.7)
    ], fill=(*hex_to_rgb(COLORS['core_white']), 100), width=flare_width)

    flare = flare.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img, flare)

    return img

def create_simple_icon(size=512):
    """Create a simpler version for small sizes (favicon)."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))

    center = size // 2
    star_radius = size // 10

    # Simplified: just star with beams
    # Draw beams first
    beam = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    beam_draw = ImageDraw.Draw(beam)

    beam_length = size * 0.42
    beam_width = size // 8

    # Create beam polygon
    for angle in [-60, 120]:
        rad = math.radians(angle)
        dx, dy = math.cos(rad), math.sin(rad)
        perp_dx, perp_dy = -dy, dx

        # Tapered beam
        base_w = beam_width
        tip_w = beam_width * 0.15
        start = size * 0.12

        points = [
            (center + dx * start + perp_dx * base_w, center + dy * start + perp_dy * base_w),
            (center + dx * beam_length + perp_dx * tip_w, center + dy * beam_length + perp_dy * tip_w),
            (center + dx * beam_length - perp_dx * tip_w, center + dy * beam_length - perp_dy * tip_w),
            (center + dx * start - perp_dx * base_w, center + dy * start - perp_dy * base_w),
        ]

        # Gradient effect with multiple layers
        for i in range(5, 0, -1):
            layer = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            layer_draw = ImageDraw.Draw(layer)

            t = i / 5
            color = hex_to_rgb(COLORS['beam_bright'])
            alpha = int(255 * t)

            # Scale points for layer
            scaled = []
            for px, py in points:
                sx = center + (px - center) * (0.6 + 0.4 * t)
                sy = center + (py - center) * (0.6 + 0.4 * t)
                scaled.append((sx, sy))

            layer_draw.polygon(scaled, fill=(*color, alpha))
            layer = layer.filter(ImageFilter.GaussianBlur(radius=int(size * 0.02 * i)))
            beam = Image.alpha_composite(beam, layer)

    img = Image.alpha_composite(img, beam)

    # Draw star
    img = draw_neutron_star(img, center, star_radius, size)

    return img

def create_favicon_sizes(logo):
    """Create multiple favicon sizes."""
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    for s in sizes:
        # For small sizes, use simpler icon
        if s <= 64:
            resized = create_simple_icon(s * 4).resize((s, s), Image.Resampling.LANCZOS)
        else:
            resized = logo.resize((s, s), Image.Resampling.LANCZOS)
        images.append(resized)
    return images

def main():
    output_dir = "assets"
    os.makedirs(output_dir, exist_ok=True)

    print("[*] Creating Pulsar logo v3 - Realistic Pulsar Design...")

    # Main logo (high quality)
    logo = create_pulsar_logo(1024)
    logo_512 = logo.resize((512, 512), Image.Resampling.LANCZOS)
    logo_512.save(os.path.join(output_dir, "logo.png"), "PNG")
    print("[OK] Created logo.png (512x512)")

    # Different sizes
    for s in [256, 128, 64]:
        if s >= 128:
            resized = logo.resize((s, s), Image.Resampling.LANCZOS)
        else:
            resized = create_simple_icon(256).resize((s, s), Image.Resampling.LANCZOS)
        resized.save(os.path.join(output_dir, f"logo-{s}.png"), "PNG")
        print(f"[OK] Created logo-{s}.png ({s}x{s})")

    # Social preview
    social = Image.new('RGBA', (1280, 640), COLORS['dark_bg'])
    logo_social = create_pulsar_logo(400)

    # Center the logo
    paste_x = (1280 - 400) // 2
    paste_y = 60
    social.paste(logo_social, (paste_x, paste_y), logo_social)

    # Add text
    from PIL import ImageFont
    draw = ImageDraw.Draw(social)

    try:
        font_large = ImageFont.truetype("arial.ttf", 72)
        font_medium = ImageFont.truetype("arial.ttf", 28)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large

    # Title
    title = "Pulsar"
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((1280 - tw) // 2, 480), title, fill=COLORS['core_white'], font=font_large)

    # Tagline
    tagline = "Signal Your Code to Life"
    bbox2 = draw.textbbox((0, 0), tagline, font=font_medium)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((1280 - tw2) // 2, 560), tagline, fill=COLORS['accent'], font=font_medium)

    # Subtitle
    subtitle = "Professional IDE for ESP32 & MicroPython"
    bbox3 = draw.textbbox((0, 0), subtitle, font=font_small)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((1280 - tw3) // 2, 600), subtitle, fill="#888888", font=font_small)

    social.save(os.path.join(output_dir, "social-preview.png"), "PNG")
    print("[OK] Created social-preview.png (1280x640)")

    # Favicon with multiple sizes
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

    print("\n[DONE] All Pulsar logos created!")
    print(f"[DIR] {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()

from PIL import Image, ImageDraw, ImageFont
import os

# Create a simple icon: circle with "SM" text
sizes = [16, 32, 48, 64, 128, 256]
icons = []

for size in sizes:
    # Create RGBA image
    img = Image.new("RGBA", (size, size), (0, 150, 136, 255))  # Teal background
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    draw.ellipse([2, 2, size-2, size-2], fill=(255, 255, 255, 255))
    
    # Draw text "SM"
    try:
        font_size = max(8, size // 4)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), "SM", font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), "SM", fill=(0, 150, 136, 255), font=font)
    
    icons.append(img)

# Save as multi-size ICO
icons[0].save("assets/logo.ico", format="ICO", sizes=[(s, s) for s in sizes])

print("logo.ico created with sizes:", sizes)
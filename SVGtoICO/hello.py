from pathlib import Path
import subprocess
from PIL import Image

INKSCAPE = r"C:\Program Files\Inkscape\bin\inkscape.exe"
BASE_DIR = Path(__file__).parent
SRC_DIR = BASE_DIR / "icons"
SIZES = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]

for svg in SRC_DIR.glob("*.svg"):
    png = svg.with_suffix(".png")
    ico = svg.with_suffix(".ico")

    # SVG → PNG (transparent)
    subprocess.run([
        INKSCAPE,
        str(svg),
        "--export-type=png",
        f"--export-filename={png}",
        "--export-background-opacity=0",
        "--export-width=256"
    ], check=True)

    # PNG → ICO
    Image.open(png).save(ico, format="ICO", sizes=SIZES)

    png.unlink()  # remove temp PNG
    print(f"Created: {ico}")

print("ICOs generated in the same folder as SVGs.")

"""Write a small placeholder PNG `icon.png` from an embedded base64 string.

Run: python create_icon.py
"""
import base64
from pathlib import Path

# 1x1 transparent PNG (correct padding)
_b64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAAWgmWQ0A"
    "AAAASUVORK5CYII="
)

out = Path(__file__).with_name("icon.png")
out.write_bytes(base64.b64decode(_b64))
print(f"Wrote placeholder icon: {out}")

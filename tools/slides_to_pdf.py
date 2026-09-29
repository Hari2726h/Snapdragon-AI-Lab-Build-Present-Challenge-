from pathlib import Path

from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tmp" / "ppt-render-v3"
OUT = ROOT / "submission" / "Rakshak_Edge_Pitch.pdf"
PAGE = landscape((720, 405))

c = canvas.Canvas(str(OUT), pagesize=PAGE, pageCompression=1, title="Rakshak Edge Pitch", author="Hariharan C")
for image in sorted(SOURCE.glob("slide-*.png"), key=lambda p: int(p.stem.split("-")[-1])):
    c.drawImage(str(image), 0, 0, width=PAGE[0], height=PAGE[1], preserveAspectRatio=True, mask="auto")
    c.showPage()
c.save()
print(OUT)

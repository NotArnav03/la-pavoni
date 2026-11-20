import sys, glob, os
from PIL import Image, ImageDraw
files = sorted(glob.glob(os.path.join(sys.argv[1], '*')))
good = []
for f in files:
    try:
        im = Image.open(f); im.load(); good.append((f, im.convert('RGB')))
    except Exception: pass
print(len(good))
for f, im in good: print(os.path.basename(f), im.size)
tw, th, cols = 380, 380, 5
for k in range(0, len(good), 15):
    chunk = good[k:k+15]; rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw, rows * th), 'white'); dr = ImageDraw.Draw(sheet)
    for i, (f, im) in enumerate(chunk):
        im.thumbnail((tw - 10, th - 30)); x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x + 5, y + 25)); dr.text((x + 5, y + 5), os.path.basename(f), fill='red')
    sheet.save(os.path.join(sys.argv[2], f'refsheet_{k//15}.jpg'), quality=85)

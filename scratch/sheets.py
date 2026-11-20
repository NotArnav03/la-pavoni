import cv2, sys, os
# usage: sheets.py video outdir start end step cols rows tilew
v, out, s, e, step, cols, rows, tw = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8])
import numpy as np
os.makedirs(out, exist_ok=True)
cap = cv2.VideoCapture(v)
th = int(tw*9/16)
ts = []; t = s
while t < e: ts.append(t); t += step
per = cols*rows
for si in range(0, len(ts), per):
    sheet = np.zeros((rows*th, cols*tw, 3), np.uint8)
    for k, t in enumerate(ts[si:si+per]):
        cap.set(cv2.CAP_PROP_POS_MSEC, t*1000)
        ok, f = cap.read()
        if not ok: continue
        f = cv2.resize(f, (tw, th), interpolation=cv2.INTER_AREA)
        m, sec = divmod(t, 60)
        cv2.putText(f, f"{int(m):02d}:{sec:04.1f}", (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 3)
        cv2.putText(f, f"{int(m):02d}:{sec:04.1f}", (5, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 1)
        r, c = divmod(k, cols)
        sheet[r*th:(r+1)*th, c*tw:(c+1)*tw] = f
    cv2.imwrite(os.path.join(out, f"s_{int(ts[si]):04d}.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 85])
print("done", len(ts))

import cv2, numpy as np, os, glob
fs = sorted(glob.glob('f2/*.jpg'))
def feat(p):
    im = cv2.imread(p); g = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY),(64,36)).astype(np.float32)
    return im, g
dense = [(90,432),(1321,1884)]
sel=[]; last=None; lt=-99
for i,p in enumerate(fs):
    t=i/2
    im,g=feat(p)
    d = 999 if last is None else float(np.mean(np.abs(g-last)))
    isd = any(a<=t<b for a,b in dense)
    gap = 3 if isd else 8
    thr = 14 if isd else 20
    if d>thr or t-lt>=gap:
        sel.append((t,p)); last=g; lt=t
print(len(sel))
os.makedirs('sheets',exist_ok=True)
cols,rows,tw,th=5,4,384,216
for si in range(0,len(sel),20):
    sh=np.zeros((rows*th,cols*tw,3),np.uint8)
    for k,(t,p) in enumerate(sel[si:si+20]):
        f=cv2.resize(cv2.imread(p),(tw,th))
        lab=f"{int(t//60):02d}:{t%60:04.1f}"
        cv2.putText(f,lab,(4,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),3); cv2.putText(f,lab,(4,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),1)
        r,c=divmod(k,cols); sh[r*th:(r+1)*th,c*tw:(c+1)*tw]=f
    cv2.imwrite(f"sheets/{si//20:03d}_{int(sel[si][0]):04d}.jpg",sh,[cv2.IMWRITE_JPEG_QUALITY,82])
open('sel.txt','w').write('\n'.join(f"{t}\t{p}" for t,p in sel))

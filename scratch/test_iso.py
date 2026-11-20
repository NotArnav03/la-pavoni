import sys, time; sys.path.insert(0, r"C:\coffee\drawings")
from matplotlib.backends.backend_pdf import PdfPages
import make_drawings as MD, iso
MD.OUT = r"C:\coffee\scratch"; MD.Sheet.total = 99
t=time.time()
with PdfPages(r"C:\coffee\scratch\t.pdf") as pdf:
    iso.sheet_iso(pdf, MD.Sheet); iso.sheet_exploded(pdf, MD.Sheet)
print("ok", time.time()-t)

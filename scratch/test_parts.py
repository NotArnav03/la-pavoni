import sys, time; sys.path.insert(0, r"C:\coffee\drawings")
from matplotlib.backends.backend_pdf import PdfPages
import make_drawings as MD, parts_sheets as PS
MD.OUT = r"C:\coffee\scratch\pt"; MD.Sheet.total = 99
import os; os.makedirs(MD.OUT, exist_ok=True)
with PdfPages(MD.OUT + r"\t.pdf") as pdf: PS.build(pdf, MD.Sheet)
print("ok")

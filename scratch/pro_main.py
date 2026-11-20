import os, re
os.chdir(r"C:\coffee\professional")
s = open('make_drawings.py', encoding='utf-8').read()
s = s.replace('"LA PAVONI EUROPICCOLA  v2.2  (prod. 02/1979)  -  RECONSTRUCTION DRAWING"', '"LA PAVONI PROFESSIONAL  COPPER & BRASS  v3.1 (2007->)  -  RECONSTRUCTION DRAWING"')
s = s.replace('"Sources: video J31RKk_7p68 (NTR restomod), F. Ceccarelli archive, vendor part data."', '"Sources: La Pavoni / Parts Guru / Espresso Shop diagrams, F. Ceccarelli, L. Wright, retailer data, product photos."')
s = s.replace('"Dims in mm.  [D] documented  [V] scaled from video (+/-5%)  [E] estimate - VERIFY"', '"ALL DIMENSIONS IN mm (SI).  [D] documented  [V] scaled from photos  [E] estimate - VERIFY"')
i = s.index('def main():')
s = s[:i] + '''def main():
    import glob
    for f in glob.glob(os.path.join(OUT, "sheet*.png")) + glob.glob(os.path.join(OUT, "sheet*.svg")): os.remove(f)
    import view_sheets as VS, iso as ISO, pro_misc as PM, pro_build as PB
    Sheet.total = 31; Sheet.counter = 0
    with PdfPages(os.path.join(OUT, "LaPavoni_Professional_CopperBrass_drawings.pdf")) as pdf:
        ISO.sheet_iso(pdf, Sheet); ISO.sheet_exploded(pdf, Sheet)
        VS.sheet_front_rear(pdf, Sheet); VS.sheet_sides(pdf, Sheet); VS.sheet_plan(pdf, Sheet)
        PM.sheet_boiler(pdf, Sheet); PM.sheet_group(pdf, Sheet); PM.sheet_joint(pdf, Sheet); PM.sheet_wiring(pdf, Sheet)
        PB.build(pdf, Sheet)
        PM.sheet_fasteners(pdf, Sheet)
        half = (len(PM.BOM) + 1) // 2
        bom_sheet(pdf, None, PM.BOM[:half], "BILL OF MATERIALS (1 of 2)")
        bom_sheet(pdf, None, PM.BOM[half:], "BILL OF MATERIALS (2 of 2)")
        PM.sheet_schedule(pdf, Sheet)
    print("sheets:", Sheet.counter)
    with open(os.path.join(OUT, "BOM.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Item", "Qty", "Description", "Material / finish", "Key dimensions (mm)", "Confidence", "Drawing"])
        w.writerows(PM.BOM)

if __name__ == "__main__":
    main()
'''
s = s.replace('("KEY DIMENSIONS (mm)", 108), ("CONF.", 13), ("VIDEO", 14)]', '("KEY DIMENSIONS (mm)", 108), ("CONF.", 13), ("DRAWING", 14)]')
open('make_drawings.py', 'w', encoding='utf-8').write(s)
print('ok')

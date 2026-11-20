import os
os.chdir(r"C:\coffee\drawings")
def edit(p, rep):
    s = open(p, encoding='utf-8').read()
    for a, b in rep:
        assert s.count(a) == 1, (p, a[:90]); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)

edit('joint.py', [('    vdim(ax, P(0, 194.3)[1], P(0, z0 + btop - 1.5)[1], P(-22, 194.3)[0], P(-22, z0 + btop)[0], P(-30, 0)[0], f"stroke {z0 + btop - 1.5 - 224.3 + 30 - 30 + 0:.1f}+... see note")',
                   '    vdim(ax, P(0, 194.3)[1], P(0, z0 + btop - 30)[1], P(-22, 194.3)[0], P(-22, z0 + btop - 30)[0], P(-30, 0)[0], f"stroke {z0 + btop - 30 - 194.3:.1f}")')])
edit('views.py', [('PORT_Z=220,', 'PORT_Z=218,'), ('ACORN_Z=309,', 'ACORN_Z=310,')])
edit('parts_sheets.py', [
    ('    rb = D["BODY_D"] / 2; top = D["BODY_Z1"] - z0\n    sk_d = 12; gr0, gr1 = sk_d, sk_d + 5.3; scr = gr1 + 1; bore_top = top - 6',
     '    rb = D["BODY_D"] / 2; top = D["BODY_Z1"] - z0\n    sk_d = 12; gr0, gr1 = sk_d, sk_d + 5.3; scr = gr1 + 1; bore_top = top - 8'),
    ('''        prof = [(sg * 31.25, 0), (sg * 36, 0), (sg * 36, 20), (sg * rb, 30), (sg * rb, top), (sg * 5.25, top), (sg * 5.25, bore_top + 2),
                (sg * 10, bore_top + 2), (sg * 10, bore_top), (sg * 22, bore_top),''',
     '''        prof = [(sg * 31.25, 0), (sg * 36, 0), (sg * 36, 20), (sg * rb, 30), (sg * rb, top), (sg * 5.25, top), (sg * 5.25, top - 2),
                (sg * 10, top - 2), (sg * 10, bore_top), (sg * 22, bore_top),'''),
    ('(scr, bore_top, f"{bore_top - scr:.1f} bore"), (bore_top, top, "6"),', '(scr, bore_top, f"{bore_top - scr:.1f} bore"), (bore_top, top - 2, "6 recess"), (top - 2, top, "2"),'),
    ('"Ø20 x 2 seal recess, Ø10.5 rod hole, circlip groove Ø21 x 1.1"', '"Ø20 x 6 seal recess (circlip groove Ø21 x 1.1 at its foot), 2 lip, Ø10.5 rod hole"'),
    ('    ax.add_patch(Circle(P(fx, fz), 3.05, fc="white", ec=INK, lw=0.5, zorder=4))', '    ax.add_patch(Circle(P(fx, fz), 5.05, fc="white", ec=INK, lw=0.5, zorder=4))'),
    ('f"fulcrum Ø6.1 H8 @ x{fx:g}, z{fz:g}"', 'f"fulcrum bore Ø10.1 H8 (roller 52) @ x{fx:g}, z{fz:g}"'),
    ('"2x Ø6.4 THRU on 38 c/c"', '"2x Ø6.4 THRU on 38 c/c (M6x10 bolts)"'),
    ('    holes = [("A", 13, 5, 5, "M6 ↧10, thd ↧8"), ("B", 13, 43, 5, "M6 ↧10, thd ↧8"), ("C", 13, 24, 6, "Ø6 THRU; Ø8 H7 ↧6 from back"),',
     '    holes = [("A", 13, 5, 5, "Ø5 ↧7.5, M6 ↧6"), ("B", 13, 43, 5, "Ø5 ↧7.5, M6 ↧6"), ("C", 13, 24, 6, "Ø6 ↧4; Ø8 H7 ↧4 from back"),'),
    ('"face: Ra 1.6, flat 0.02. Back face R40 concave to suit Ø80 shell."', '"face Ra 1.6, flat 0.02. Back R40 concave on Ø80 shell: 8 thick on C/L, 10 at edges."'),
    (''' 38: ("Piston rod", "Steel, hard chrome 20 µm (or AISI 303)", 1, "V/E", dict(segs=[dict(L=14, D=8, t="M8"), dict(L=48, D=10, tol="f7"), dict(L=12, D=10),
     dict(L=12, D=8, t="M8")], xholes=[(68, 6.1, "rod pin, H8")], notes=["Ø10 f7 Ra 0.2 through rod seal.", "Top M8: check nut 47 + acorn 48."])),''',
     ''' 38: ("Piston rod", "Steel, hard chrome 20 µm (or AISI 303)", 1, "V/E", dict(segs=[dict(L=14, D=8, t="M8"), dict(L=39, D=10, tol="f7"), dict(L=12, D=10),
     dict(L=19, D=10), dict(L=14, D=8, t="M8")], xholes=[(59.1, 6.1, "rod pin, H8")], notes=["Ø10 f7 Ra 0.2 through rod seal.", "Top M8: check nut 47 + acorn 48."])),'''),
    (''' 52: ("Lever roller / bush", BRB, 1, "D/E", dict(segs=[dict(L=12, D=10)], bl=[(12, 6.05)])),''',
     ''' 52: ("Lever roller / bush", BRB, 1, "D/E", dict(segs=[dict(L=16, D=10, tol="f7")], bl=[(16, 6.05)], notes=["Runs in column bore Ø10.1 H8 on fulcrum pin 50."])),'''),
    (''' 46: ("Group bolt M6x12", "Stainless A2-70, ISO 4017", 2, "D/V", dict(segs=[dict(L=4, hex=10), dict(L=12, D=6, t="M6")])),''',
     ''' 46: ("Group bolt M6x10", "Stainless A2-70, ISO 4017", 2, "D/V", dict(segs=[dict(L=4, hex=10), dict(L=10, D=6, t="M6")], notes=["5 mm engagement in boss 69; 6 Nm [E]."])),'''),
])
edit('iso.py', [
    ('add(46, "hex bolt M6x12 A2-70", cyl((d["FL_X1"], 0, zz), (d["FL_X1"] + 4, 0, zz), 5.77, col=STL, shape="hex")\n            + cyl((d["FL_X1"] - 12, 0, zz), (d["FL_X1"], 0, zz), 3, col=STL), (55, 0, 0))',
     'add(46, "hex bolt M6x10 A2-70", cyl((d["FL_X1"], 0, zz), (d["FL_X1"] + 4, 0, zz), 5.77, col=STL, shape="hex")\n            + cyl((d["FL_X1"] - 10, 0, zz), (d["FL_X1"], 0, zz), 3, col=STL), (55, 0, 0))'),
    ('add(69, "group boss (pad)", box(bx + 36, d["PAD_X1"], -13, 13, pz - 26, pz + 26, CHR))', 'add(69, "group boss (pad)", box(bx + 38, d["PAD_X1"], -13, 13, pz - 24, pz + 24, CHR))'),
    ('         + box(d["PAD_X1"], d["FL_X1"], -13, 13, pz - 26, pz + 26, CHR) + cyl((d["FL_X1"], 0, pz), (131, 0, pz), 11, col=CHR))',
     '         + box(d["PAD_X1"], d["FL_X1"], -13, 13, pz - 24, pz + 24, CHR) + cyl((d["FL_X1"], 0, pz), (131, 0, pz), 11, col=CHR))'),
    ('         + box(gx - 31, gx - 9, -10, 10, d["YOKE_Z1"] - 16, d["YOKE_Z1"], CHR) + cyl((gx, 0, d["YOKE_Z1"]), (gx, 0, d["YOKE_Z1"] + 8), 4, col=STL)',
     '         + box(d["COL_X0"], d["COL_X1"], -8, 8, d["BODY_Z1"] - 4, d["YOKE_Z1"], CHR)'),
    ('         + cyl((gx, 0, 206), (gx, 0, d["BODY_Z1"]), 25, col=CHR) + box(gx - 9, gx + 9, -10, 10, d["BODY_Z1"], d["YOKE_Z1"], CHR)',
     '         + cyl((gx, 0, 206), (gx, 0, d["BODY_Z1"]), 25, col=CHR)'),
    ('add(47, "lock nut M8", cyl((gx, 0, d["YOKE_Z1"]), (gx, 0, d["YOKE_Z1"] + 6), 7.5, col=CHR, shape="hex"), tuple(G + [0, 0, 30]))',
     'add(47, "check nut M8", cyl((gx, 0, 294), (gx, 0, 300), 7.5, col=CHR, shape="hex"), tuple(G + [0, 0, 30]))'),
    ('add(48, "acorn nut M8", cyl((gx, 0, d["YOKE_Z1"] + 6), (gx, 0, d["ACORN_Z"] - 4), 7.5, col=CHR, shape="hex")',
     'add(48, "acorn nut M8", cyl((gx, 0, 300), (gx, 0, d["ACORN_Z"] - 4), 7.5, col=CHR, shape="hex")'),
    ('add(36, "piston", cyl((gx, 0, 183), (gx, 0, 213), 21.95, col=BRS), tuple(P + [0, 0, -10]))', 'add(36, "piston", cyl((gx, 0, 194.3), (gx, 0, 224.3), 21.95, col=BRS), tuple(P + [0, 0, -10]))'),
    ('add(37, "piston seal", cyl((gx, 0, 188), (gx, 0, 193.5), 22, ri=18, col=BLK), tuple(P + [0, 0, -38]))', 'add(37, "piston seal", cyl((gx, 0, 198.3), (gx, 0, 203.9), 22, ri=18, col=BLK), tuple(P + [0, 0, -38]))'),
    ('add(37, "piston seal", cyl((gx, 0, 201), (gx, 0, 206.5), 22, ri=18, col=BLK), tuple(P + [0, 0, -52]))', 'add(37, "piston seal", cyl((gx, 0, 211.3), (gx, 0, 216.9), 22, ri=18, col=BLK), tuple(P + [0, 0, -52]))'),
    ('add(38, "piston rod", cyl((gx, 0, 201), (gx, 0, 274), 5, col=STL), tuple(P + [0, 0, -10]))', 'add(38, "piston rod", cyl((gx, 0, 210.3), (gx, 0, 308.3), 5, col=STL), tuple(P + [0, 0, -10]))'),
    ('add(39, "rod seal", cyl((gx, 0, 249), (gx, 0, 253), 10, ri=5, col=PTFE), tuple(P + [0, 0, 42]))', 'add(39, "rod seal", cyl((gx, 0, 254), (gx, 0, 258), 10, ri=5, col=PTFE), tuple(P + [0, 0, 42]))'),
    ('add(40, "rod washer", cyl((gx, 0, 248), (gx, 0, 249), 10, ri=5.25, col=STL), tuple(P + [0, 0, 50]))', 'add(40, "rod washer", cyl((gx, 0, 253), (gx, 0, 254), 10, ri=5.25, col=STL), tuple(P + [0, 0, 50]))'),
    ('add(41, "circlip DIN 472-20", cyl((gx, 0, 247), (gx, 0, 248), 11, ri=9.5, col=BLK), tuple(P + [0, 0, 58]))', 'add(41, "circlip DIN 472-20", cyl((gx, 0, 252), (gx, 0, 253), 10.5, ri=8.5, col=BLK), tuple(P + [0, 0, 58]))'),
    ('add(43, "shower screen", cyl((gx, 0, 181.3), (gx, 0, 182.3), 26, col=STL), tuple(G + [0, 0, -30]))', 'add(43, "shower screen", cyl((gx, 0, 193.3), (gx, 0, 194.3), 26, col=STL), tuple(G + [0, 0, -30]))'),
    ('add(42, "group gasket", cyl((gx, 0, 176), (gx, 0, 181.3), 28.85, ri=23.5, col=BLK), tuple(G + [0, 0, -46]))', 'add(42, "group gasket", cyl((gx, 0, 188), (gx, 0, 193.3), 28.85, ri=23.5, col=BLK), tuple(G + [0, 0, -46]))'),
    ('add(56, "basket double", cyl((gx, 0, 157), (gx, 0, 176), 22, 24.5, col=STL, ri=21), tuple(G + [0, 0, -66]))', 'add(56, "basket double", cyl((gx, 0, 168), (gx, 0, 187), 22, 24.5, col=STL, ri=21), tuple(G + [0, 0, -66]))'),
    ('add(57, "basket single", cyl((gx, 0, 163), (gx, 0, 176), 21, 24.5, col=STL, ri=20), tuple(G + [0, 80, -66]))', 'add(57, "basket single", cyl((gx, 0, 174), (gx, 0, 187), 21, 24.5, col=STL, ri=20), tuple(G + [0, 80, -66]))'),
    ('add(58, "basket spring", cyl((gx, 0, 170), (gx, 0, 171), 26, ri=25, col=STL), tuple(G + [0, 0, -80]))', 'add(58, "basket spring", cyl((gx, 0, 182), (gx, 0, 183), 26, ri=25, col=STL), tuple(G + [0, 0, -80]))'),
    ('''    add(54, "portafilter body", cyl((gx, 0, 152), (gx, 0, 176), 28, 30, col=CHR, ri=26) + cyl((gx, 0, 152), (gx, 0, 155), 28, col=CHR)
        + box(gx - 4, gx + 4, 28, 34, 170, 176, CHR) + box(gx - 4, gx + 4, -34, -28, 170, 176, CHR) + tube([PFp(28, 165), PFp(52, 163)], 15, CHR),''',
     '''    add(54, "portafilter body", cyl((gx, 0, 164), (gx, 0, 188), 28, 30, col=CHR, ri=26) + cyl((gx, 0, 160), (gx, 0, 164), 13, col=CHR) + cyl((gx, 0, 164), (gx, 0, 166), 28, col=CHR)
        + box(gx - 4, gx + 4, 28, 33, 180, 183.5, CHR) + box(gx - 4, gx + 4, -33, -28, 180, 183.5, CHR) + tube([PFp(28, 172), PFp(52, 170)], 15, CHR),'''),
    ('add(55, "spout", cyl((gx, 0, 140), (gx, 0, 152), 6, 7, col=CHR) + tube([(gx, -5, 141), (gx, -15, 135)], 6, CHR) + tube([(gx, 5, 141), (gx, 15, 135)], 6, CHR),',
     'add(55, "spout", cyl((gx, 0, 146), (gx, 0, 160), 6, 7, col=CHR) + tube([(gx, -5, 147), (gx, -15, 135)], 6, CHR) + tube([(gx, 5, 147), (gx, 15, 135)], 6, CHR),'),
    ('add(59, "handle stud M8x75", tube([PFp(40, 164), PFp(115, 160)], 8, STL)', 'add(59, "handle stud M8x75", tube([PFp(40, 171), PFp(115, 167)], 8, STL)'),
    ('add(60, "PF handle", tube([PFp(52, 163), PFp(152, 158)], 24, WOOD)', 'add(60, "PF handle", tube([PFp(52, 170), PFp(152, 165)], 24, WOOD)'),
    ('    for pp, tag in ((Fp, "fulcrum"), (np.array([149, 0, 268.0]), "rod pin")):', '    for pp, tag in ((Fp, "fulcrum"), (np.array([d["ROD_PIN_X"], 0, d["ROD_PIN_Z"]]), "rod pin")):'),
    ('    add(52, "fulcrum bush", cyl(tuple(Fp + [0, -10, 0]), tuple(Fp + [0, 10, 0]), 5, ri=3.05, col=BRS), tuple(L + [0, -28, 0]))',
     '    add(52, "roller Ø10x16", cyl(tuple(Fp + [0, -8, 0]), tuple(Fp + [0, 8, 0]), 5, ri=3.05, col=BRS), tuple(L + [0, -28, 0]))'),
])
# make_drawings main
edit('make_drawings.py', [
    ('''    with PdfPages(os.path.join(OUT, "LaPavoni_Europiccola_1979_drawings.pdf")) as pdf:
        import view_sheets as VS
        VS.sheet_front_rear(pdf, Sheet); VS.sheet_sides(pdf, Sheet); VS.sheet_plan(pdf, Sheet)
        import sections as SC
        SC.sheet_boiler(pdf, Sheet, View); SC.sheet_group(pdf, Sheet, View); sheet4(pdf); sheet5(pdf)
        half = (len(BOM) + 1) // 2''',
     '''    import glob
    for f in glob.glob(os.path.join(OUT, "sheet*.png")) + glob.glob(os.path.join(OUT, "sheet*.svg")): os.remove(f)
    import view_sheets as VS, sections as SC, iso as ISO, joint as JT, parts_sheets as PS
    Sheet.total = 27; Sheet.counter = 0
    with PdfPages(os.path.join(OUT, "LaPavoni_Europiccola_1979_drawings.pdf")) as pdf:
        ISO.sheet_iso(pdf, Sheet); ISO.sheet_exploded(pdf, Sheet)
        VS.sheet_front_rear(pdf, Sheet); VS.sheet_sides(pdf, Sheet); VS.sheet_plan(pdf, Sheet)
        SC.sheet_boiler(pdf, Sheet, View); JT.sheet_group(pdf, Sheet); JT.sheet_joint(pdf, Sheet); sheet5(pdf)
        PS.build(pdf, Sheet)
        JT.sheet_fasteners(pdf, Sheet)
        half = (len(BOM) + 1) // 2'''),
])
s = open('make_drawings.py', encoding='utf-8').read()
s = s.replace('bom_sheet(pdf, 8, BOM[:half]', 'bom_sheet(pdf, None, BOM[:half]').replace('bom_sheet(pdf, 9, BOM[half:]', 'bom_sheet(pdf, None, BOM[half:]')
s = s.replace('sh = Sheet(10, "SEAL', 'sh = Sheet(None, "SEAL').replace('sh = Sheet(7, "BASE', 'sh = Sheet(None, "BASE')
open('make_drawings.py', 'w', encoding='utf-8').write(s)
print("ok")

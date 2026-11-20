"""Section sheets rebuilt on the shared dimension table (views.D) so sections and orthographic views agree."""
import math
from views import D

BR, BR2, GK, WD = "#f4e3b5", "#e6c98f", "#dddddd", "#d2ae7e"

def sheet_boiler(pdf, Sheet, View):
    sh = Sheet(4, "BOILER ASSEMBLY - SECTION A-A (vertical, through boiler axis)", "1:1.4")
    s = 0.72
    v = View(sh, 150, 22, s)
    R, t = D["SH_D"] / 2, 1.5
    zf, z1, zs, zn = D["FOOT_Z"], D["SH_Z1"], D["SHO_Z"], D["NECK_Z"]
    # rubber cover + base sheet (cut through the X-Z plane: rear wall at x=-BX)
    v.rect(-D["BX"] - 2, 0, D["BX"] + 82, D["RUB_H"] - 9, fc="#2b2b2b", lw="thin"); v.line([(80, -4), (84, 6), (78, 10), (82, 66)], lw="thin")
    v.poly([(-D["BX"] - 2, 0), (-D["BX"] + 6, 0), (-D["BX"] + 6, D["RUB_H"]), (-D["BX"] - 2, D["RUB_H"])], fc="#2b2b2b", lw="thin")
    v.line([(-D["BX"], 8), (-D["BX"] + 6, 59.5), (-41, 59.5)], lw=1.4); v.line([(41, 59.5), (80, 59.5)], lw=1.4)
    v.text(-D["BX"] + 8, 30, "61 base 1.0 [E]", size=4.6); v.text(-D["BX"] + 8, 4, "63 rubber cover", size=4.6, color="white")
    # gaskets (upper on top of base, lower beneath), ring nut, spigot, foot flare
    for sg in (-1, 1):
        v.sec(sg * 40 - (6.5 if sg < 0 else 0), 60, 6.5, 2, hatch="xxxx", fc=GK)
        v.sec(sg * 40 - (6.5 if sg < 0 else 0), 57, 6.5, 2, hatch="xxxx", fc=GK)
        v.poly([(sg * 40, 45), (sg * 49, 45), (sg * 49, 57), (sg * 40, 57)], fc=BR, hatch="////")
        v.rect(sg * 49 - (8 if sg < 0 else 0), 45, 8, 12, fc=BR, lw="thin")
        v.poly([(sg * 34, 42), (sg * 40, 42), (sg * 40, 62), (sg * 46, 62), (sg * 46, 65), (sg * R, zf), (sg * (R - t), zf), (sg * 34, 66)],
               fc=BR, hatch="\\\\\\\\")
        for k in range(9): v.line([(sg * 40, 43 + k * 2), (sg * 40.8, 44 + k * 2)], lw="thin")
        v.sec(sg * 34 - (7 if sg < 0 else 0), 40, 7, 2, hatch="xxxx", fc=GK)
        v.rect(sg * 52 - 3, 32, 6, 22, fc="#cccccc", lw="thin"); v.rect(sg * 52 - 5, 26, 10, 6, fc="#cccccc", lw="thin")
    v.poly([(-42, 32), (42, 32), (42, 40), (-42, 40)], fc=BR, hatch="////")
    v.rect(42, 32, 13, 8, fc=BR, lw="thin"); v.rect(-55, 32, 13, 8, fc=BR, lw="thin")
    for i in range(8):
        z = 52 + i * 12
        for xx in (-26 + (i % 2) * 3, 22 - (i % 2) * 3): v.circ(xx + 2, z, 4, fc="#d9a066")
    for xx in (-24, 24, -8): v.line([(xx, 40), (xx, 50)], lw=2.4)
    for xx in (-22, -7, 8, 23):
        v.rect(xx - 3, 18, 6, 14, fc="#fafafa", lw="thin"); v.rect(xx - 1, 11, 2, 7, fc="#bbb", lw="thin")
    # shell, shoulder, neck
    for sg in (-1, 1):
        v.sec(sg * R - (t if sg > 0 else 0), zf, t, z1 - zf, hatch="////", fc=BR)
        v.poly([(sg * R, z1), (sg * (R - t), z1), (sg * 20.5, zs - 1), (sg * 19, zs), (sg * 19, zn), (sg * 22, zn), (sg * 22, zs), (sg * R, z1 + 3)],
               fc=BR, hatch="\\\\\\\\")
        for k in range(4): v.line([(sg * 19, 264 + k * 2.3), (sg * 18.3, 265 + k * 2.3)], lw="thin")
    # cap insert + gasket + knob + screw
    v.poly([(-18.5, 252), (18.5, 252), (18.5, zn), (22, zn + 2), (22, zn + 5), (-22, zn + 5), (-22, zn + 2), (-18.5, zn)], fc=BR2, hatch="....")
    v.sec(-22, zn, 6, 2, hatch="xxxx", fc=GK); v.sec(16, zn, 6, 2, hatch="xxxx", fc=GK)
    v.poly([(-14, zn + 5), (14, zn + 5), (19, D["CAP_Z"]), (29, D["CAP_Z"]), (29, D["TOP"]), (-29, D["TOP"]), (-29, D["CAP_Z"]), (-19, D["CAP_Z"])], fc=WD, hatch="----")
    v.rect(-4, 258, 8, 54, fc="#cccccc", lw="thin")
    # safety valve on shoulder (front side)
    sx = D["SV_X"] - D["BX"]
    v.rect(sx - 6, 248, 12, 10, fc=BR2, hatch="////", lw="thin"); v.rect(sx - 7, 258, 14, 6, fc="#e8e8e8", lw="thin")
    v.circ(sx, 260, 3, fc="#999"); v.line([(sx - 2.5, 262), (sx + 2.5, 264), (sx - 2.5, 266), (sx + 2.5, 268), (sx - 2.5, 270)], lw="thin")
    v.rect(sx - 11, 264, 22, 24, fc="#eeeeee", lw="thin"); v.line([(sx + 11, 275), (sx + 20, 268), (54, 250), (54, 140)], lw=1.0, color="#777")
    # steam valve (rear, Y=-12: shown rotated into plane)
    zst = D["STK_Z"]
    v.rect(-D["BX"] + 6, zst - 7.5, D["BX"] - 6 - 30, 15, fc="#eeeeee"); v.rect(-D["BX"] - 2, zst - 8, 8, 16, fc="#e0e0e0")
    v.rect(-D["BX"] - 6, zst - 3, 4, 6, fc="#ccc", lw="thin")
    v.poly([(-D["BX"] - 6, zst - 18.5), (D["STK_X0"] - D["BX"], zst - 15.5), (D["STK_X0"] - D["BX"], zst + 15.5), (-D["BX"] - 6, zst + 18.5)], fc=WD, hatch="----")
    v.line([(-52, zst - 7), (-53, 250), (-55, 200), (-55, 128), (-49, 116)], lw=8 * s * 2.835 * 0.35, color="#888")
    # group port + boiler boss + L-tube (front)
    pz = D["PORT_Z"]
    v.poly([(R, pz - 16), (R + 16, pz - 16), (R + 16, pz + 16), (R, pz + 16)], fc=BR, hatch="////")
    v.rect(R, pz - 4, 16, 8, fc="white", lw="thin"); v.sec(R + 16, pz - 12, 2, 24, hatch="xxxx", fc=GK)
    v.poly([(R + 18, pz - 27), (R + 24, pz - 27), (R + 24, pz + 27), (R + 18, pz + 27)], fc="none", lw="hid")
    v.text(R + 26, pz + 22, "group (sheet 5)", size=4.6)
    v.line([(R + 2, pz), (22, pz), (16, pz - 6), (16, 140)], lw=2.4)
    # sight glass (rear-left, rotated into plane), r = 47
    for zc in (D["SG_Z0"], D["SG_Z1"]):
        v.rect(-56, zc - 9, 18, 18, fc="#eeeeee"); v.rect(-38, zc - 5, 4, 10, fc="#cccccc", lw="thin")
        v.rect(-34, zc - 8.5, 5, 17, fc=BR, hatch="////", lw="thin")
    v.rect(-55, D["SG_Z0"] + 9, 16, D["SG_Z1"] - D["SG_Z0"] - 18, fc="#e8f4fb", lw="thin")
    v.rect(-53, D["SG_Z0"] + 3, 12, 106, fc="white", lw="thin")
    # water levels
    v.line([(-R + t, 185), (R - t, 185)], lw="thin", ls=(0, (6, 2)), color="#2a6fb0"); v.text(-34, 187, "MAX working fill ~0.6 l [E]", size=4.4, color="#2a6fb0")
    v.line([(-R + t, 150), (R - t, 150)], lw="thin", ls=(0, (6, 2)), color="#2a6fb0"); v.text(-34, 152, "MIN - cover element & L-tube", size=4.4, color="#2a6fb0")
    v.cl((0, -2), (0, 328))
    for (x, y, n, dx, dy) in [(R - 0.7, 160, 1, 32, 0), (21, 256, 2, 28, 14), (40, 52, 3, 30, -6), (45, 51, 4, 26, -14), (43, 61, 5, 30, 2),
                              (0, 90, 6, 52, -12), (-37, 41, 7, -36, -4), (-52, 28, 8, -26, -8), (0, 262, 9, -10, 30), (-19, 274, 10, -38, 6),
                              (-24, 312, 11, -30, 4), (0, 306, 12, 16, 14), (sx, 252, 13, 34, -12), (sx, 260, 14, 34, -4), (sx, 267, 15, 34, 4),
                              (sx + 8, 284, 16, 26, 10), (-47, 165, 17, -40, 8), (-55, 140, 18, -22, -6), (-47, D["SG_Z1"], 19, -26, 10),
                              (-31, D["SG_Z0"], 21, -36, -8), (-60, zst + 6, 25, -10, 14), (16, 170, 45, 32, -10), (-7, 22, 6, -30, -10)]:
        v.balloon(x, y, n, dx, dy)
    v.dim((-R, 120), (R, 120), 0, f"Ø{D['SH_D']} shell", "V")
    v.dim((-46, 62), (46, 62), 34, "Ø92 foot", "V", size=4.6)
    v.dim((R, zf), (R, z1), 56, f"{z1 - zf} shell", "V")
    v.dim((R, z1), (R, zs), 56, f"{zs - z1}", "V", size=4.4)
    v.dim((-40, 42), (40, 42), -16, "M80x1.25 spigot", "D/E")
    v.dim((-42, 32), (42, 32), -24, "Ø84 element flange", "D")
    v.dim((-22, zn), (22, zn), 34, f"Ø{D['NECK_D']} neck", "V", size=4.6)
    v.dim((-29, D["TOP"]), (29, D["TOP"]), 6, f"Ø{D['KNOB_D']}", "V")
    v.dim((-56, D["SG_Z0"]), (-56, D["SG_Z1"]), 12, f"{D['SG_Z1'] - D['SG_Z0']} c/c", "V")
    v.dim((-53, D["SG_Z0"] + 3), (-53, D["SG_Z0"] + 109), 22, "glass 106", "D")
    v.dim((R + 16, 0), (R + 16, pz), -24, f"{pz} port", "V")
    v.dim((0, 0), (0, D["TOP"]), 95, f"{D['TOP']} overall", "D")
    v.dim((-D["BX"], 0), (-D["BX"], 60), 6, "60", "V", size=4.4)
    v.dim((0, 300), (sx, 300), 0, f"{sx}", "V", size=4.4)
    sh.note(255, 285, "NOTES - BOILER", 7, weight="bold")
    sh.note(255, 279, "\n".join([
        f"1. Shell: brass tube Ø{D['SH_D']} x 1.5 [V/E] (3\" tube, 76.2), {z1 - zf} long, Ag-brazed",
        "   into a stamped foot casting (flare Ø92 + threaded spigot) and a",
        "   shoulder/neck casting. Assembly Cu/Ni/Cr plated outside.",
        "2. Spigot thread M80x1.25 fine pitch (La Pavoni 1978-96) [D pitch].",
        "   Do NOT fit a 1.5-pitch (post-1996) ring nut.",
        "3. Base clamped between 2 gaskets 93x80x2 AFM34 by ring nut 4.",
        "4. Element flange seals on the spigot end face with 82x68x2 gasket,",
        "   pulled up by 3 screws into the ring-nut ears, ~4 Nm in 3 passes [E].",
        "5. Original 1979 fibre gaskets may contain asbestos: wet, don't sand.",
        "6. Cross-check: these dims give ~0.86 l gross internal volume,",
        "   consistent with the documented 0.8 l capacity [D].",
        "7. Neck internal thread ~M38x1.5 [E]; v2 cap screws INTO the neck [D].",
        "8. Sight glass and steam valve are not in the section plane;",
        "   they are shown rotated into it (true positions on sheets 1-3).",
        "9. Hatching: //// brass, xxxx gasket, ---- wood/phenolic, .... insert.",
    ]), 5.3)
    sh.note(255, 196, "THREAD DATA (verify with a thread gauge)", 6.5, weight="bold")
    data = [("Spigot / ring nut", "M80 x 1.25", "D pitch, E dia"), ("Neck / cap insert", "~M38 x 1.5", "E"), ("Safety valve", "M12", "D"),
            ("Steam valve boss", "12 mm", "D"), ("Sight-glass spigots", "M12 x 1", "E"), ("Group bolts", "M6", "D/V"), ("Element screws", "M6 (or M5)", "D")]
    for i, (a, b, c) in enumerate(data):
        y = 189 - i * 4.6
        sh.ax.text(255, y, a, fontsize=5.3, va="top"); sh.ax.text(305, y, b, fontsize=5.3, va="top", weight="bold"); sh.ax.text(340, y, c, fontsize=5.3, va="top")
    sh.save(pdf)

def sheet_group(pdf, Sheet, View):
    sh = Sheet(5, "BREW GROUP, PISTON & LEVER - SECTION B-B (through group axis)", "1:1")
    v = View(sh, 115, 92, 1.0)
    PFb = D["PF_Z0"] - D["BELL_Z0"]          # portafilter exterior bottom (rel.)
    Sp = D["SPOUT_Z"] - D["BELL_Z0"]
    rb = D["BODY_D"] / 2
    top = D["BODY_Z1"] - D["BELL_Z0"]; yk = D["YOKE_Z1"] - D["BELL_Z0"]; ac = D["ACORN_Z"] - D["BELL_Z0"]; pz = D["PORT_Z"] - D["BELL_Z0"]
    # group body section
    for sg in (-1, 1):
        v.poly([(sg * 22, 6.3), (sg * 22, top - 6), (sg * 10, top - 6), (sg * 10, top - 10), (sg * 5.5, top - 10), (sg * 5.5, top), (sg * rb, top),
                (sg * rb, 30), (sg * 36, 20), (sg * 36, 0), (sg * 28.85, 0), (sg * 28.85, 5.3), (sg * 23.5, 5.3), (sg * 23.5, 6.3)], fc=BR, hatch="////")
    v.poly([(-rb, pz - 4), (-22, pz - 4), (-22, pz + 4), (-rb, pz + 4)], fc="white", lw="thin")
    v.poly([(-rb - 6, 20), (-rb, 20), (-rb, 74), (-rb - 6, 74)], fc=BR, hatch="////")
    v.poly([(-rb - 6, pz - 4), (-rb, pz - 4), (-rb, pz + 4), (-rb - 6, pz + 4)], fc="white", lw="thin")
    v.sec(-rb - 8, pz - 12, 2, 24, hatch="xxxx", fc=GK)
    v.poly([(-rb - 8, 31), (-rb - 24, 31), (-rb - 24, 63), (-rb - 8, 63)], fc=BR2, hatch="\\\\\\\\"); v.text(-rb - 24, 66, "boiler boss", size=4.4)
    for zb in (pz - D["BOLT_CC"] / 2, pz + D["BOLT_CC"] / 2):
        v.hid([(-rb - 22, zb - 3), (-rb + 2, zb - 3)]); v.hid([(-rb - 22, zb + 3), (-rb + 2, zb + 3)])
    # gasket, screen
    v.sec(-28.85, 0, 5.35, 5.3, hatch="xxxx", fc=GK); v.sec(23.5, 0, 5.35, 5.3, hatch="xxxx", fc=GK)
    v.rect(-26, 5.3, 52, 1, fc="#bbbbbb", lw="thin")
    # rod seal stack at top
    v.sec(-10, top - 10, 4.5, 4, hatch="....", fc="white"); v.sec(5.5, top - 10, 4.5, 4, hatch="....", fc="white")
    v.rect(-10, top - 11, 4.5, 1, fc="#888", lw="thin"); v.rect(5.5, top - 11, 4.5, 1, fc="#888", lw="thin")
    v.rect(-11, top - 12, 1.2, 1, fc="#222", lw="thin"); v.rect(9.8, top - 12, 1.2, 1, fc="#222", lw="thin")
    # piston (bottom of stroke) + seals + rod
    p0 = 7
    v.poly([(-21.9, p0), (21.9, p0), (21.9, p0 + 30), (-21.9, p0 + 30)], fc=BR2, hatch="\\\\\\\\")
    for g in (p0 + 5, p0 + 18):
        for sg in (-1, 1):
            v.poly([(sg * 22, g), (sg * 18, g), (sg * 18, g + 5.5), (sg * 22, g + 5.5)], fc="#333", lw="thin")
    v.rect(-5, p0 + 30, 10, 92 - p0 - 30 + 5, fc="#dddddd"); v.circ(0, 92, 3, fc="white")
    v.rect(-4, p0 + 20, 8, 10, fc="white", lw="thin"); v.text(5, p0 + 24, "M8", size=4.4)
    # yoke, stud, nuts
    v.poly([(-9, top), (9, top), (9, yk), (-31, yk), (-31, yk - 16), (-9, yk - 16)], fc="#eeeeee")
    v.rect(-4, top, 8, yk - top, fc="white", lw="thin")
    v.circ(-25, 105 - 0, 3.5, fc="white")
    v.rect(-4, yk, 8, 4, fc="#ccc", lw="thin"); v.rect(-7.5, yk, 15, 6, fc="#e8e8e8", lw="thin")
    v.poly([(-7.5, yk + 6), (7.5, yk + 6), (6, ac - 4), (0, ac), (-6, ac - 4)], fc="#e8e8e8", lw="thin")
    # lever fork stub (phantom)
    la = math.radians(D["LEV_ANG"])
    v.line([(-25 - 14 * math.cos(la), 105 + 14 * math.sin(la)), (-25 + 90 * math.cos(la), 105 - 90 * math.sin(la))], lw=0.5, ls=(0, (10, 2, 2, 2)), color="#666")
    # portafilter + basket + spout
    for sg in (-1, 1):
        v.poly([(sg * 26, 0), (sg * 30, 0), (sg * 30, -3), (sg * 28, PFb), (sg * 7, PFb), (sg * 7, PFb + 4), (sg * 25, PFb + 4), (sg * 26, -1)], fc=BR, hatch="////")
    v.line([(-24.5, -0.5), (-21, -19), (21, -19), (24.5, -0.5)], lw=0.6)
    v.poly([(-7, PFb), (7, PFb), (6, PFb - 12), (-6, PFb - 12)], fc=BR2, hatch="////")
    v.line([(-5, PFb - 12), (-15, Sp)], lw=1.8); v.line([(5, PFb - 12), (15, Sp)], lw=1.8)
    v.cl((0, Sp - 6), (0, ac + 6))
    for (x, y, n, dx, dy) in [(rb - 1, 50, 35, 24, 10), (0, p0 + 12, 36, 34, -12), (20, p0 + 8, 37, 26, -4), (0, 70, 38, 26, 16),
                              (8, top - 8, 39, 22, 10), (8, top - 10.5, 40, 22, 4), (10.4, top - 11.5, 41, 22, -2), (26, 2.6, 42, 22, -6),
                              (-20, 5.8, 43, -16, -12), (-rb - 7, pz + 9, 44, -12, 18), (-rb - 14, pz - 19, 46, -18, -10), (0, yk + 3, 47, 18, 2),
                              (0, ac - 4, 48, 18, 6), (29, -8, 54, 22, -8), (0, -12, 56, 30, -2), (-12, Sp + 3, 55, -16, -6), (-25, 105, 50, -16, 8)]:
        v.balloon(x, y, n, dx, dy)
    v.dim((-22, 60), (22, 60), 0, "bore Ø44 H8", "D")
    v.dim((-rb, top + 2), (rb, top + 2), 0, f"Ø{D['BODY_D']} body", "E")
    v.dim((-36, 0), (36, 0), -50, "Ø72 bell", "D")
    v.dim((-28.85, 5.3), (28.85, 5.3), -46, "gasket 57.7 x 47 x 5.3", "D")
    v.dim((-30, PFb), (30, PFb), -8, f"Ø{D['PF_D']} PF / basket 49", "V/D")
    v.dim((rb, 0), (rb, top), 18, f"{top} seat to body top", "V")
    v.dim((rb, top), (rb, ac), 18, f"{ac - top}", "V", size=4.4)
    v.dim((-rb - 24, pz - D["BOLT_CC"] / 2), (-rb - 24, pz + D["BOLT_CC"] / 2), -8, f"{D['BOLT_CC']} bolt c/c", "V")
    v.dim((-21.9, p0), (-21.9, p0 + 30), -6, "30", "E", size=4.4)
    v.dim((-15, Sp), (15, Sp), -14, "30 spout c/c", "V", size=4.4)
    v.text(-56, -66, "Z values on this sheet are measured from the portafilter seat; add 176 for height above the table.", size=4.6, color="#7a1f1f")
    v.text(-56, -71, f"Group body Ø{D['BODY_D']} is the minimum around a Ø44 bore; the video reads 42-47 (chrome reflections) - MEASURE.", size=4.6, color="#7a1f1f")
    # lever geometry view
    L = View(sh, 250, 225, 0.42, "LEVER GEOMETRY (1:2.4)", lx=320, ly=168)
    F = (0, 0); Rp = (19, -13)
    ex, ez = D["LEV_L"] * math.cos(la), -D["LEV_L"] * math.sin(la)
    L.line([(-14 * math.cos(la), 14 * math.sin(la)), (60 * math.cos(la), -60 * math.sin(la))], lw=6, color="#3a3a3a")
    L.line([(55 * math.cos(la), -55 * math.sin(la)), ((D["LEV_L"] - D["HANDLE_L"]) * math.cos(la), -(D["LEV_L"] - D["HANDLE_L"]) * math.sin(la))], lw=3, color="#999")
    L.line([((D["LEV_L"] - D["HANDLE_L"]) * math.cos(la), -(D["LEV_L"] - D["HANDLE_L"]) * math.sin(la)), (ex, ez)], lw=8, color=WD)
    L.circ(*F, 3.5, fc="white"); L.circ(*Rp, 3.5, fc="white"); L.rect(15, -80, 8, 67, fc="#ddd", lw="thin")
    L.dim(F, Rp, 9, "23 [V]", size=4.4); L.dim(F, (ex, ez), -12, f"{D['LEV_L']} fulcrum to handle end", "V")
    L.dim(((D["LEV_L"] - D["HANDLE_L"]) * math.cos(la), -(D["LEV_L"] - D["HANDLE_L"]) * math.sin(la)), (ex, ez), 14, f"{D['HANDLE_L']} handle", "V", size=4.4)
    L.text(-20, 18, f"Fulcrum: X{D['FX']} Z{D['FZ']} (25 behind group axis)\nRod pin: X149 Z268  -  lever at rest {D['LEV_ANG']}° below horizontal\n"
           f"Ratio ~ {D['LEV_L']}/23 = 11.8:1 (pin spacing +/-3 -> 10-13:1) [V/E]", size=4.8, color="#7a1f1f")
    sh.note(250, 128, "NOTES - GROUP", 7, weight="bold")
    sh.note(250, 122, "\n".join([
        "1. Hot-stamped brass group, plated. Fixed to the boiler boss by 2 x M6x20",
        "   A2-70 hex bolts (AF10), sealed by item 44; L-tube 45 dips into the boiler.",
        "2. Piston drawn at the bottom of its stroke (lever down). Raising the lever lifts",
        f"   the piston past the inlet port (Z{D['PORT_Z']} above table); stroke ~40 [E].",
        "3. Piston seal lips face DOWN. Grease with food-grade silicone (Molykote 111).",
        "4. Gasket and screen: press into the group, then seat them with the portafilter.",
        "5. Pins Ø6 with E-clips DIN 6799 size 5. Top: M8 lock nut + acorn nut.",
    ]), 5.3)
    sh.save(pdf)

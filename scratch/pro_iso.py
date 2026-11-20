import os
os.chdir(r"C:\coffee\professional")
s = open('iso.py', encoding='utf-8').read()
i = s.index('# ------------------------------------------------------------------ itemised model'); j = s.index('# ------------------------------------------------------------------ renderer')
new = r'''# ------------------------------------------------------------------ itemised model (PROFESSIONAL v3.1 copper/brass)
COP, BRP = "#d98c5f", "#e9c35a"
def items():
    d = D; bx, gx, pz = d["BX"], d["GX"], d["PORT_Z"]
    I = []
    add = lambda it, lab, F, ex=(0, 0, 0): I.append((it, lab, F, np.array(ex, float)))
    # ---- base group
    for k, (fx_, fy_) in enumerate(((30, -70), (30, 70), (255, -62), (255, 62))):
        add(80, "foot", cyl((fx_, fy_, 0), (fx_, fy_, 4), 9, col=RUB), (0, 0, -330))
    add(79, "sub-base (ABS)", loft(rounded_trap(202, 188, 292, 59, x0=-1), 4, rounded_trap(202, 188, 292, 59, x0=-1), 10, RUB), (0, 0, -300))
    add(61, "base (brass)", loft(rounded_trap(200, 186, 290, 58), 10, rounded_trap(186, 172, 276, 51, x0=7), 65, BRP), (0, 0, -240))
    tr = rounded_trap(d["TRAY_W"], d["TRAY_W"] - 6, d["TRAY_L"], 24, x0=d["TRAY_X0"])
    add(82, "drip tray (ABS)", loft(tr, 50, tr, 64, BLK), (0, 0, -200))
    tg = rounded_trap(d["TRAY_W"] - 8, d["TRAY_W"] - 14, d["TRAY_L"] - 8, 20, x0=d["TRAY_X0"] + 4)
    F = loft(tg, 64, tg, 64.8, BRP)
    for a in range(10):
        for b in range(8):
            if abs(a - 4.5) < 1 and abs(b - 3.5) < 1: continue
            F += cyl((d["TRAY_X0"] + 14 + a * 12.2, -45 + b * 12.8, 64.81), (d["TRAY_X0"] + 14 + a * 12.2, -45 + b * 12.8, 64.9), 3.6, col="#555555", n=10)
    add(62, "drip grid (brass)", F, (0, 0, -150))
    sx, sz = d["SW_X"], d["SW_Z"]
    add(65, "switch (green)", box(sx - 13, sx + 13, -101, -97, sz - 17, sz + 17, BLK) + box(sx - 11, sx + 11, -101.6, -100.9, sz - 15, sz + 15, "#1f8a3a"), (0, -45, -240))
    add(64, "badge", cyl((285, d["BADGE_Y"], d["BADGE_Z"]), (288.5, d["BADGE_Y"], d["BADGE_Z"]), 19, col="#d93030"), (35, 0, -240))
    add(66, "cable gland", cyl((-6, 45, 30), (6, 45, 30), 8, col=STL) + cyl((0, 45, 30), (3, 45, 30), 11, col=STL, shape="hex"), (-30, 0, -240))
    add(67, "mains cord", tube([(-6, 45, 30), (-32, 50, 20), (-60, 54, 8)], 7, BLK), (-55, 0, -240))
    add(73, "pressurestat", box(bx + 70, bx + 100, 30, 62, 14, 44, "#3a6fb0") + cyl((bx + 85, 30, 29), (bx + 85, 24, 29), 6, col=BRP, shape="hex"), (60, 70, -150))
    add(74, "pressurestat pipe", tube([(bx + 20, 10, 30), (bx + 30, 14, 26), (bx + 60, 20, 28), (bx + 85, 24, 29)], 4, CU), (60, 40, -150))
    add(75, "safety thermostat", cyl((bx - 20, -15, 26), (bx - 20, -15, 32), 8, col=STL), (0, -40, -150))
    # boiler bottom stack
    add(5, "boiler/base gasket", cyl((bx, 0, 65), (bx, 0, 67), 57, ri=41, col="#8a8a8a"), (0, 0, -18))
    add(5, "lower gasket", cyl((bx, 0, 62), (bx, 0, 64), 46.5, ri=40, col="#8a8a8a"), (0, 0, -50))
    F = cyl((bx, 0, 50), (bx, 0, 62), 49, ri=40, col=BRP)
    for k in range(3):
        a = math.radians(90 + 120 * k); c = (bx + 52 * math.cos(a), 52 * math.sin(a)); F += cyl((c[0], c[1], 50), (c[0], c[1], 62), 7, col=BRP)
    add(4, "fixing ring nut", F, (0, 0, -70))
    add(7, "element O-ring", cyl((bx, 0, 46), (bx, 0, 48), 38.5, ri=35, col=BLK), (0, 0, -90))
    F = cyl((bx, 0, 40), (bx, 0, 46), 42, col=STL)
    for k in range(3):
        a = math.radians(90 + 120 * k); c = (bx + 52 * math.cos(a), 52 * math.sin(a)); F += cyl((c[0], c[1], 40), (c[0], c[1], 46), 6.5, col=STL)
    for k in range(2):
        a = math.radians(45 + 180 * k); c = (bx + 17 * math.cos(a), 17 * math.sin(a)); F += cyl((c[0], c[1], 28), (c[0], c[1], 40), 3, col=STL)
    F += cyl((bx + 20, 10, 30), (bx + 20, 10, 40), 4, col=BRP)
    h1, _ = helix(bx, 0, 28, 60, 13, 6, 8, STL); F += h1 + tube([(bx + 28, 0, 46), (bx + 28, 0, 60)], 8, STL)
    add(6, "heating element 1000 W (SS)", F, (0, 0, -120))
    for k in range(3):
        a = math.radians(90 + 120 * k); c = (bx + 52 * math.cos(a), 52 * math.sin(a))
        add(8, "screw M5x12", cyl((c[0], c[1], 35), (c[0], c[1], 40), 4.2, col=STL) + cyl((c[0], c[1], 40), (c[0], c[1], 52), 2.5, col=STL), (0, 0, -160))
    # boiler
    add(3, "foot casting (brass)", cyl((bx, 0, 44), (bx, 0, 66), 40, ri=34, col=BRP) + cyl((bx, 0, 65), (bx, 0, 70), 56, ri=34, col=BRP)
        + cyl((bx, 0, 70), (bx, 0, 76), 56, 51, col=BRP))
    add(1, "lower shell (Cu)", cyl((bx, 0, 70), (bx, 0, d["SEAM_Z"]), 50, ri=48.5, col=COP, n=44))
    add(84, "seam ring (Cu)", cyl((bx, 0, d["SEAM_Z"] - 2), (bx, 0, d["SEAM_Z"] + 2), 50.7, ri=48.5, col=COP, n=44))
    add(85, "upper shell (Cu)", cyl((bx, 0, d["SEAM_Z"]), (bx, 0, d["SH_Z1"]), 50, ri=48.5, col=COP, n=44))
    F = cyl((bx, 0, d["SH_Z1"]), (bx, 0, d["SHO_Z"]), 50, 24, col=COP, n=44) + cyl((d["STK_X"], -12, 262), (d["STK_X"], -12, 266), 9, col=COP)
    F += cyl((d["SV_X"], d["SV_Y"], 258), (d["SV_X"], d["SV_Y"], 262), 9.5, col=COP)
    add(2, "dome (Cu)", F)
    add(86, "neck ring (brass)", cyl((bx, 0, d["SHO_Z"]), (bx, 0, d["NECK_Z"]), 23, ri=20, col=BRP), (0, 0, 14))
    add(69, "group boss (pad)", box(bx + 46, d["PAD_X1"], -30, 30, pz - 13, pz + 13, BRP))
    # sight glass + gauge
    sgx, sgy = d["SG_X"], d["SG_Y"]
    u = np.array([sgx - bx, sgy, 0.0]); u /= np.linalg.norm(u); sg = np.array([sgx, sgy, 0.0])
    S = lambda z, k=0: tuple(sg + u * k + np.array([0, 0, z]))
    for zc, tag in ((d["SG_Z0"], "lower"), (d["SG_Z1"], "upper")):
        add(19, f"sight-glass block ({tag})", box(sgx - 9, sgx + 9, sgy - 9, sgy + 9, zc - 9, zc + 9, BRP) + cyl(S(zc, -9), S(zc, -17), 6, col=BRP), tuple(u * 45))
        add(21, "nut D12 (M12x1)", cyl(S(zc, -18), S(zc, -14), 9.8, col=BRP, shape="hex"), tuple(u * 25))
        add(23, "PTFE washer", cyl(S(zc, -13.5), S(zc, -12.5), 9, ri=6, col=PTFE), tuple(u * 33))
    add(20, "glass nut M16x1", cyl(S(d["SG_Z0"] + 9), S(d["SG_Z0"] + 14), 9.8, col=BRP, shape="hex"), tuple(u * 45 + np.array([0, 0, 22])))
    add(20, "glass nut M16x1", cyl(S(d["SG_Z1"] - 14), S(d["SG_Z1"] - 9), 9.8, col=BRP, shape="hex"), tuple(u * 45 + np.array([0, 0, -22])))
    add(22, "glass seal", cyl(S(d["SG_Z0"] + 5), S(d["SG_Z0"] + 9), 8.5, ri=6, col=BLK), tuple(u * 62 + np.array([0, 0, 14])))
    add(22, "glass seal", cyl(S(d["SG_Z1"] - 9), S(d["SG_Z1"] - 5), 8.5, ri=6, col=BLK), tuple(u * 62 + np.array([0, 0, -14])))
    add(17, "sight glass tube", cyl(S(d["SG_Z0"] + 1), S(d["SG_Z1"] - 1), 6, ri=4.5, col=GLS), tuple(u * 80))
    add(18, "glass guard (clear PC)", cyl(S(d["SG_Z0"] + 14), S(d["SG_Z1"] - 14), 9, ri=8, col="#e6f4fa"), tuple(u * 98))
    add(70, "plug M10x1 (bottom)", cyl(S(d["SG_Z0"] - 15), S(d["SG_Z0"] - 9), 7, col=BRP), tuple(u * 45 + np.array([0, 0, -22])))
    add(72, "gauge adapter", cyl(S(d["SG_Z1"] + 9), S(d["GAUGE_Z"] - 22), 6, col=BRP) + cyl(S(d["GAUGE_Z"] - 22), S(d["GAUGE_Z"] - 16), 8.1, col=BRP, shape="hex"), (0, 0, 22))
    add(71, "pressure gauge Ø40", cyl((sgx, sgy + 12, d["GAUGE_Z"]), (sgx, sgy - 14, d["GAUGE_Z"]), 22, col=BRP)
        + cyl((sgx, sgy - 14, d["GAUGE_Z"]), (sgx, sgy - 14.6, d["GAUGE_Z"]), 19, col="#f8f8f0") + cyl(S(d["GAUGE_Z"] - 22), S(d["GAUGE_Z"] - 16), 3, col=BRP), (0, -20, 48))
    # cap
    zn = d["NECK_Z"]
    add(10, "cap gasket", cyl((bx, 0, zn), (bx, 0, zn + 2), 23, ri=20.25, col=BLK), (0, 0, 30))
    add(9, "cap insert", cyl((bx, 0, zn - 16), (bx, 0, zn + 2), 20, col=BRP) + cyl((bx, 0, zn + 2), (bx, 0, zn + 5), 23, col=BRP) + cyl((bx, 0, zn + 5), (bx, 0, zn + 11), 10, col=BRP), (0, 0, 50))
    add(11, "cap knob (wood)", cyl((bx, 0, zn + 5), (bx, 0, d["CAP_Z"]), 14, 19, col=WOOD) + cyl((bx, 0, d["CAP_Z"]), (bx, 0, d["TOP"]), 29, col=WOOD, shape="lobed"), (0, 0, 76))
    add(12, "cap screw M8x40", cyl((bx, 0, 333), (bx, 0, 341), 6.5, col=STL) + cyl((bx, 0, 300), (bx, 0, 333), 4, col=STL), (0, 0, 120))
    # safety valve with anti-vacuum
    sv = (d["SV_X"], d["SV_Y"])
    add(14, "valve poppet / anti-vac", cyl((sv[0], sv[1], 262), (sv[0], sv[1], 266), 3, col=STL), (0, 0, 20))
    add(13, "safety-valve body", cyl((sv[0], sv[1], 254), (sv[0], sv[1], 262), 6, col=BRP) + cyl((sv[0], sv[1], 262), (sv[0], sv[1], 268), 8.1, col=BRP, shape="hex"), (0, 0, 36))
    add(15, "valve spring", helix(sv[0], sv[1], 2.6, 266, 1.8, 7, 0.8, STL)[0], (0, 0, 54))
    add(16, "valve cup + exhaust tube", cyl((sv[0], sv[1], 268), (sv[0], sv[1], 290), 11, col=BRP)
        + tube([(sv[0] + 9, sv[1] + 6, 276), (136, 34, 266), (140, 36, 240), (140, 36, 120), (146, 36, 66)], 5, CU), (0, 0, 74))
    # steam valve (axis along Y), riser, knob, pipe, swivel, wand, frother
    z = d["STK_Z"]; x = d["STK_X"]
    add(87, "steam riser", cyl((x, -12, 262), (x, -12, z - 6), 7, col=BRP), (-24, 0, 0))
    add(25, "steam-valve body", cyl((x, d["STK_Y0"], z), (x, d["STK_Y1"], z), 7.5, col=BRP) + cyl((x, d["STK_Y0"], z), (x, d["STK_Y0"] - 8, z), 8, col=BRP, shape="hex"), (-24, 0, 30))
    add(28, "stem packing", cyl((x, d["STK_Y0"] - 8, z), (x, d["STK_Y0"] - 14, z), 6, ri=3.1, col=BLK), (-24, -30, 30))
    add(27, "packing nut M12x1", cyl((x, d["STK_Y0"] - 10, z), (x, d["STK_Y0"] - 16, z), 8.1, col=BRP, shape="hex"), (-24, -42, 30))
    add(26, "valve stem", cyl((x, d["STK_Y0"] + 30, z), (x, d["STK_KNOB_Y"] + 22, z), 3, col=STL), (-24, -56, 30))
    add(30, "steam knob (wood)", cyl((x, d["STK_KNOB_Y"] + 22, z), (x, d["STK_KNOB_Y"], z), 18.5, 15.5, col=WOOD, shape="lobed"), (-24, -80, 30))
    add(31, "knob pin", cyl((x - 16, d["STK_KNOB_Y"] + 11, z), (x + 16, d["STK_KNOB_Y"] + 11, z), 1.25, col=STL), (-50, -80, 30))
    add(88, "steam pipe", tube([(x, d["STK_Y1"], z), (x + 8, d["STK_Y1"] + 4, z), (150, 24, z)], 8, BRP), (0, 30, 30))
    add(33, "swivel", cyl((150, 24, z + 6), (150, 24, z - 6), 8.1, col=BRP, shape="hex"), (0, 50, 30))
    add(32, "steam wand", tube([(150, 24, z - 6), (156, 26, z - 14), (196, 34, 236)], 8, BRP), (0, 70, 10))
    add(34, "steam tip", sphere((196, 34, 232), 4.5, BRP), (0, 70, -6))
    add(89, "auto-frother", cyl((196, 34, 222), (196, 34, 242), 9, col=BRP), (30, 90, -40))
    # group joint (bolts in Y)
    G = np.array([95.0, 0, 0])
    add(44, "group-to-boiler O-ring", cyl((d["PAD_X1"] - 1, 0, pz), (d["PAD_X1"] + 0.5, 0, pz), 8.2, ri=5.5, col=BLK), (30, 0, 0))
    add(45, "pick-up tube", tube([(d["PAD_X1"] - 1.5, 0, pz), (110, 0, pz), (100, 0, pz - 10), (100, 0, 140)], 8, BRP), (0, -125, 0))
    for yy in (-22, 22):
        add(46, "hex bolt M6x10", cyl((d["FL_X1"], yy, pz), (d["FL_X1"] + 4, yy, pz), 5.77, col=STL, shape="hex") + cyl((d["FL_X1"] - 10, yy, pz), (d["FL_X1"], yy, pz), 3, col=STL), (55, 0, 0))
    F = (cyl((gx, 0, 176), (gx, 0, 198), 38, ri=31.5, col=BRP) + cyl((gx, 0, 198), (gx, 0, 210), 38, 29, col=BRP)
         + cyl((gx, 0, 210), (gx, 0, d["BODY_Z1"]), 29, col=BRP) + box(d["COL_X0"], d["COL_X1"], -8, 8, d["BODY_Z1"] - 4, d["YOKE_Z1"], BRP)
         + box(d["PAD_X1"], d["FL_X1"], -30, 30, pz - 13, pz + 13, BRP) + cyl((d["FL_X1"], 0, pz), (gx - 27, 0, pz), 11, col=BRP))
    add(35, "group body (brass)", F, tuple(G))
    add(76, "Teflon sleeve", cyl((gx, 0, 196), (gx, 0, 254), 25, ri=22, col=PTFE), tuple(G + [0, -125, 40]))
    add(77, "sleeve O-ring", cyl((gx, 0, 198), (gx, 0, 201.5), 25.5, ri=22.5, col=BLK), tuple(G + [0, -125, 10]))
    add(47, "check nut M8", cyl((gx, 0, 295), (gx, 0, 301), 7.5, col=BRP, shape="hex"), tuple(G + [0, 0, 30]))
    add(48, "acorn nut M8", cyl((gx, 0, 301), (gx, 0, d["ACORN_Z"] - 4), 7.5, col=BRP, shape="hex") + sphere((gx, 0, d["ACORN_Z"] - 4), 5.5, BRP), tuple(G + [0, 0, 48]))
    P = np.array([0, -190.0, 0]) + G
    add(36, "piston (brass)", cyl((gx, 0, 196.3), (gx, 0, 226.3), 21.95, col=BRP), tuple(P + [0, 0, -10]))
    add(37, "piston seal", cyl((gx, 0, 200.3), (gx, 0, 205.9), 22, ri=18, col=BLK), tuple(P + [0, 0, -38]))
    add(37, "piston seal", cyl((gx, 0, 213.3), (gx, 0, 218.9), 22, ri=18, col=BLK), tuple(P + [0, 0, -52]))
    add(38, "piston rod", cyl((gx, 0, 212.3), (gx, 0, 310), 5, col=STL), tuple(P + [0, 0, -10]))
    add(39, "rod seal", cyl((gx, 0, 256), (gx, 0, 260), 10, ri=5, col=PTFE), tuple(P + [0, 0, 42]))
    add(40, "brass washer with holes", cyl((gx, 0, 255), (gx, 0, 256), 10, ri=5.25, col=BRP), tuple(P + [0, 0, 50]))
    add(41, "C-clip 20 mm", cyl((gx, 0, 254), (gx, 0, 255), 10.5, ri=8.5, col=BLK), tuple(P + [0, 0, 58]))
    add(43, "shower screen Ø54", cyl((gx, 0, 194.3), (gx, 0, 195.3), 27, col=STL), tuple(G + [0, 0, -30]))
    add(42, "group gasket 60x50x5.5", cyl((gx, 0, 188.8), (gx, 0, 194.3), 30, ri=25, col=BLK), tuple(G + [0, 0, -46]))
    add(56, "basket double", cyl((gx, 0, 168), (gx, 0, 188), 23, 26, col=STL, ri=22), tuple(G + [0, 0, -68]))
    add(57, "basket single", cyl((gx, 0, 175), (gx, 0, 188), 22, 26, col=STL, ri=21), tuple(G + [0, 85, -68]))
    a = math.radians(d["PF_ANG"]); hu = np.array([math.cos(a), math.sin(a), 0])
    PFp = lambda r, zz: tuple(np.array([gx, 0, zz]) + hu * r)
    add(54, "portafilter body", cyl((gx, 0, 164), (gx, 0, 188.8), 29, 31, col=BRP, ri=27) + cyl((gx, 0, 160), (gx, 0, 164), 13, col=BRP) + cyl((gx, 0, 164), (gx, 0, 166), 29, col=BRP)
        + box(gx - 4, gx + 4, 30, 35, 181, 184.5, BRP) + box(gx - 4, gx + 4, -35, -30, 181, 184.5, BRP) + tube([PFp(30, 172), PFp(54, 170)], 15, BRP), tuple(G + [0, 0, -110]))
    add(55, "spout", cyl((gx, 0, 146), (gx, 0, 160), 6, 7, col=BRP) + tube([(gx, -5, 147), (gx, -15, 135)], 6, BRP) + tube([(gx, 5, 147), (gx, 15, 135)], 6, BRP), tuple(G + [0, 0, -138]))
    add(59, "handle stud M8", tube([PFp(42, 171), PFp(118, 167)], 8, STL), tuple(G + [0, 0, -110] + hu * 25))
    add(60, "PF handle (wood)", tube([PFp(54, 170), PFp(154, 165)], 26, WOOD), tuple(G + [0, 0, -110] + hu * 50))
    la = math.radians(d["LEV_ANG"]); lv = np.array([math.cos(la), 0, -math.sin(la)]); Fp = np.array([d["FX"], 0, d["FZ"]])
    q = lambda r: tuple(Fp + lv * r)
    L = G + [0, 0, 85]
    add(49, "lever (brass)", tube([q(-14), q(60)], 22, "#c9a440") + tube([q(55), q(d["LEV_L"] - d["HANDLE_L"] + 4)], 11, BRP), tuple(L))
    add(53, "lever handle (wood)", tube([q(d["LEV_L"] - d["HANDLE_L"]), q(d["LEV_L"])], d["HANDLE_D"], WOOD), tuple(L + lv * 45))
    for pp, tag in ((Fp, "fulcrum"), (np.array([d["ROD_PIN_X"], 0, d["ROD_PIN_Z"]]), "rod pin")):
        add(50, f"pin Ø6x34 ({tag})", cyl(tuple(pp + [0, -16, 0]), tuple(pp + [0, 16, 0]), 3, col=STL), tuple(L + [0, -48, 0]))
        add(51, "E-clip DIN 6799-5", cyl(tuple(pp + [0, -15, 0]), tuple(pp + [0, -14.3, 0]), 4.5, ri=2.5, col=BLK), tuple(L + [0, -70, 0]))
        add(51, "E-clip DIN 6799-5", cyl(tuple(pp + [0, 14.3, 0]), tuple(pp + [0, 15, 0]), 4.5, ri=2.5, col=BLK), tuple(L + [0, 30, 0]))
    add(52, "roller Ø10x16", cyl(tuple(Fp + [0, -8, 0]), tuple(Fp + [0, 8, 0]), 5, ri=3.05, col=BRP), tuple(L + [0, -28, 0]))
    return I

'''
s = s[:i] + new + s[j:]
s = s.replace('"ISOMETRIC VIEW - ASSEMBLED (viewed from front-left-above)"', '"ISOMETRIC VIEW - ASSEMBLED (front-left-above)"')
s = s.replace('"Shaded projection of the itemised 3D", "model (75 item numbers). Every item"', '"Shaded projection of the itemised 3D", "model (89 item numbers). Every item"')
s = s.replace('iso_dim(sh.ax, s, ox, oy, (0, -95, 0), (270, -95, 0), (0, -25, 0), "270 base [D]")', 'iso_dim(sh.ax, s, ox, oy, (0, -105, 0), (290, -105, 0), (0, -25, 0), "290 base [D]")')
s = s.replace('iso_dim(sh.ax, s, ox, oy, (0, -90, 0), (0, -90, 320), (-30, 0, 0), "320 overall [D]")', 'iso_dim(sh.ax, s, ox, oy, (0, -100, 0), (0, -100, 345), (-30, 0, 0), "345 overall [V]")')
s = s.replace('iso_dim(sh.ax, s, ox, oy, (275, -90, 0), (275, 90, 0), (25, 0, 0), "180 [D]")', 'iso_dim(sh.ax, s, ox, oy, (295, -100, 0), (295, 100, 0), (25, 0, 0), "200 [D]")')
s = s.replace('cols = 2', 'cols = 2')
open('iso.py', 'w', encoding='utf-8').write(s)
print('ok')

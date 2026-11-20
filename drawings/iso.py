"""Itemised 3D model (every part, fastener, seal as its own item) + shaded isometric renderer.
Sheets: assembled isometric, exploded isometric with balloons."""
import math
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.patches import Circle
from views import D, rounded_trap, lobed, hexagon

CHR, BRS, WOOD, BASEC, RUB, STL, BLK, GLS, CU, PTFE = ("#dcdcdc", "#d9b56a", "#c99a62", "#9fdcc8", "#333333", "#b8b8b8", "#2a2a2a",
                                                      "#cfe8f5", "#c87f4a", "#f2f2f2")
def _rgb(h): h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])

# ------------------------------------------------------------------ mesh primitives -> faces [(pts(N,3), colour)]
def _basis(a):
    a = a / np.linalg.norm(a); t = np.array([0, 0, 1.0]) if abs(a[2]) < 0.9 else np.array([1.0, 0, 0])
    e1 = np.cross(a, t); e1 /= np.linalg.norm(e1); e2 = np.cross(a, e1); return a, e1, e2

def _profile(shape, n):
    if shape == "hex": return [(math.cos(math.radians(30 + 60 * i)), math.sin(math.radians(30 + 60 * i))) for i in range(6)]
    if shape == "lobed": return [(u, v) for u, v in lobed(0, 0, 1, m=48)]
    return [(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n)]

def cyl(A, B, r0, r1=None, col=CHR, shape="round", n=28, ri=0.0, caps=True):
    """Frustum / tube between A and B. ri>0 -> annulus (hollow)."""
    r1 = r0 if r1 is None else r1
    A, B = np.array(A, float), np.array(B, float); a, e1, e2 = _basis(B - A)
    pr = _profile(shape, n); m = len(pr)
    P0 = [A + r0 * (u * e1 + v * e2) for u, v in pr]; P1 = [B + r1 * (u * e1 + v * e2) for u, v in pr]
    F = [(np.array([P0[i], P0[(i + 1) % m], P1[(i + 1) % m], P1[i]]), col) for i in range(m)]
    if ri > 0:
        Q0 = [A + ri * (u * e1 + v * e2) for u, v in _profile("round", n)]; Q1 = [B + ri * (u * e1 + v * e2) for u, v in _profile("round", n)]
        pr2 = _profile("round", n)
        if shape != "round": P0 = [A + r0 * (u * e1 + v * e2) for u, v in pr2]; P1 = [B + r1 * (u * e1 + v * e2) for u, v in pr2]
        F += [(np.array([Q0[(i + 1) % n], Q0[i], Q1[i], Q1[(i + 1) % n]]), col) for i in range(n)]
        if caps:
            F += [(np.array([P0[i], Q0[i], Q0[(i + 1) % n], P0[(i + 1) % n]]), col) for i in range(n)]
            F += [(np.array([P1[(i + 1) % n], Q1[(i + 1) % n], Q1[i], P1[i]]), col) for i in range(n)]
    elif caps:
        for P, c in ((P0, A), (P1, B)):
            F += [(np.array([c, P[i], P[(i + 1) % m]]), col) for i in range(m)]
    return F

def loft(p0, z0, p1, z1, col=BASEC, top=True, bottom=True):
    m = len(p0); P0 = [np.array([x, y, z0]) for x, y in p0]; P1 = [np.array([x, y, z1]) for x, y in p1]
    F = [(np.array([P0[i], P0[(i + 1) % m], P1[(i + 1) % m], P1[i]]), col) for i in range(m)]
    for P, ok in ((P0, bottom), (P1, top)):
        if not ok: continue
        c = sum(P) / m; F += [(np.array([c, P[i], P[(i + 1) % m]]), col) for i in range(m)]
    return F

def box(x0, x1, y0, y1, z0, z1, col=CHR):
    r = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]; return loft(r, z0, r, z1, col)

def tube(pts, d, col=CHR, n=10):
    F = []
    for a, b in zip(pts[:-1], pts[1:]): F += cyl(a, b, d / 2, col=col, n=n, caps=False)
    for p in pts[1:-1] + [pts[0], pts[-1]]: F += sphere(p, d / 2, col, 6, 8)
    return F

def sphere(c, r, col=CHR, nl=8, nm=12):
    c = np.array(c, float); F = []
    for i in range(nl):
        t0, t1 = math.pi * i / nl - math.pi / 2, math.pi * (i + 1) / nl - math.pi / 2
        for j in range(nm):
            p0, p1 = 2 * math.pi * j / nm, 2 * math.pi * (j + 1) / nm
            q = lambda t, p: c + r * np.array([math.cos(t) * math.cos(p), math.cos(t) * math.sin(p), math.sin(t)])
            F.append((np.array([q(t0, p0), q(t0, p1), q(t1, p1), q(t1, p0)]), col))
    return F

def helix(cx, cy, R, z0, pitch, turns, d, col=CU, seg=20):
    pts = [(cx + R * math.cos(2 * math.pi * k / seg), cy + R * math.sin(2 * math.pi * k / seg), z0 + pitch * k / seg) for k in range(int(turns * seg) + 1)]
    return tube(pts, d, col, n=8), pts

# ------------------------------------------------------------------ itemised model
def items():
    d = D; bx, gx, pz = d["BX"], d["GX"], d["PORT_Z"]
    I = []   # (item, label, faces, explode(dx,dy,dz))
    add = lambda it, lab, F, ex=(0, 0, 0): I.append((it, lab, F, np.array(ex, float)))
    # ---- base group
    add(63, "rubber cover", loft(rounded_trap(184, 174, 274, 52, x0=-2), 0, rounded_trap(184, 174, 274, 52, x0=-2), 12, RUB), (0, 0, -300))
    add(61, "base", loft(rounded_trap(180, 170, 270, 50), 8, rounded_trap(168, 158, 258, 44, x0=6), 60, BASEC), (0, 0, -235))
    g = rounded_trap(112, 108, 141, 26, x0=d["TRAY_X0"])
    F = loft(g, 60.2, g, 61.0, "#c4c4c4")
    for i in range(10):
        for j in range(8):
            if abs(i - 4.5) < 1 and abs(j - 3.5) < 1: continue
            F += cyl((d["TRAY_X0"] + 12 + i * 13, -44 + j * 12.6, 61.01), (d["TRAY_X0"] + 12 + i * 13, -44 + j * 12.6, 61.1), 4, col="#555555", n=10)
    add(62, "drip grid", F, (0, 0, -205))
    sx, sz = d["SW_X"], d["SW_Z"]
    add(65, "switch", box(sx - 17, sx + 17, -90.5, -87, sz - 13, sz + 13, BLK) + box(sx - 15, sx + 15, -91.5, -90.4, sz, sz + 11, "#e03030")
        + box(sx - 15, sx + 15, -91.5, -90.4, sz - 11, sz, "#f3eedd"), (0, -45, -235))
    add(64, "badge", cyl((265, d["BADGE_Y"], d["BADGE_Z"]), (268.5, d["BADGE_Y"], d["BADGE_Z"]), 19, col="#d93030"), (35, 0, -235))
    add(66, "cable gland", cyl((-9, 40, 25), (3, 40, 25), 8, col=STL) + cyl((-3, 40, 25), (0, 40, 25), 11, col=STL, shape="hex"), (-30, 0, -235))
    add(67, "mains cord", tube([(-9, 40, 25), (-35, 46, 18), (-60, 52, 8)], 7, "#f4f4f4"), (-55, 0, -235))
    add(5, "upper gasket", cyl((bx, 0, 60), (bx, 0, 62), 46.5, ri=40, col="#8a8a8a"), (0, 0, -18))
    add(5, "lower gasket", cyl((bx, 0, 57), (bx, 0, 59), 46.5, ri=40, col="#8a8a8a"), (0, 0, -42))
    F = cyl((bx, 0, 45), (bx, 0, 57), 49, ri=40, col=BRS)
    for k in range(3):
        a = math.radians(90 + 120 * k); c = (bx + 52 * math.cos(a), 52 * math.sin(a))
        F += cyl((c[0], c[1], 45), (c[0], c[1], 57), 7, col=BRS)
    add(4, "ring nut", F, (0, 0, -62))
    add(7, "element gasket", cyl((bx, 0, 40), (bx, 0, 42), 41, ri=34, col="#8a8a8a"), (0, 0, -80))
    F = cyl((bx, 0, 32), (bx, 0, 40), 42, col=BRS)
    for k in range(3):
        a = math.radians(90 + 120 * k); c = (bx + 52 * math.cos(a), 52 * math.sin(a))
        F += cyl((c[0], c[1], 32), (c[0], c[1], 40), 6.5, col=BRS)
    for k in range(4):
        a = math.radians(45 + 90 * k); c = (bx + 17 * math.cos(a), 17 * math.sin(a))
        F += cyl((c[0], c[1], 14), (c[0], c[1], 32), 4, col="#f6f6f6") + cyl((c[0], c[1], 8), (c[0], c[1], 14), 1.5, col=STL)
    h1, _ = helix(bx, 0, 26, 52, 12, 6, 8); h2, _ = helix(bx, 0, 15, 52, 12, 4, 8)
    F += h1 + h2 + tube([(bx + 26, 0, 40), (bx + 26, 0, 52)], 8, CU) + tube([(bx + 15, 0, 40), (bx + 15, 0, 52)], 8, CU)
    add(6, "heating element", F, (0, 0, -118))
    for k in range(3):
        a = math.radians(90 + 120 * k); c = (bx + 52 * math.cos(a), 52 * math.sin(a))
        add(8, "element screw M6x16", cyl((c[0], c[1], 26), (c[0], c[1], 32), 5, col=STL) + cyl((c[0], c[1], 32), (c[0], c[1], 48), 3, col=STL), (0, 0, -160))
    # ---- boiler
    add(3, "foot casting", cyl((bx, 0, 42), (bx, 0, 62), 40, ri=34, col=BRS) + cyl((bx, 0, 62), (bx, 0, 65), 46, ri=34, col=CHR)
        + cyl((bx, 0, 65), (bx, 0, 71), 46, 39.5, col=CHR))
    add(1, "boiler shell", cyl((bx, 0, 67), (bx, 0, d["SHELL_TOP"]), 38, ri=36.5, col=CHR, n=40))
    F = cyl((bx, 0, d["SHELL_TOP"]), (bx, 0, 240), 38, col=CHR, n=40) + cyl((bx, 0, 240), (bx, 0, 263), 38, 22, col=CHR, n=40)
    F += cyl((bx, 0, 263), (bx, 0, 273), 22, ri=19, col=CHR) + cyl((bx - 21, 0, 268), (bx - 23, 0, 268), 9, col=CHR)
    F += cyl((d["SV_X"], d["SV_Y"], 246), (d["SV_X"], d["SV_Y"], 252), 9.5, col=CHR)
    add(2, "shoulder / neck casting", F)
    add(69, "group boss (pad)", box(bx + 38, d["PAD_X1"], -13, 13, pz - 24, pz + 24, CHR))
    # sight glass
    u = np.array([d["SG_X"] - bx, d["SG_Y"], 0.0]); u /= np.linalg.norm(u); sg = np.array([d["SG_X"], d["SG_Y"], 0.0])
    S = lambda z, k=0: tuple(sg + u * k + np.array([0, 0, z]))
    for zc, tag in ((d["SG_Z0"], "lower"), (d["SG_Z1"], "upper")):
        add(19, f"sight-glass block ({tag})", box(sg[0] - 9, sg[0] + 9, sg[1] - 9, sg[1] + 9, zc - 9, zc + 9, CHR)
            + cyl(S(zc, -9), S(zc, -17), 6, col=BRS), tuple(u * 45))
        add(21, "lock nut M12x1", cyl(S(zc, -18), S(zc, -14), 9.8, col=BRS, shape="hex"), tuple(u * 25))
        add(23, "PTFE washer", cyl(S(zc, -13.5), S(zc, -12.5), 9, ri=6, col=PTFE), tuple(u * 33))
    add(20, "gland nut M16x1", cyl(S(122), S(127), 9.8, col=CHR, shape="hex"), tuple(u * 45 + np.array([0, 0, 22])))
    add(20, "gland nut M16x1", cyl(S(224), S(229), 9.8, col=CHR, shape="hex"), tuple(u * 45 + np.array([0, 0, -22])))
    add(22, "glass seal", cyl(S(118), S(122), 8.5, ri=6, col=BLK), tuple(u * 62 + np.array([0, 0, 14])))
    add(22, "glass seal", cyl(S(229), S(233), 8.5, ri=6, col=BLK), tuple(u * 62 + np.array([0, 0, -14])))
    add(17, "sight glass tube", cyl(S(114.5), S(237.5), 6, ri=4.5, col=GLS), tuple(u * 80))
    add(18, "glass guard", cyl(S(127), S(224), 8, ri=7.2, col=CHR), tuple(u * 98))
    add(24, "plug M10x1 (top)", cyl(S(247), S(253), 7, col=CHR), tuple(u * 45 + np.array([0, 0, 22])))
    add(70, "plug M10x1 (bottom)", cyl(S(98), S(104), 7, col=CHR), tuple(u * 45 + np.array([0, 0, -22])))
    # cap
    zn = d["NECK_Z"]
    add(10, "cap gasket", cyl((bx, 0, zn), (bx, 0, zn + 2), 22, ri=19.25, col=BLK), (0, 0, 24))
    add(9, "cap insert", cyl((bx, 0, zn - 16), (bx, 0, zn + 2), 19, col=BRS) + cyl((bx, 0, zn + 2), (bx, 0, zn + 5), 22, col=BRS)
        + cyl((bx, 0, zn + 5), (bx, 0, zn + 11), 10, col=BRS), (0, 0, 42))
    add(11, "cap knob", cyl((bx, 0, zn + 5), (bx, 0, d["CAP_Z"]), 14, 19, col=WOOD) + cyl((bx, 0, d["CAP_Z"]), (bx, 0, d["TOP"]), 29, col=WOOD, shape="lobed"), (0, 0, 66))
    add(12, "cap screw M8x35", cyl((bx, 0, 309), (bx, 0, 317), 6.5, col=STL) + cyl((bx, 0, 282), (bx, 0, 309), 4, col=STL), (0, 0, 110))
    # safety valve
    sv = (d["SV_X"], d["SV_Y"])
    add(14, "valve ball Ø6", sphere((sv[0], sv[1], 250), 3, STL), (0, 0, 18))
    add(13, "safety-valve body", cyl((sv[0], sv[1], 244), (sv[0], sv[1], 252), 6, col=BRS) + cyl((sv[0], sv[1], 252), (sv[0], sv[1], 258), 8.1, col=CHR, shape="hex")
        + cyl((sv[0], sv[1], 258), (sv[0], sv[1], 266), 5, col=CHR), (0, 0, 34))
    add(15, "valve spring", helix(sv[0], sv[1], 2.6, 253, 1.8, 7, 0.8, STL)[0], (0, 0, 52))
    add(16, "valve cup + drain tube", cyl((sv[0], sv[1], 262), (sv[0], sv[1], 286), 11, col=CHR)
        + tube([(sv[0] + 9, sv[1] + 6, 270), (118, 26, 262), (124, 26, 236), (124, 26, 120), (128, 26, 62)], 5, CU), (0, 0, 72))
    # steam valve (rear)
    z = d["STK_Z"]
    add(25, "steam-valve body", cyl((bx - 22, 0, z), (bx - 28, 0, z), 9.8, col=CHR, shape="hex") + cyl((bx - 28, 0, z), (10, 0, z), 7.5, col=CHR)
        + cyl((18, 0, z - 7), (18, 0, z - 15), 7, col=CHR), (-22, 0, 0))
    add(29, "stem washer", cyl((8, 0, z), (7.2, 0, z), 6, ri=3.1, col=BRS), (-40, 0, 0))
    add(28, "stem packing", cyl((7, 0, z), (1, 0, z), 6, ri=3.1, col=BLK), (-48, 0, 0))
    add(27, "packing nut M12x1", cyl((10, 0, z), (2, 0, z), 8.1, col=CHR, shape="hex"), (-62, 0, 0))
    add(26, "valve stem", cyl((45, 0, z), (-4, 0, z), 3, col=STL), (-80, 0, 0))
    add(30, "steam knob", cyl((-4, 0, z), (d["STK_X0"], 0, z), 18.5, 15.5, col=WOOD, shape="lobed"), (-108, 0, 0))
    add(31, "knob pin Ø2.5x30", cyl((-15, -8, z), (-15, 8, z), 1.25, col=STL), (-108, -38, 0))
    add(33, "wand union nut", cyl((18, 0, z - 15), (18, 0, z - 23), 9.8, col=CHR, shape="hex"), (-15, -50, -22))
    add(32, "steam wand", tube([(18, 0, z - 23), (18, 0, 212), (16, -22, 178), (14, -34, 136), (18, -38, 124)], 8, CHR), (-15, -50, -40))
    add(34, "steam tip", sphere((18, -38, 124), 4.5, CHR), (-15, -50, -58))
    # ---- group joint
    G = np.array([95.0, 0, 0])
    add(44, "port seal / Cu washer", cyl((d["PAD_X1"] - 1, 0, pz), (d["PAD_X1"] + 0.5, 0, pz), 8.2, ri=4.1, col=CU), (30, 0, 0))
    add(45, "L-tube", tube([(d["PAD_X1"] - 1.5, 0, pz), (96, 0, pz), (88, 0, pz - 4), (86, 0, pz - 12), (86, 0, 140)], 8, BRS)
        + cyl((d["PAD_X1"] - 2.5, 0, pz), (d["PAD_X1"] - 1, 0, pz), 6, col=BRS), (0, -115, 0))
    for zz in (pz - 19, pz + 19):
        add(46, "hex bolt M6x10 A2-70", cyl((d["FL_X1"], 0, zz), (d["FL_X1"] + 4, 0, zz), 5.77, col=STL, shape="hex")
            + cyl((d["FL_X1"] - 10, 0, zz), (d["FL_X1"], 0, zz), 3, col=STL), (55, 0, 0))
    F = (cyl((gx, 0, 176), (gx, 0, 196), 36, ri=29, col=CHR) + cyl((gx, 0, 196), (gx, 0, 206), 36, 25, col=CHR)
         + cyl((gx, 0, 206), (gx, 0, d["BODY_Z1"]), 25, col=CHR)
         + box(d["COL_X0"], d["COL_X1"], -8, 8, d["BODY_Z1"] - 4, d["YOKE_Z1"], CHR)
         + box(d["PAD_X1"], d["FL_X1"], -13, 13, pz - 24, pz + 24, CHR) + cyl((d["FL_X1"], 0, pz), (131, 0, pz), 11, col=CHR))
    add(35, "group body", F, tuple(G))
    add(47, "check nut M8", cyl((gx, 0, 294), (gx, 0, 300), 7.5, col=CHR, shape="hex"), tuple(G + [0, 0, 30]))
    add(48, "acorn nut M8", cyl((gx, 0, 300), (gx, 0, d["ACORN_Z"] - 4), 7.5, col=CHR, shape="hex")
        + sphere((gx, 0, d["ACORN_Z"] - 4), 5.5, CHR), tuple(G + [0, 0, 48]))
    P = np.array([0, -125.0, 0]) + G
    add(36, "piston", cyl((gx, 0, 194.3), (gx, 0, 224.3), 21.95, col=BRS), tuple(P + [0, 0, -10]))
    add(37, "piston seal", cyl((gx, 0, 198.3), (gx, 0, 203.9), 22, ri=18, col=BLK), tuple(P + [0, 0, -38]))
    add(37, "piston seal", cyl((gx, 0, 211.3), (gx, 0, 216.9), 22, ri=18, col=BLK), tuple(P + [0, 0, -52]))
    add(38, "piston rod", cyl((gx, 0, 210.3), (gx, 0, 308.3), 5, col=STL), tuple(P + [0, 0, -10]))
    add(39, "rod seal", cyl((gx, 0, 254), (gx, 0, 258), 10, ri=5, col=PTFE), tuple(P + [0, 0, 42]))
    add(40, "rod washer", cyl((gx, 0, 253), (gx, 0, 254), 10, ri=5.25, col=STL), tuple(P + [0, 0, 50]))
    add(41, "circlip DIN 472-20", cyl((gx, 0, 252), (gx, 0, 253), 10.5, ri=8.5, col=BLK), tuple(P + [0, 0, 58]))
    add(43, "shower screen", cyl((gx, 0, 193.3), (gx, 0, 194.3), 26, col=STL), tuple(G + [0, 0, -30]))
    add(42, "group gasket", cyl((gx, 0, 188), (gx, 0, 193.3), 28.85, ri=23.5, col=BLK), tuple(G + [0, 0, -46]))
    add(56, "basket double", cyl((gx, 0, 168), (gx, 0, 187), 22, 24.5, col=STL, ri=21), tuple(G + [0, 0, -66]))
    add(57, "basket single", cyl((gx, 0, 174), (gx, 0, 187), 21, 24.5, col=STL, ri=20), tuple(G + [0, 80, -66]))
    add(58, "basket spring", cyl((gx, 0, 182), (gx, 0, 183), 26, ri=25, col=STL), tuple(G + [0, 0, -80]))
    a = math.radians(d["PF_ANG"]); hu = np.array([math.cos(a), math.sin(a), 0])
    PFp = lambda r, zz: tuple(np.array([gx, 0, zz]) + hu * r)
    add(54, "portafilter body", cyl((gx, 0, 164), (gx, 0, 188), 28, 30, col=CHR, ri=26) + cyl((gx, 0, 160), (gx, 0, 164), 13, col=CHR) + cyl((gx, 0, 164), (gx, 0, 166), 28, col=CHR)
        + box(gx - 4, gx + 4, 28, 33, 180, 183.5, CHR) + box(gx - 4, gx + 4, -33, -28, 180, 183.5, CHR) + tube([PFp(28, 172), PFp(52, 170)], 15, CHR),
        tuple(G + [0, 0, -105]))
    add(55, "spout", cyl((gx, 0, 146), (gx, 0, 160), 6, 7, col=CHR) + tube([(gx, -5, 147), (gx, -15, 135)], 6, CHR) + tube([(gx, 5, 147), (gx, 15, 135)], 6, CHR),
        tuple(G + [0, 0, -132]))
    add(59, "handle stud M8x75", tube([PFp(40, 171), PFp(115, 167)], 8, STL), tuple(G + [0, 0, -105] + hu * 25))
    add(60, "PF handle", tube([PFp(52, 170), PFp(152, 165)], 24, WOOD), tuple(G + [0, 0, -105] + hu * 50))
    la = math.radians(d["LEV_ANG"]); lv = np.array([math.cos(la), 0, -math.sin(la)]); Fp = np.array([d["FX"], 0, d["FZ"]])
    q = lambda r: tuple(Fp + lv * r)
    L = G + [0, 0, 85]
    add(49, "lever (fork + rod)", tube([q(-14), q(60)], 22, BLK) + tube([q(55), q(d["LEV_L"] - d["HANDLE_L"] + 4)], 11, CHR), tuple(L))
    add(53, "lever handle", tube([q(d["LEV_L"] - d["HANDLE_L"]), q(d["LEV_L"])], d["HANDLE_D"], WOOD), tuple(L + lv * 45))
    for pp, tag in ((Fp, "fulcrum"), (np.array([d["ROD_PIN_X"], 0, d["ROD_PIN_Z"]]), "rod pin")):
        add(50, f"pin Ø6x34 ({tag})", cyl(tuple(pp + [0, -16, 0]), tuple(pp + [0, 16, 0]), 3, col=STL), tuple(L + [0, -48, 0]))
        add(51, "E-clip DIN 6799-5", cyl(tuple(pp + [0, -15, 0]), tuple(pp + [0, -14.3, 0]), 4.5, ri=2.5, col=BLK), tuple(L + [0, -70, 0]))
        add(51, "E-clip DIN 6799-5", cyl(tuple(pp + [0, 14.3, 0]), tuple(pp + [0, 15, 0]), 4.5, ri=2.5, col=BLK), tuple(L + [0, 30, 0]))
    add(52, "roller Ø10x16", cyl(tuple(Fp + [0, -8, 0]), tuple(Fp + [0, 8, 0]), 5, ri=3.05, col=BRS), tuple(L + [0, -28, 0]))
    return I

# ------------------------------------------------------------------ renderer
VIEW = np.array([1.0, -1.0, 1.0]) / math.sqrt(3)
RIGHT = np.array([1.0, 1.0, 0]) / math.sqrt(2)
UP = np.cross(RIGHT, -VIEW); UP /= np.linalg.norm(UP)
if UP[2] < 0: UP = -UP
LIGHT = np.array([0.3, -0.7, 0.9]); LIGHT /= np.linalg.norm(LIGHT)

def project(p): return np.array([p @ RIGHT, p @ UP, p @ VIEW])

def render(ax, I, exploded, ox, oy, s, edge=True):
    polys, cols, depths = [], [], []
    centers = {}
    for it, lab, F, ex in I:
        off = ex if exploded else np.zeros(3)
        acc = []
        for pts, col in F:
            P = pts + off
            n = np.cross(P[1] - P[0], P[2] - P[0]); nn = np.linalg.norm(n)
            if nn < 1e-9 and len(P) > 3: n = np.cross(P[2] - P[0], P[3] - P[0]); nn = np.linalg.norm(n)
            if nn < 1e-9: continue
            n /= nn
            Q = np.array([project(p) for p in P]); acc.append(Q[:, :2].mean(axis=0))
            if n @ VIEW < -0.02: continue
            shade = 0.42 + 0.58 * max(0.0, n @ LIGHT) + 0.18 * max(0.0, n @ VIEW) ** 8
            c = np.clip(_rgb(col) * shade, 0, 1)
            polys.append([(ox + q[0] * s, oy + q[1] * s) for q in Q]); cols.append(c); depths.append(Q[:, 2].mean())
        if acc: centers.setdefault((it, lab, tuple(off)), np.mean(acc, axis=0))
    order = np.argsort(depths)
    pc = PolyCollection([polys[i] for i in order], facecolors=[cols[i] for i in order],
                        edgecolors=[tuple(np.clip(cols[i] * (0.55 if len(polys[i]) > 3 else 1.0), 0, 1)) for i in order] if edge else "none",
                        linewidths=[0.08 if len(polys[i]) > 3 else 0.15 for i in order], zorder=3)
    ax.add_collection(pc)
    return {k: (ox + v[0] * s, oy + v[1] * s) for k, v in centers.items()}

def extents(I, exploded):
    pts = []
    for it, lab, F, ex in I:
        off = ex if exploded else np.zeros(3)
        for P, _ in F[:: max(1, len(F) // 40)]:
            for p in P: pts.append(project(p + off)[:2])
    pts = np.array(pts); return pts.min(axis=0), pts.max(axis=0)

def fit(I, exploded, box_):
    (x0, y0, x1, y1) = box_; mn, mx = extents(I, exploded)
    s = min((x1 - x0) / (mx[0] - mn[0]), (y1 - y0) / (mx[1] - mn[1]))
    ox = x0 + ((x1 - x0) - (mx[0] - mn[0]) * s) / 2 - mn[0] * s; oy = y0 + ((y1 - y0) - (mx[1] - mn[1]) * s) / 2 - mn[1] * s
    return ox, oy, s

def iso_dim(ax, s, ox, oy, p0, p1, offv, txt):
    a = project(np.array(p0, float)); b = project(np.array(p1, float)); o = project(np.array(offv, float))
    A = (ox + (a[0] + o[0]) * s, oy + (a[1] + o[1]) * s); B = (ox + (b[0] + o[0]) * s, oy + (b[1] + o[1]) * s)
    for p, q in ((a, A), (b, B)):
        ax.plot([ox + p[0] * s, q[0]], [oy + p[1] * s, q[1]], lw=0.2, color="#0b3d91", zorder=20)
    ax.annotate("", xy=A, xytext=B, arrowprops=dict(arrowstyle="<|-|>", lw=0.4, color="#0b3d91", mutation_scale=5, shrinkA=0, shrinkB=0), zorder=21)
    ang = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
    if ang > 90 or ang < -90: ang -= 180
    ax.text((A[0] + B[0]) / 2, (A[1] + B[1]) / 2, txt, rotation=ang, fontsize=6, color="#0b3d91", ha="center", va="bottom", zorder=22,
            bbox=dict(fc="white", ec="none", pad=0.2))

def sheet_iso(pdf, Sheet):
    sh = Sheet(None, "ISOMETRIC VIEW - ASSEMBLED (viewed from front-left-above)", "NTS (approx. 1:2.3)")
    I = items(); ox, oy, s = fit(I, False, (30, 62, 330, 282))
    render(sh.ax, I, False, ox, oy, s)
    iso_dim(sh.ax, s, ox, oy, (0, -95, 0), (270, -95, 0), (0, -25, 0), "270 base [D]")
    iso_dim(sh.ax, s, ox, oy, (0, -90, 0), (0, -90, 320), (-30, 0, 0), "320 overall [D]")
    iso_dim(sh.ax, s, ox, oy, (275, -90, 0), (275, 90, 0), (25, 0, 0), "180 [D]")
    sh.ax.text(340, 282, "ISOMETRIC  (true iso, 35.26° / 45°)", fontsize=7, weight="bold", va="top")
    sh.ax.text(340, 276, "\n".join([
        "Shaded projection of the itemised 3D", "model (75 item numbers). Every item", "is drawn: castings, tubes, seals,",
        "screws, nuts, pins and clips.", "", "Viewer at (+X, -Y, +Z): front (user", "side) to the right, switch side", "facing you.",
        "", "See the exploded isometric for item", "call-outs and the part drawings for", "every dimension.", "",
        "Datums: Z0 table, X0 base rear,", "Y0 centre line (-Y switch side)."]), fontsize=5.4, va="top", linespacing=1.35)
    sh.save(pdf)

NAMES = {}
def sheet_exploded(pdf, Sheet):
    sh = Sheet(None, "EXPLODED ISOMETRIC - EVERY PART, FASTENER AND SEAL CALLED OUT", "NTS")
    I = items(); ox, oy, s = fit(I, True, (16, 58, 300, 284))
    C = render(sh.ax, I, True, ox, oy, s, edge=True)
    # balloons with simple repulsion
    keys = list(C.keys()); P = np.array([C[k] for k in keys]); cen = P.mean(axis=0)
    B = P + np.array([(p - cen) / (np.linalg.norm(p - cen) + 1e-6) * 9 for p in P])
    for _ in range(250):
        for i in range(len(B)):
            for j in range(i + 1, len(B)):
                dv = B[i] - B[j]; dd = np.linalg.norm(dv)
                if dd < 5.6:
                    push = (5.6 - dd) / 2 * (dv / (dd + 1e-6) if dd > 1e-6 else np.array([1.0, 0]))
                    B[i] += push; B[j] -= push
        B += (P - B) * 0.004
    for (it, lab, _), p, b in zip(keys, P, B):
        sh.ax.plot([p[0], b[0]], [p[1], b[1]], lw=0.25, color="#111111", zorder=30)
        sh.ax.add_patch(Circle(p, 0.35, color="#111111", zorder=30))
        sh.ax.add_patch(Circle(b, 2.5, fc="white", ec="#111111", lw=0.4, zorder=31))
        sh.ax.text(b[0], b[1], str(it), fontsize=4.3, ha="center", va="center", weight="bold", zorder=32)
        NAMES.setdefault(it, lab)
    # legend
    sh.ax.text(305, 284, "ITEM LEGEND (qty in BOM)", fontsize=6.5, weight="bold", va="top")
    its = sorted(NAMES.items()); col = 0
    for k, (it, lab) in enumerate(its):
        cx = 305 + (k // 42) * 52; cy = 278 - (k % 42) * 5.1
        sh.ax.text(cx, cy, f"{it:>2}  {lab}", fontsize=4.5, va="top", family="DejaVu Sans")
    sh.save(pdf)

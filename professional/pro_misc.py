"""Professional assembly sheets: boiler section, group section, joint, wiring, fasteners, schedules, BOM. SI units (mm, kPa, N·m, kg, L, °C)."""
import math
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle
from views import D
from partdraw import hdim, vdim, leader, cl, INK, DIMC, NOTE

BR, BR2, CUF, GK, ST, WD = "#f4e3b5", "#e6c98f", "#f2c4a6", "#bdbdbd", "#cfcfcf", "#c9956a"

def _p(ax, pts, fc, hatch=None, lw=0.6, z=3):
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=INK, lw=lw, hatch=hatch, zorder=z))

def zcolumn(ax, P, items, xr, title="Z (mm above table)"):
    ys = []
    for z, lab, xa in items:
        y = P(0, z)[1]; ly = max(y, (ys[-1] + 3.1) if ys else y); ys.append(ly)
        ax.plot([P(xa, z)[0], xr - 2], [y, y], lw=0.15, color=DIMC, zorder=20); ax.plot([xr - 2, xr], [y, ly], lw=0.15, color=DIMC, zorder=20)
        ax.text(xr + 1, ly, lab, fontsize=4.5, color=DIMC, va="center", zorder=22, bbox=dict(fc="white", ec="none", pad=0.1))
    ax.plot([xr - 2, xr - 2], [P(0, items[0][0])[1], P(0, items[-1][0])[1]], lw=0.25, color=DIMC)
    ax.text(xr - 2, max(ys) + 4, title, fontsize=5, color=DIMC, ha="center", weight="bold")

# ================================================================== BOILER SECTION
def sheet_boiler(pdf, Sheet):
    sh = Sheet(None, "BOILER ASSEMBLY - SECTION A-A (X-Z through boiler axis)", "1:1.82")
    ax = sh.ax; s = 0.55; ox, oy = 118, 58
    P = lambda x, z: (ox + x * s, oy + z * s)       # x = radial from boiler axis (+ = front)
    R = 50; t = 1.5
    # feet, sub-base, base
    _p(ax, [P(-80, 4), P(150, 4), P(150, 10), P(-80, 10)], "#3a3a3a"); _p(ax, [P(-60, 0), P(-42, 0), P(-42, 4), P(-60, 4)], "#3a3a3a")
    ax.plot(*zip(P(-80, 10), P(-73, 64), P(-41, 64)), lw=1.0, color="#9a7a20"); ax.plot(*zip(P(41, 64), P(150, 64)), lw=1.0, color="#9a7a20")
    # gaskets, ring nut, element
    for sg in (1, -1):
        _p(ax, [P(sg * 41, 65), P(sg * 56, 65), P(sg * 56, 67), P(sg * 41, 67)], GK, "xxxx", 0.4)
        _p(ax, [P(sg * 40, 61.5), P(sg * 46.5, 61.5), P(sg * 46.5, 63.5), P(sg * 40, 63.5)], GK, "xxxx", 0.4)
        _p(ax, [P(sg * 40, 49.5), P(sg * 49, 49.5), P(sg * 49, 61.5), P(sg * 40, 61.5)], BR, "////")
        _p(ax, [P(sg * 34, 44), P(sg * 40, 44), P(sg * 40, 67), P(sg * 56, 67), P(sg * 56, 72), P(sg * 51.5, 76), P(sg * 50, 76), P(sg * 50, 70), P(sg * 34, 70)], BR2, "\\\\\\\\")
        ax.add_patch(Circle(P(sg * 37, 45), 1.8 * s * 1.8, fc="#333", ec=INK, lw=0.3, zorder=5))
        _p(ax, [P(sg * 49, 38), P(sg * 59, 38), P(sg * 59, 44), P(sg * 49, 44)], ST)
        _p(ax, [P(sg * 50, 33), P(sg * 54, 33), P(sg * 54, 58), P(sg * 50, 58)], "#dddddd", lw=0.4, z=4)
    _p(ax, [P(-42, 38), P(42, 38), P(42, 44), P(-42, 44)], ST, "////")
    for i in range(6):
        z = 52 + i * 13
        for xx in (-28, 28): ax.add_patch(Circle(P(xx + (2 if i % 2 else -2), z), 4 * s, fc="#b9b9b9", ec=INK, lw=0.4, zorder=4))
    ax.plot(*zip(P(28, 44), P(28, 52)), lw=2, color="#999"); ax.plot(*zip(P(-28, 44), P(-28, 52)), lw=2, color="#999")
    ax.plot(*zip(P(20, 38), P(20, 30), P(60, 28), P(85, 29)), lw=1.6, color="#c87f4a", zorder=4)
    _p(ax, [P(85, 14), P(115, 14), P(115, 44), P(85, 44)], "#3a6fb0", lw=0.5, z=4); ax.text(*P(87, 38), "73", fontsize=5, color="white", weight="bold", zorder=6)
    _p(ax, [P(-28, 32), P(-12, 32), P(-12, 38), P(-28, 38)], "#999", lw=0.4, z=4)
    # shells, seam, dome, neck, cap
    for sg in (1, -1):
        _p(ax, [P(sg * (R - t), 70), P(sg * R, 70), P(sg * R, D["SEAM_Z"]), P(sg * (R - t), D["SEAM_Z"])], CUF, "////", 0.5)
        _p(ax, [P(sg * (R - t), D["SEAM_Z"]), P(sg * R, D["SEAM_Z"]), P(sg * R, 262), P(sg * (R - t), 262)], CUF, "////", 0.5)
        _p(ax, [P(sg * (R - 3), D["SEAM_Z"] - 5), P(sg * (R - t), D["SEAM_Z"] - 5), P(sg * (R - t), D["SEAM_Z"] + 5), P(sg * (R - 3), D["SEAM_Z"] + 5)], CUF, "\\\\\\\\", 0.4)
        _p(ax, [P(sg * R, 254), P(sg * 51.6, 254), P(sg * 51.6, 262), P(sg * 23, 274), P(sg * 21.5, 274), P(sg * R, 262.5)], CUF, "\\\\\\\\", 0.5)
        _p(ax, [P(sg * 20, 274), P(sg * 23, 274), P(sg * 23, 284), P(sg * 20, 284)], BR, "////", 0.5)
    _p(ax, [P(-19, 268), P(19, 268), P(19, 284), P(23, 286), P(23, 289), P(-23, 289), P(-23, 286), P(-19, 284)], BR2, "....")
    _p(ax, [P(-23, 284), P(-17, 284), P(-17, 286), P(-23, 286)], "#333", lw=0.3); _p(ax, [P(17, 284), P(23, 284), P(23, 286), P(17, 286)], "#333", lw=0.3)
    _p(ax, [P(-14, 289), P(14, 289), P(19, D["CAP_Z"]), P(29, D["CAP_Z"]), P(29, D["TOP"]), P(-29, D["TOP"]), P(-29, D["CAP_Z"]), P(-19, D["CAP_Z"])], WD, "----")
    ax.add_patch(Rectangle(P(-4, 278), 8 * s, 63 * s, fc="#cccccc", ec=INK, lw=0.4, zorder=4))
    # group side (right): boss + port + tube; sight glass left; valves on dome
    pz = D["PORT_Z"]
    _p(ax, [P(R, pz - 13), P(58, pz - 13), P(58, pz + 13), P(R, pz + 13)], BR2, "////")
    ax.add_patch(Rectangle(P(R, pz - 3), 8 * s, 6 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    ax.plot(*zip(P(56, pz), P(30, pz), P(20, pz - 10), P(20, 140)), lw=8 * s * 2.835 * 0.35, color="#b9975b", zorder=3)
    _p(ax, [P(58, pz - 13), P(63, pz - 13), P(63, pz + 13), P(58, pz + 13)], "#eeeeee", lw=0.4); ax.text(*P(64, pz + 15), "group (sheet 7-8)", fontsize=4.4)
    sgr = -math.hypot(D["SG_X"] - D["BX"], D["SG_Y"])
    for zc in (D["SG_Z0"], D["SG_Z1"]):
        _p(ax, [P(sgr - 9, zc - 9), P(sgr + 9, zc - 9), P(sgr + 9, zc + 9), P(sgr - 9, zc + 9)], BR2)
        _p(ax, [P(sgr + 9, zc - 5), P(-R + 1, zc - 5), P(-R + 1, zc + 5), P(sgr + 9, zc + 5)], "#e0c070", lw=0.4)
        _p(ax, [P(-R + 1.5, zc - 8.5), P(-R + 6, zc - 8.5), P(-R + 6, zc + 8.5), P(-R + 1.5, zc + 8.5)], BR, "////", 0.4)
    _p(ax, [P(sgr - 9, D["SG_Z0"] + 9), P(sgr + 9, D["SG_Z0"] + 9), P(sgr + 9, D["SG_Z1"] - 9), P(sgr - 9, D["SG_Z1"] - 9)], "#e6f4fa", lw=0.4)
    _p(ax, [P(sgr - 6, D["SG_Z0"] + 1), P(sgr + 6, D["SG_Z0"] + 1), P(sgr + 6, D["SG_Z1"] - 1), P(sgr - 6, D["SG_Z1"] - 1)], "white", lw=0.4, z=4)
    _p(ax, [P(sgr - 6, D["SG_Z1"] + 9), P(sgr + 6, D["SG_Z1"] + 9), P(sgr + 6, 260), P(sgr - 6, 260)], BR2, lw=0.4)
    ax.add_patch(Circle(P(sgr, D["GAUGE_Z"]), 22 * s, fc="#ecc865", ec=INK, lw=0.5, zorder=4)); ax.add_patch(Circle(P(sgr, D["GAUGE_Z"]), 19 * s, fc="#fbfbf3", ec=INK, lw=0.4, zorder=5))
    svr = math.hypot(D["SV_X"] - D["BX"], D["SV_Y"])
    _p(ax, [P(svr - 6, 256), P(svr + 6, 256), P(svr + 6, 268), P(svr - 6, 268)], BR2, "////", 0.4); _p(ax, [P(svr - 11, 268), P(svr + 11, 268), P(svr + 11, 290), P(svr - 11, 290)], BR2, lw=0.4)
    str_ = -math.hypot(D["STK_X"] - D["BX"], 12)
    _p(ax, [P(str_ - 7, 262), P(str_ + 7, 262), P(str_ + 7, 294), P(str_ - 7, 294)], BR2, "////", 0.4)
    _p(ax, [P(str_ - 22, 292.5), P(str_ + 22, 292.5), P(str_ + 22, 307.5), P(str_ - 22, 307.5)], BR2, lw=0.4)
    # water levels
    for z, lab in ((220, "MAX fill 1.1 L usable [D] (Z220)"), (140, "MIN: keep above pick-up tube end (Z140)")):
        ax.plot(*zip(P(-R + t, z), P(R - t, z)), lw=0.4, ls=(0, (6, 2)), color="#2a6fb0"); ax.text(*P(-46, z + 2), lab, fontsize=4.3, color="#2a6fb0")
    cl(ax, P(0, -4), P(0, 350))
    zcolumn(ax, P, [(0, "0 table (feet)", 0), (10, "10 sub-base top", 150), (38, "38 element flange", 59), (44, "44 spigot end / O-ring", 40),
                    (50, "50 ring nut", 49), (65, "65 base top", 150), (70, "70 lower shell", R), (76, "76 foot flare top", 56),
                    (D["SG_Z0"], f"{D['SG_Z0']} sight glass low", 50), (140, "140 pick-up tube end", 20), (D["SEAM_Z"], f"{D['SEAM_Z']} seam ring", R),
                    (pz, f"{pz} group port", 63), (D["SG_Z1"], f"{D['SG_Z1']} sight glass high", 50), (254, "254 dome skirt", R), (262, "262 shell top", R),
                    (274, "274 neck ring", 23), (D["GAUGE_Z"], f"{D['GAUGE_Z']} gauge C/L", 50), (284, "284 neck top", 23), (D["STK_Z"], f"{D['STK_Z']} steam valve C/L", 60),
                    (D["CAP_Z"], f"{D['CAP_Z']} knob lobes", 29), (D["TOP"], f"{D['TOP']} top", 29)], P(118, 0)[0])
    hdim(ax, P(-R, 0)[0], P(R, 0)[0], P(-R, 230)[1], P(R, 230)[1], P(0, 230)[1], "Ø100 shell [D]")
    hdim(ax, P(-40, 0)[0], P(40, 0)[0], P(-40, 44)[1], P(40, 44)[1], P(0, 0)[1] - 6, "M80 x 1.5 spigot [D]")
    hdim(ax, P(-56, 0)[0], P(56, 0)[0], P(-56, 76)[1], P(56, 76)[1], P(0, 0)[1] - 12, "Ø112 foot flare")
    sh.ax.text(250, 285, "NOTES - BOILER (SI units: mm, kPa, °C, L)", fontsize=7, weight="bold", va="top")
    sh.ax.text(250, 279, "\n".join([
        "1. Copper shell Ø100 x 1.5 in two lengths (lower 122, upper 70) joined",
        "   by an internal seam ring; foot, dome and neck ring silver-brazed.",
        "2. Boiler spigot M80 x 1.5 (coarse, 1996 on) and fixing ring are shared",
        "   with the Europiccola [D]; only the tank (Ø100) and upper gasket differ.",
        "3. Element 1000 W stainless, sealed by O-ring 3.53 x 73.98 on the spigot",
        "   face, pulled up by 3 x M5 x 12 screws into the ring-nut ears [D], 3 N·m.",
        "4. Pressurestat 73 fed by copper pipe 74 from the element port (G1/8);",
        "   cuts the element at ~90 kPa, cuts in at ~70 kPa (adjustable 50-120).",
        "5. Safety thermostat 75 (manual reset, 127 °C [D]) on the element flange.",
        "6. Safety valve 13 opens at ~150 kPa; its anti-vacuum poppet admits air",
        "   on cooling so the boiler cannot suck water back from the group.",
        f"7. Capacity check: Ø97 x 192 inside + dome = 1.5 L gross ~ 1.6 L [D].",
        "8. Sight glass, steam riser and safety valve are rotated into this plane.",
    ]), fontsize=5.3, va="top", linespacing=1.38)
    sh.save(pdf)

# ================================================================== GROUP SECTION (MILLENNIUM)
def sheet_group(pdf, Sheet):
    sh = Sheet(None, "BREW GROUP ASSEMBLY (MILLENNIUM) - SECTION B-B, lever at rest", "1:1")
    ax = sh.ax; z0 = D["BELL_Z0"]; gx = D["GX"]
    ox, oy = 128, 104
    P = lambda x, z: (ox + x, oy + z - z0)
    rb = D["BODY_D"] / 2; top = D["BODY_Z1"] - z0; sk, g1 = 12, 17.5; scr = g1 + 1; bt = top - 8
    for sg in (1, -1):
        prof = [(sg * 32.25, 0), (sg * 38, 0), (sg * 38, 22), (sg * rb, 34), (sg * rb, top), (sg * 5.25, top), (sg * 5.25, top - 2),
                (sg * 10, top - 2), (sg * 10, bt), (sg * 25.1, bt), (sg * 25.1, scr), (sg * 27, scr), (sg * 27, g1), (sg * 30, g1), (sg * 30, sk), (sg * 32.25, sk)]
        _p(ax, [P(x, z + z0) for x, z in prof], BR, "////")
        _p(ax, [P(sg * 22, z0 + scr), P(sg * 25, z0 + scr), P(sg * 25, z0 + bt), P(sg * 22, z0 + bt)], "#f8f8f8", "....", 0.4)
        ax.add_patch(Circle(P(sg * 23.6, z0 + scr + 3), 1.8, fc="#333", ec=INK, lw=0.3, zorder=5))
    pz = D["PORT_Z"]; fl0, fl1 = D["PAD_X1"] - gx, D["FL_X1"] - gx
    _p(ax, [P(fl0, pz - 13), P(fl1, pz - 13), P(fl1, pz - 11), P(-rb, pz - 11), P(-rb, pz + 11), P(fl1, pz + 11), P(fl1, pz + 13), P(fl0, pz + 13)], BR, "////")
    ax.add_patch(Rectangle(P(fl0, pz - 4), (-22 - fl0), 8, fc="#cfe8f5", ec=INK, lw=0.5, zorder=4))
    shx = D["BX"] + D["SH_D"] / 2 - gx
    _p(ax, [P(shx, pz - 13), P(fl0, pz - 13), P(fl0, pz + 13), P(shx, pz + 13)], BR2, "\\\\\\\\")
    _p(ax, [P(shx - 1.5, pz - 40), P(shx, pz - 40), P(shx, pz - 7), P(shx - 1.5, pz - 7)], CUF, "////"); _p(ax, [P(shx - 1.5, pz + 7), P(shx, pz + 7), P(shx, pz + 40), P(shx - 1.5, pz + 40)], CUF, "////")
    ax.plot(*zip(P(shx + 4, pz), P(-69, pz), P(-79, pz - 10), P(-79, pz - 60)), lw=8 * 2.835 * 0.35, color="#b9975b", zorder=2)
    pb = z0 + scr
    _p(ax, [P(-21.95, pb), P(21.95, pb), P(21.95, pb + 30), P(-21.95, pb + 30)], BR2, "\\\\\\\\")
    for g in (pb + 4, pb + 17):
        for sg in (1, -1): _p(ax, [P(sg * 22, g), P(sg * 18, g), P(sg * 18, g + 5.6), P(sg * 22, g + 5.6)], "#333", lw=0.4, z=4)
    rod0 = pb + 16
    ax.add_patch(Rectangle(P(-5, rod0), 10, 84.5, fc="#dddddd", ec=INK, lw=0.5, zorder=4)); ax.add_patch(Rectangle(P(-4, rod0 + 84.5), 8, 14, fc="#dddddd", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Circle(P(0, D["ROD_PIN_Z"]), 3.05, fc="white", ec=INK, lw=0.5, zorder=5))
    _p(ax, [P(-7.5, 295), P(7.5, 295), P(7.5, 301), P(-7.5, 301)], "#ecc865", z=5)
    _p(ax, [P(-7.5, 301), P(7.5, 301), P(7.5, 306), P(5, 310.5), P(0, 312), P(-5, 310.5), P(-7.5, 306)], "#ecc865", z=5)
    c0, c1 = D["COL_X0"] - gx, D["COL_X1"] - gx
    _p(ax, [P(c0, D["BODY_Z1"] - 4), P(c1, D["BODY_Z1"] - 4), P(c1, D["YOKE_Z1"]), P(c0, D["YOKE_Z1"])], "#f1e3b5")
    ax.add_patch(Circle(P(D["FX"] - gx, D["FZ"]), 5.05, fc=BR2, ec=INK, lw=0.5, zorder=5)); ax.add_patch(Circle(P(D["FX"] - gx, D["FZ"]), 3, fc=ST, ec=INK, lw=0.5, zorder=6))
    for sg in (1, -1):
        _p(ax, [P(sg * 27, 188.8), P(sg * 31, 188.8), P(sg * 29, 164), P(sg * 7, 160), P(sg * 7, 164), P(sg * 27, 166)], BR, "////")
        _p(ax, [P(sg * 25, 188), P(sg * 30, 188), P(sg * 30, 193.5), P(sg * 25, 193.5)], "#333")
    ax.add_patch(Rectangle(P(-27, 193.5), 54, 1, fc="#999", ec=INK, lw=0.3, zorder=5))
    ax.plot(*zip(P(-25.5, 188), P(-22, 168), P(22, 168), P(25.5, 188)), lw=0.7, color=INK, zorder=5)
    _p(ax, [P(-7, 160), P(7, 160), P(6, 146), P(-6, 146)], BR2, "////")
    ax.plot(*zip(P(-5, 147), P(-15, 135)), lw=1.8, color=INK); ax.plot(*zip(P(5, 147), P(15, 135)), lw=1.8, color=INK)
    cl(ax, P(0, 128), P(0, 318)); cl(ax, P(-85, pz), P(-15, pz))
    up = z0 + bt - 30
    zcolumn(ax, P, [(132, "132 spout tip", 15), (160, "160 PF bottom", 7), (176, "176 bell face", 38), (188, "188 gasket seat", 30), (193.5, "193.5 screen", 27),
                    (194.5, "194.5 piston face (rest)", 22), (198, "198 bell top", 38), (pz, f"{pz} port C/L", 25), (224.5, "224.5 piston top (rest)", 22),
                    (z0 + bt, f"{z0 + bt:g} sleeve top / C-clip", 25), (D["BODY_Z1"], f"{D['BODY_Z1']} body top", rb), (D["ROD_PIN_Z"], f"{D['ROD_PIN_Z']} rod pin", 5),
                    (D["FZ"], f"{D['FZ']} fulcrum", 0), (D["YOKE_Z1"], f"{D['YOKE_Z1']} column top", 0), (295, "295 check nut", 7.5), (312, "312 acorn top", 0)], P(50, 0)[0])
    vdim(ax, P(0, 194.5)[1], P(0, up)[1], P(-22, 194.5)[0], P(-22, up)[0], P(-32, 0)[0], f"stroke {up - 194.5:.1f}")
    hdim(ax, P(-22, 0)[0], P(22, 0)[0], P(-22, 236)[1], P(22, 236)[1], P(0, 236)[1], "Ø44 piston [D]")
    hdim(ax, P(-25, 0)[0], P(25, 0)[0], P(-25, 246)[1], P(25, 246)[1], P(0, 246)[1], "Ø50 sleeve")
    hdim(ax, P(-38, 0)[0], P(38, 0)[0], P(-38, 176)[1], P(38, 176)[1], P(0, 176)[1] - 26, "Ø76 bell")
    hdim(ax, P(-31, 0)[0], P(31, 0)[0], P(-31, 188.8)[1], P(31, 188.8)[1], P(0, 160)[1] - 6, "Ø62 portafilter (60 rim [D])")
    leader(ax, P(-23.6, z0 + scr + 3), (P(-90, 0)[0], P(0, 205)[1]), "77 sleeve O-ring (3.53 section [D])")
    leader(ax, P(-23, 230), (P(-90, 0)[0], P(0, 240)[1]), "76 Teflon sleeve, 2 inlet holes Ø6")
    leader(ax, P(8, z0 + top - 4), (P(30, 0)[0] + 10, P(0, 288)[1]), "41 C-clip / 40 washer / 39 lip seal")
    leader(ax, P(-28, 190), (P(-90, 0)[0], P(0, 186)[1]), "42 gasket 60 x 50 x 5.5 [D]")
    ax.text(14, 283, "NOTES", fontsize=7, weight="bold", va="top")
    disp = math.pi / 4 * 4.4 ** 2 * (up - 194.5) / 10
    ax.text(14, 277, "\n".join([
        f"Stroke {up - 194.5:.1f} mm: piston face 194.5 (lever down) -> {up:.1f} (lever up, piston top on C-clip).",
        f"Swept volume = π/4 x 44² x {up - 194.5:.1f} = {disp * 1000:.0f} mm³ = {disp:.0f} mL (Wright, millennium Professional: 43 mL [D]).",
        f"Port Ø8 at Z{pz} spans Z{pz - 4}-{pz + 4}: fully open when piston face is above Z{pz + 4}.",
        "The Teflon sleeve insulates the brew water from the hot group (Millennium change, 2001) [D].",
        "Group bolts are side by side (Y = ±22), not visible in this plane - see joint sheet."]), fontsize=5.2, va="top", linespacing=1.38)
    sh.save(pdf)

# ================================================================== GROUP-TO-BOILER JOINT (bolts in Y)
def sheet_joint(pdf, Sheet):
    sh = Sheet(None, "GROUP-TO-BOILER JOINT - boss, flange, side bolts, O-ring", "2:1")
    ax = sh.ax; gx = D["GX"]; pz = D["PORT_Z"]; X0 = D["BX"]; s = 2.0
    shx = X0 + 50; fl1 = D["FL_X1"]; px1 = D["PAD_X1"]; bw = gx - D["BODY_D"] / 2
    ox, oy = 40 - 112 * s, 150
    P = lambda x, y: (ox + x * s, oy + y * s)
    arc = [(X0 + 50 * math.cos(t), 50 * math.sin(t)) for t in np.linspace(-0.75, 0.75, 50)]
    _p(ax, [P(*p) for p in arc] + [P(X0 + 48.5 * math.cos(t), 48.5 * math.sin(t)) for t in np.linspace(0.75, -0.75, 50)], CUF, "////", 0.5)
    pad = [(X0 + math.sqrt(2500 - y * y), y) for y in np.linspace(-30, 30, 40)]
    _p(ax, [P(*p) for p in pad[::-1]] + [P(px1, -30), P(px1, 30)][::-1], BR2, "\\\\\\\\")
    _p(ax, [P(px1, -30), P(fl1, -30), P(fl1, 30), P(px1, 30)], BR, "////")
    _p(ax, [P(fl1, -11), P(bw, -11), P(bw, 11), P(fl1, 11)], BR, "////")
    _p(ax, [P(bw, -29), P(bw + 3.9, -29), P(bw + 3.9, 29), P(bw, 29)], BR, "////")
    ax.add_patch(Rectangle(P(shx - 2, -3), (bw + 4 - shx + 2) * s, 6 * s, fc="#cfe8f5", ec=INK, lw=0.4, zorder=4))
    for yb in (-22, 22):
        _p(ax, [P(fl1, yb - 5), P(fl1 + 4, yb - 5), P(fl1 + 4, yb + 5), P(fl1, yb + 5)], ST, z=6)
        _p(ax, [P(fl1 - 10, yb - 3), P(fl1, yb - 3), P(fl1, yb + 3), P(fl1 - 10, yb + 3)], ST, z=6)
        for k in range(8): ax.plot([P(fl1 - 10 + k, 0)[0]] * 2, [P(0, yb - 3)[1], P(0, yb + 3)[1]], lw=0.2, color="#666", zorder=7)
        cl(ax, P(fl1 - 14, yb), P(fl1 + 7, yb))
    for sg in (1, -1): ax.add_patch(Circle(P(px1 - 1, sg * 6.8), 1.31 * s, fc="#333", ec=INK, lw=0.3, zorder=6))
    cl(ax, P(shx - 6, 0), P(bw + 10, 0))
    yt = P(0, 30)[1] + 6
    xs = [(shx, "X130 shell"), (fl1 - 10, "X133 bolt tip"), (px1, "X138 boss face"), (fl1, "X143 flange"), (fl1 + 4, "X147 head"), (bw, "X150 body")]
    for (a, _), (b, _) in zip(xs[:-1], xs[1:]): hdim(ax, P(a, 0)[0], P(b, 0)[0], P(a, 30)[1], P(b, 30)[1], yt, f"{b - a:g}", size=4.6)
    for k, (xv, lab) in enumerate(xs): ax.text(P(xv, 0)[0], yt + 6 + 4 * (k % 2), lab, fontsize=4.4, ha="center", color=DIMC)
    for a, b, lab in ((-30, -22, "8"), (-22, 0, "22"), (0, 22, "22"), (22, 30, "8")):
        vdim(ax, P(0, a)[1], P(0, b)[1], P(fl1, a)[0], P(fl1, b)[0], P(fl1 + 12, 0)[0], lab, side="right", size=4.6)
    vdim(ax, P(0, -30)[1], P(0, 30)[1], P(fl1, -30)[0], P(fl1, 30)[0], P(fl1 + 22, 0)[0], "60", side="right")
    ax.text(*P(112, -40), "VIEW A - PLAN SECTION AT Z218 (through both bolts), 2:1", fontsize=5.6, weight="bold")
    leader(ax, P(126, 22), (P(bw + 30, 0)[0], P(0, 36)[1]), "boss 13 thick at the bolts; drill Ø5 ↧7.5, tap M6 ↧6")
    leader(ax, P(px1 - 1, 6.8), (P(bw + 30, 0)[0], P(0, 12)[1]), "O-ring 44: OR 3112 (10.77 x 2.62) in groove Ø11/Ø16.2 x 2.0")
    leader(ax, P(fl1 + 2, -22), (P(bw + 30, 0)[0], P(0, -36)[1]), "46 hex bolt M6 x 10, 10 mm AF, 6 N·m, 5 mm engaged")
    # VIEW B: boss face
    bx0, by0 = 300, 200
    Q = lambda y, z: (bx0 + y * s, by0 + (z - pz) * s)
    _p(ax, [Q(-30, pz - 13), Q(30, pz - 13), Q(30, pz + 13), Q(-30, pz + 13)], BR2)
    for yb in (-22, 22): ax.add_patch(Circle(Q(yb, pz), 2.5 * s, fc="white", ec=INK, lw=0.5, zorder=4)); ax.add_patch(Circle(Q(yb, pz), 3 * s, fc="none", ec=INK, lw=0.3, zorder=4))
    ax.add_patch(Circle(Q(0, pz), 8.1 * s, fc="#eeeeee", ec=INK, lw=0.5, zorder=4)); ax.add_patch(Circle(Q(0, pz), 5.5 * s, fc="#eeeeee", ec=INK, lw=0.4, zorder=5))
    ax.add_patch(Circle(Q(0, pz), 3 * s, fc="white", ec=INK, lw=0.5, zorder=6))
    cl(ax, Q(-34, pz), Q(34, pz)); cl(ax, Q(0, pz - 17), Q(0, pz + 17))
    hdim(ax, Q(-30, 0)[0], Q(30, 0)[0], Q(0, pz - 13)[1], Q(0, pz - 13)[1], Q(0, pz - 13)[1] - 5, "60")
    hdim(ax, Q(-22, 0)[0], Q(22, 0)[0], Q(0, pz + 13)[1], Q(0, pz + 13)[1], Q(0, pz + 13)[1] + 5, "44 bolt centres")
    vdim(ax, Q(0, pz - 13)[1], Q(0, pz + 13)[1], Q(30, 0)[0], Q(30, 0)[0], Q(30, 0)[0] + 5, "26", side="right")
    ax.text(bx0, Q(0, pz + 13)[1] + 14, "VIEW B - BOSS FACE (from the group), 2:1", fontsize=5.6, weight="bold", ha="center")
    ax.text(14, 56, "\n".join([
        "Joint stack (boiler -> group): Ø100 copper shell (hole Ø14) | brazed boss 69 (face X138) | O-ring 44 in face groove |",
        "group flange 5 thick (X138-143) | 2 x M6 x 10 bolts side by side at Y = ±22, heads on X143.",
        "Tighten alternately to 6 N·m [E]. Fit pick-up tube 45 into the Ø8 H7 back bore before brazing / from inside the boiler."]),
        fontsize=5, va="top", linespacing=1.45)
    sh.save(pdf)

# ================================================================== WIRING + ELECTRICAL
def sheet_wiring(pdf, Sheet):
    sh = Sheet(None, "ELECTRICAL - WIRING, PRESSURESTAT, SAFETY THERMOSTAT", "-")
    ax = sh.ax; wx, wy = 30, 210
    def box(x, y, w, h, t, fc="white"):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=0.6)); ax.text(x + w / 2, y + h / 2, t, fontsize=5.4, ha="center", va="center")
    box(wx, wy, 30, 22, "MAINS\n230 V 50 Hz\nL   N   PE")
    box(wx + 50, wy, 40, 22, "65 SWITCH\ngreen, lit\n2-pole 16 A", "#e9f6ec")
    box(wx + 110, wy, 40, 22, "75 SAFETY\nTHERMOSTAT\n127 °C manual reset", "#fff3e6")
    box(wx + 170, wy, 40, 22, "73 PRESSURESTAT\nopens ~90 kPa\ncloses ~70 kPa", "#e6eefb")
    box(wx + 230, wy, 40, 22, "6 ELEMENT\n1000 W\n52.9 Ω", "#fde9d0")
    for a, b in ((wx + 30, wx + 50), (wx + 90, wx + 110), (wx + 150, wx + 170), (wx + 210, wx + 230)):
        ax.annotate("", xy=(b, wy + 15), xytext=(a, wy + 15), arrowprops=dict(arrowstyle="-|>", lw=0.9, color="#a0522d"))
    ax.text(wx + 40, wy + 18, "L", fontsize=5, color="#a0522d")
    ax.plot([wx + 270, wx + 285, wx + 285, wx + 70, wx + 70], [wy + 7, wy + 7, wy - 18, wy - 18, wy], lw=0.9, color="#1f5fbf")
    ax.plot([wx + 15, wx + 15], [wy, wy - 18], lw=0.9, color="#1f5fbf"); ax.plot([wx + 15, wx + 70], [wy - 18, wy - 18], lw=0.9, color="#1f5fbf")
    ax.text(wx + 150, wy - 22, "N (through 2nd pole of switch)", fontsize=5, color="#1f5fbf", ha="center")
    ax.plot([wx + 5, wx + 5, wx + 250, wx + 250], [wy, wy - 34, wy - 34, wy], lw=0.9, color="#2e8b57")
    ax.text(wx + 130, wy - 38, "PE (protective earth): element flange M4 stud + base shell tag, < 0.1 Ω", fontsize=5, color="#2e8b57", ha="center")
    rows = [("Supply", "230 V AC, 50 Hz (120 V / 60 Hz version: element 14.4 Ω)"), ("Power", "1000 W [D]; current 4.35 A at 230 V"),
            ("Pressurestat", "SP-NC switch, G1/4 male, adjustable 50-120 kPa, factory ~80 kPa [D]"), ("Safety thermostat", "bimetal disc, opens 127 °C, manual reset [D]"),
            ("Internal wire", "1.0 mm² silicone, 180 °C rated; 6.3 mm insulated spade terminals"), ("Cord", "H05RR-F 3G1.0 mm², 1.5 m, gland M16 x 1.5"),
            ("Insulation test", "> 2 MΩ at 500 V DC, L+N to PE"), ("Heat-up", "~10 min from 20 °C to 90 kPa with 1.1 L water [E]")]
    ax.text(30, 150, "ELECTRICAL DATA (SI)", fontsize=7, weight="bold", va="top")
    for i, (k, v) in enumerate(rows):
        ax.text(30, 143 - i * 5.2, k, fontsize=5.4, va="top", weight="bold"); ax.text(80, 143 - i * 5.2, v, fontsize=5.4, va="top")
    sh.save(pdf)

# ================================================================== FASTENERS
FASTENERS = [
 ("46", 2, "Hex bolt", "ISO 4017", "M6 x 10", "Brass / A2-70", "Group flange -> boiler boss (side by side)", "10 mm AF", "6 N·m"),
 ("8", 3, "Screw", "ISO 4762", "M5 x 12 [D]", "A2-70", "Element flange -> ring-nut ears", "4 mm hex key", "3 N·m, 3 passes"),
 ("12", 1, "Socket cap screw", "ISO 4762", "M8 x 40", "A2-70", "Cap knob -> cap insert", "6 mm hex key", "hand tight"),
 ("47", 1, "Check nut", "DIN 439", "M8", "Brass", "Piston rod top", "13 mm AF", "snug"),
 ("48", 1, "Acorn nut", "DIN 1587", "M8", "Brass", "Piston rod top", "13 mm AF", "snug on 47"),
 ("50", 2, "Grooved pin", "-", "Ø6 h8 x 34", "AISI 303", "Lever fulcrum + rod pin", "-", "-"),
 ("51", 4, "E-clip", "DIN 6799", "5", "Spring steel", "On pins 50 [D 'circlip size 5']", "E-clip tool", "-"),
 ("41", 1, "C-clip", "DIN 472", "20 x 1 [D]", "Spring steel", "Top of group sleeve", "circlip pliers", "-"),
 ("31", 1, "Spring pin", "ISO 8752", "Ø2.5 x 30", "Stainless", "Steam knob -> stem", "2.5 mm drift", "press"),
 ("4", 1, "Fixing ring nut", "-", "M80 x 1.5", "Brass", "Boiler spigot -> base", "3-lug / filter wrench", "hand + 1/8 turn"),
 ("20", 2, "Glass nut", "-", "M16 x 1", "Brass", "Sight-glass retainers", "17 mm AF", "hand + 1/4 turn"),
 ("21", 2, "Nut D12", "-", "M12 x 1 [D]", "Brass", "Sight-glass spigots (inside boiler)", "17 mm AF box", "8 N·m"),
 ("24/70", 1, "Slotted plug", "-", "M10 x 1", "Brass", "Lower sight-glass block", "slot 1.6", "snug"),
 ("72", 1, "Gauge adapter", "-", "M10 x 1 / G1/8", "Brass", "Upper block -> gauge [D]", "14 mm AF", "8 N·m"),
 ("71", 1, "Gauge stem", "ISO 228", "G1/8", "Brass", "Into adapter 72", "by case", "hand + 1/2 turn, PTFE tape"),
 ("74", 2, "Pipe nuts", "ISO 228", "G1/8 + G1/4", "Brass", "Pressurestat pipe ends [D]", "14 / 17 mm AF", "snug + 1/4 turn"),
 ("73", 2, "Bracket screws", "ISO 7045", "M4 x 8", "Zn steel", "Pressurestat to sub-base", "PH2", "1.2 N·m"),
 ("75", 2, "Self-tapping screws", "ISO 7049", "M3 / ST3.5 [D]", "Zn steel", "Thermostat to element flange", "PH1", "0.8 N·m"),
 ("6", 3, "Terminal nuts", "ISO 4032", "M4 [D 'hex nut M4 in brass']", "Brass", "Element terminals + PE", "7 mm AF", "1.2 N·m"),
 ("87", 1, "Steam riser", "-", "M12 x 1 / M10 x 1", "Brass", "Dome boss -> valve body", "14 mm AF", "10 N·m + PTFE tape"),
 ("27", 1, "Packing nut", "-", "M12 x 1", "Brass", "Steam stem gland", "14 mm AF", "until stem drags"),
 ("13", 1, "Safety valve", "-", "M12 x 1.5", "Brass", "Dome boss", "14 mm AF", "10 N·m + PTFE tape"),
 ("9", 1, "Cap insert", "-", "M40 x 1.5", "Brass", "Neck ring", "by knob", "hand"),
 ("81", 1, "Sub-base screw", "ISO 7049", "ST4.2 x 20 [D 'base screw']", "Zn steel", "Sub-base -> base boss", "PH2", "1.5 N·m"),
 ("59", 1, "Handle stud", "DIN 976", "M8 x 80", "A2", "Portafilter handle", "-", "Loctite 243"),
 ("55", 1, "Spout", "-", "M10 x 1", "Brass", "Portafilter", "hand", "snug"),
 ("66", 1, "Cable gland", "EN 62444", "M16 x 1.5", "Ni brass", "Base rear wall", "22 mm AF", "5 N·m"),
]

def sheet_fasteners(pdf, Sheet):
    sh = Sheet(None, "FASTENER MASTER TABLE - every screw, nut, pin, clip and threaded joint", "-")
    ax = sh.ax
    cols = [("ITEM", 13), ("QTY", 9), ("TYPE", 34), ("STANDARD", 19), ("SIZE (mm)", 38), ("MATERIAL", 24), ("WHERE", 92), ("TOOL", 32), ("TIGHTEN (SI)", 34)]
    x0, y0, rh = 14, 283, 6.2
    x = x0
    for n, w in cols:
        ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc="#dde6f3", ec=INK, lw=0.4)); ax.text(x + 1, y0 - rh / 2, n, fontsize=5, va="center", weight="bold"); x += w
    for i, r in enumerate(FASTENERS):
        y = y0 - rh * (i + 2); x = x0
        for (n, w), v in zip(cols, r):
            ax.add_patch(Rectangle((x, y), w, rh, fc="white" if i % 2 else "#f7f7f7", ec="#999", lw=0.2)); ax.text(x + 1, y + rh / 2, str(v), fontsize=4.7, va="center"); x += w
    ax.text(14, y0 - rh * (len(FASTENERS) + 2) - 3, f"{len(FASTENERS)} positions, {sum(r[1] for r in FASTENERS)} pieces. Torques in newton-metres (N·m) for brass threads [E]. "
            "G-threads are ISO 228 parallel pipe threads (G1/8: Ø9.73, pitch 0.907; G1/4: Ø13.16, pitch 1.337).", fontsize=5, va="top", color=NOTE)
    sh.save(pdf)

# ================================================================== SEAL SCHEDULE + ASSEMBLY + VERIFY + MASS
SEALS = [("37", "Piston seals x2", "44 x 36 x 5.5 V-lip [D]", "Silicone VMQ 70 ShA"), ("42", "Group gasket", "60 x 50 x 5.5 [D]", "Silicone VMQ"),
         ("77", "Sleeve O-ring", "44.2 x 3.53 [D section]", "FKM 75"), ("39", "Rod lip seal", "20 x 10 x 4", "PTFE"), ("44", "Group-to-boiler O-ring", "OR 3112, 10.77 x 2.62 [D]", "EPDM 70"),
         ("5", "Base gaskets", "112 x 82 x 2 + 93 x 80 x 2", "AFM34 fibre"), ("7", "Element O-ring", "73.98 x 3.53 [D]", "Silicone VMQ 70"),
         ("10", "Cap gasket", "46 x 40.5 x 2", "Silicone VMQ 60"), ("22", "Glass seals x2", "17 x 12 x 4", "Silicone VMQ"), ("23", "Spigot washers x4", "18 x 12 x 1", "PTFE"),
         ("28", "Stem packing", "11 x 6 x 6", "EPDM 70"), ("90", "Frother O-ring", "12 x 8 x 2", "Silicone VMQ")]

def sheet_schedule(pdf, Sheet):
    sh = Sheet(None, "SEAL SCHEDULE, ASSEMBLY SEQUENCE, CHECKS, MASS", "-")
    ax = sh.ax
    ax.text(14, 283, "SEAL SCHEDULE (all sizes in mm)", fontsize=7.5, weight="bold", va="top")
    cols = [("ITEM", 12), ("SEAL", 44), ("SIZE", 50), ("MATERIAL", 40)]; y0, rh = 276, 5.4
    x = 14
    for n, w in cols:
        ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc="#dde6f3", ec=INK, lw=0.4)); ax.text(x + 1, y0 - rh / 2, n, fontsize=5, va="center", weight="bold"); x += w
    for i, r in enumerate(SEALS):
        x = 14; y = y0 - rh * (i + 2)
        for (n, w), v in zip(cols, r):
            ax.add_patch(Rectangle((x, y), w, rh, fc="white", ec="#999", lw=0.2)); ax.text(x + 1, y + rh / 2, v, fontsize=4.7, va="center"); x += w
    ax.text(14, 196, "ASSEMBLY SEQUENCE", fontsize=7.5, weight="bold", va="top")
    seq = ["1  Braze: lower shell + seam ring + upper shell, foot casting, dome, neck ring, boss 69, dome bosses.",
           "2  Press pick-up tube 45 into the boss from inside; fit sight-glass spigot nuts (D12) with PTFE washers.",
           "3  Base: upper gasket, base shell, lower gasket, ring nut 4 (3-lug wrench), hand + 1/8 turn.",
           "4  Element: O-ring 7 on flange, 3 x M5 x 12 into ring-nut ears, 3 N·m in three passes.",
           "5  Pressurestat pipe 74 (G1/8 -> G1/4), pressurestat 73 on sub-base, thermostat 75 on flange, wiring, earth.",
           "6  Sight glass: seals, tube, guard, glass nuts; gauge adapter 72 + gauge 71 on the upper block.",
           "7  Steam: riser 87, valve body 25, stem 26, packing 28, nut 27, knob 30 + pin 31; pipe 88, swivel 33, wand 32.",
           "8  Safety valve 13 (+ PTFE tape) with spring, poppet, cup 16 and exhaust tube to the tray.",
           "9  Group: sleeve 76 + O-ring 77, piston 36 + 2 seals (lips down), rod 38, washer 40, lip seal 39, C-clip 41.",
           "10 Group onto boss: O-ring 44, 2 x M6 x 10 at 6 N·m; lever 49, roller 52, pins 50, E-clips 51; nuts 47 + 48.",
           "11 Screen 43 + gasket 42 (seat with the portafilter); sub-base 79 + feet 80; drip tray 82 + grid 62.",
           "12 Fill 1.1 L, heat, check 80-90 kPa cut-out, purge air via steam valve, check for leaks."]
    for i, t in enumerate(seq): ax.text(14, 189 - i * 5.0, t, fontsize=5, va="top")
    ax.text(240, 283, "CHECK BEFORE MAKING PARTS (measure with calipers)", fontsize=7.5, weight="bold", va="top", color=NOTE)
    ver = ["Overall height 345 and base height 65 (scaled from photos).", "Shell wall thickness (1.5 assumed) - use an ultrasonic gauge.",
           "Bell Ø76 and body Ø58 of the Millennium group.", "Sleeve OD 50 / ID 44 and its O-ring groove.", "Bolt spacing 44 on the boss (side by side).",
           "Steam valve layout and wand length (from photos).", "Dome boss positions for steam riser and safety valve.", "Gauge adapter thread (M10 x 1 assumed).",
           "Every value marked [V] or [E] in the drawings."]
    for i, t in enumerate(ver): ax.text(240, 276 - i * 5.0, "[ ]  " + t, fontsize=5.2, va="top")
    ax.text(240, 222, "MASS ESTIMATE (kg)", fontsize=7.5, weight="bold", va="top")
    m = [("Boiler (copper shell, castings, element, fittings)", 2.6), ("Group, piston, lever", 1.25), ("Base, sub-base, tray, grid, electrics", 1.75),
         ("Portafilter + baskets", 0.65), ("Steam valve, gauge, safety valve, cap", 0.45)]
    for i, (k, v) in enumerate(m): ax.text(240, 215 - i * 5, k, fontsize=5.2, va="top"); ax.text(380, 215 - i * 5, f"{v:.2f}", fontsize=5.2, va="top", weight="bold")
    ax.text(240, 188, f"Total about {sum(v for _, v in m):.1f} kg (retailers: 6.4-7.3 kg) [D]", fontsize=5.4, va="top", weight="bold")
    sh.save(pdf)

# ================================================================== BOM (Professional)
BOM = [
 ("1", 1, "Lower shell", "Copper Cu-DHP tube, polished + lacquer", "Ø100 x 1.5 x 122, hole Ø12.5", "D/E", "drg 1"),
 ("85", 1, "Upper shell", "Copper Cu-DHP tube", "Ø100 x 1.5 x 70, holes Ø14 + Ø12.5", "D/E", "drg 1"),
 ("84", 1, "Seam ring", "Copper", "Ø97 x 1.5 x 10, brazed inside", "E", "-"),
 ("2", 1, "Dome", "Copper, spun 1.5", "Ø103 skirt -> Ø48, 20 tall, 2 bosses", "V/E", "drg 3"),
 ("86", 1, "Neck ring", "Brass CW617N", "Ø46 x 10, M40 x 1.5 inside", "V/E", "drg 3"),
 ("3", 1, "Foot casting", "Brass CW617N", "Spigot M80 x 1.5, flare Ø112, socket Ø100.2", "D/V/E", "drg 3"),
 ("69", 1, "Boiler boss", "Brass CW617N", "60 x 26, R50 seat, 2 x M6, O-ring groove", "V/E", "drg 4"),
 ("4", 1, "Fixing ring nut", "Brass CW617N", "M80 x 1.5, Ø98 x 12, 3 ears M5", "D/V", "drg 4"),
 ("5", 2, "Base gaskets", "Fibre AFM34", "112 x 82 x 2 + 93 x 80 x 2", "D/E", "drg 17"),
 ("6", 1, "Heating element", "AISI 316", "1000 W 230 V, flange Ø84", "D/V", "drg 4"),
 ("7", 1, "Element O-ring", "Silicone VMQ 70", "73.98 x 3.53 (465225)", "D", "drg 17"),
 ("8", 3, "Element screw", "A2-70 ISO 4762", "M5 x 12", "D", "-"),
 ("9", 1, "Cap insert", "Brass CW614N", "M40 x 1.5 x 16, flange Ø46", "V/E", "drg 3"),
 ("10", 1, "Cap gasket", "Silicone VMQ 60", "46 x 40.5 x 2", "E", "drg 17"),
 ("11", 1, "Cap knob", "Rosewood, oiled", "Ø58 6-lobe, 61 tall", "V", "drg 4"),
 ("12", 1, "Cap screw", "A2-70 ISO 4762", "M8 x 40", "V/E", "drg 5"),
 ("13", 1, "Safety valve body", "Brass, anti-vacuum type", "M12 x 1.5, 14 mm AF", "D/E", "drg 9"),
 ("14", 1, "Valve poppet", "Stainless + silicone", "Ø6", "E", "-"),
 ("15", 1, "Valve spring", "AISI 302 wire Ø0.8", "OD 5.2 x 13 free", "E", "-"),
 ("16", 1, "Valve cup + exhaust tube", "Brass + Cu tube Ø5", "Ø22 x 22; tube 214 long", "V/E", "drg 9, 16"),
 ("17", 1, "Sight-glass tube", "Borosilicate 3.3", "Ø12 x 9 x 135", "V/E", "drg 6"),
 ("18", 1, "Glass guard", "Polycarbonate, clear", "Ø18 x 16 x 109", "V/E", "drg 7"),
 ("19", 2, "Sight-glass block", "Brass CW614N", "18 cube, M12 x 1 spigot, M16 x 1 boss", "D/V/E", "drg 6"),
 ("20", 2, "Glass nut", "Brass", "M16 x 1, 17 mm AF", "V/E", "drg 7"),
 ("21", 2, "Nut D12", "Brass", "M12 x 1, 17 mm AF", "D", "drg 7"),
 ("22", 2, "Glass seal", "Silicone VMQ", "17 x 12 x 4", "D/E", "drg 17"),
 ("23", 4, "Spigot washer", "PTFE + brass", "18 x 12 x 1", "D", "drg 17"),
 ("24", 1, "Plug (bottom, = 70)", "Brass", "M10 x 1 x 6", "D/V", "drg 7"),
 ("25", 1, "Steam valve body", "Brass CW614N", "Ø15 x 48, M12 x 1 both ends", "D/V/E", "drg 8"),
 ("26", 1, "Steam stem", "AISI 303", "Ø6 x 62, M8 x 1", "V/E", "drg 8"),
 ("27", 1, "Packing nut", "Brass", "M12 x 1, 14 mm AF", "D/E", "drg 8"),
 ("28", 1, "Stem packing", "EPDM 70", "11 x 6 x 6", "D/E", "drg 17"),
 ("29", 2, "Stem washer", "Brass", "11 x 6.2 x 0.8", "D/V", "drg 17"),
 ("30", 1, "Steam knob", "Rosewood, oiled", "Ø37 6-lobe x 22", "V", "drg 8"),
 ("31", 1, "Knob pin", "Stainless ISO 8752", "Ø2.5 x 30", "D/E", "drg 10"),
 ("32", 1, "Steam wand", "Brass tube Ø8 x 1", "bend table", "V/E", "drg 15"),
 ("33", 1, "Steam swivel", "Brass", "14 mm AF x 12", "V/E", "drg 9"),
 ("34", 1, "Steam tip", "Brass", "Ø9 ball, 1 hole Ø1.2", "V/E", "drg 10"),
 ("35", 1, "Group body (Millennium)", "Brass CW617N", "Bell Ø76, bore Ø50.2, flange 60 x 26", "D/V/E", "drg 2"),
 ("36", 1, "Piston (brass, v3.1)", "Brass CW614N", "Ø43.9 x 30, 2 grooves", "D", "drg 11"),
 ("37", 2, "Piston seal", "Silicone VMQ 70", "44 x 36 x 5.5", "D", "drg 17"),
 ("38", 1, "Piston rod", "Hard-chromed steel", "Ø10 x 98.5, M8 ends", "V/E", "drg 11"),
 ("39", 1, "Rod lip seal", "PTFE", "20 x 10 x 4", "D/E", "drg 17"),
 ("40", 1, "Brass washer with holes", "Brass", "20 x 10.5 x 1", "D/E", "drg 14"),
 ("41", 1, "C-clip", "DIN 472", "20 x 1", "D", "drg 18"),
 ("42", 1, "Group gasket", "Silicone VMQ", "60 x 50 x 5.5", "D", "drg 18"),
 ("43", 1, "Shower screen", "AISI 304", "Ø54", "D", "-"),
 ("44", 1, "Group-to-boiler O-ring", "EPDM 70", "OR 3112", "D", "drg 18"),
 ("45", 1, "Pick-up tube", "Brass tube Ø8 x 1", "bend table", "V/E", "drg 15"),
 ("46", 2, "Group bolt", "Brass / A2-70", "M6 x 10", "D/V", "drg 14"),
 ("47", 1, "Check nut", "Brass DIN 439", "M8", "D", "drg 14"),
 ("48", 1, "Acorn nut", "Brass DIN 1587", "M8", "D", "drg 12"),
 ("49", 1, "Lever", "Brass, polished", "272 fulcrum to end, rod Ø11", "V/E", "drg 12"),
 ("50", 2, "Lever pin", "AISI 303", "Ø6 x 34", "D", "drg 12"),
 ("51", 4, "E-clip", "DIN 6799", "5", "D", "drg 18"),
 ("52", 1, "Roller", "Brass", "Ø10 x 16, bore 6.05", "D", "drg 11"),
 ("53", 1, "Lever handle", "Rosewood", "Ø22-24 x 101", "V", "drg 12"),
 ("54", 1, "Portafilter body", "Brass, polished", "Ø60 rim, inside Ø54", "D/V", "drg 13"),
 ("55", 1, "Double spout", "Brass", "M10 x 1", "V", "drg 13"),
 ("56", 1, "Basket, double", "AISI 304", "51 nominal, 60 rim", "D", "-"),
 ("57", 1, "Basket, single", "AISI 304", "51 nominal, 60 rim", "D", "-"),
 ("59", 1, "Handle stud", "A2", "M8 x 80", "V/E", "drg 13"),
 ("60", 1, "Portafilter handle", "Rosewood", "Ø24-26 x 100", "V", "drg 13"),
 ("61", 1, "Base shell", "Brass 0.8, polished", "290 x 200 x 55", "D/V/E", "drg 5"),
 ("62", 1, "Drip grid", "Brass 0.8", "128 x 112, 76 holes Ø7.2", "V", "drg 5"),
 ("64", 1, "Badge", "Enamel", "Ø38", "V", "-"),
 ("65", 1, "Switch", "Green lit rocker, 2-pole 16 A", "cut-out 22 x 30", "V", "-"),
 ("66", 1, "Cable gland", "Ni brass", "M16 x 1.5", "V/E", "drg 10"),
 ("67", 1, "Mains cord", "H05RR-F 3G1.0", "1.5 m", "E", "-"),
 ("70", 1, "Plug (bottom)", "Brass", "M10 x 1 x 6", "D/V", "drg 7"),
 ("71", 1, "Pressure gauge", "Brass case", "Ø40 dial, 0-250 kPa, G1/8", "D", "drg 6"),
 ("72", 1, "Gauge adapter", "Brass", "M10 x 1 / G1/8", "D/E", "drg 6"),
 ("73", 1, "Pressurestat", "Bought-in", "G1/4 male, 50-120 kPa", "D", "-"),
 ("74", 1, "Pressurestat pipe", "Copper Ø4 x 0.7", "bend table, G1/8 + G1/4 nuts", "D/V", "drg 16"),
 ("75", 1, "Safety thermostat", "Bimetal, manual reset", "127 °C", "D", "-"),
 ("76", 1, "Group sleeve", "PTFE (Teflon)", "Ø50 x Ø44 x 59.5", "D/E", "drg 11"),
 ("77", 1, "Sleeve O-ring", "FKM 75", "44.2 x 3.53", "D/E", "drg 18"),
 ("79", 1, "Sub-base", "ABS black", "292 x 202", "D/E", "drg 5"),
 ("80", 4, "Foot", "TPE black", "Ø18 x 4", "D/E", "-"),
 ("81", 1, "Sub-base screw", "Zn steel", "ST4.2 x 20", "D/E", "-"),
 ("82", 1, "Drip tray", "ABS black", "136 x 120 x 14", "D/V", "-"),
 ("87", 1, "Steam riser", "Brass", "M12 x 1 / M10 x 1, 38 long", "V/E", "drg 9"),
 ("88", 1, "Steam pipe", "Brass tube Ø8 x 1", "bend table", "V/E", "drg 15"),
 ("89", 1, "Auto-frother", "Brass + silicone", "Ø18 x 32", "D/E", "drg 10"),
 ("90", 1, "Frother O-ring", "Silicone VMQ", "12 x 8 x 2", "D/E", "drg 18"),
]

"""Group section (new design) + group-to-boiler joint sheet + fastener master table."""
import math
from matplotlib.patches import Polygon, Circle, Rectangle
from views import D
from partdraw import hdim, vdim, leader, cl, INK, DIMC, NOTE

BR, BR2, GK, WD, ST = "#f4e3b5", "#e6c98f", "#bdbdbd", "#d2ae7e", "#cfcfcf"

def _poly(ax, pts, fc, hatch=None, lw=0.6, z=3):
    ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=INK, lw=lw, hatch=hatch, zorder=z))

def group_profile(rb, top):
    sk, gr1, scr, btop = 12, 17.3, 18.3, top - 8
    out = []
    for sg in (1, -1):
        out.append([(sg * 31.25, 0), (sg * 36, 0), (sg * 36, 20), (sg * rb, 30), (sg * rb, top), (sg * 5.25, top), (sg * 5.25, top - 2),
                    (sg * 10, top - 2), (sg * 10, btop), (sg * 22, btop), (sg * 22, scr), (sg * 26, scr), (sg * 26, gr1),
                    (sg * 28.85, gr1), (sg * 28.85, sk), (sg * 31.25, sk)])
    return out, btop

def sheet_group(pdf, Sheet):
    sh = Sheet(None, "BREW GROUP ASSEMBLY - SECTION B-B, lever at rest", "1:1")
    ax = sh.ax; z0 = D["BELL_Z0"]; gx = D["GX"]
    ox, oy = 120, 108
    P = lambda x, z: (ox + x, oy + z - z0)          # x rel. group axis, z = machine Z
    rb = D["BODY_D"] / 2; top = D["BODY_Z1"] - z0
    profs, btop = group_profile(rb, top)
    for pr in profs: _poly(ax, [P(x, z + z0) for x, z in pr], BR, "////")
    pz = D["PORT_Z"]; fl0, fl1 = D["PAD_X1"] - gx, D["FL_X1"] - gx
    _poly(ax, [P(fl0, pz - 24), P(fl1, pz - 24), P(fl1, pz - 11), P(-rb, pz - 11), P(-rb, pz + 11), P(fl1, pz + 11), P(fl1, pz + 24), P(fl0, pz + 24)], BR, "////")
    ax.add_patch(Rectangle(P(fl0, pz - 4), (-22 - fl0), 8, fc="#cfe8f5", ec=INK, lw=0.5, zorder=4))
    # pad + shell + bolts
    shx = D["BX"] + D["SH_D"] / 2 - gx
    _poly(ax, [P(shx, pz - 24), P(fl0, pz - 24), P(fl0, pz + 24), P(shx, pz + 24)], BR2, "\\\\\\\\")
    ax.add_patch(Rectangle(P(shx, pz - 3), fl0 - shx, 6, fc="#cfe8f5", ec=INK, lw=0.4, zorder=4))
    _poly(ax, [P(shx - 1.5, pz - 60), P(shx, pz - 60), P(shx, pz - 7), P(shx - 1.5, pz - 7)], BR, "////")
    _poly(ax, [P(shx - 1.5, pz + 7), P(shx, pz + 7), P(shx, pz + 40), P(shx - 1.5, pz + 40)], BR, "////")
    for zb in (pz - 19, pz + 19):
        ax.add_patch(Rectangle(P(fl1, zb - 5), 4, 10, fc=ST, ec=INK, lw=0.5, zorder=5))
        ax.add_patch(Rectangle(P(fl1 - 10, zb - 3), 10, 6, fc=ST, ec=INK, lw=0.5, zorder=5))
    ax.add_patch(Rectangle(P(fl0 - 0.3, pz - 8), 1.5, 16, fc="#c87f4a", ec=INK, lw=0.4, zorder=6))
    # L-tube inside boiler
    ax.plot(*zip(P(shx + 4, pz), P(-59, pz), P(-69, pz - 10), P(-69, pz - 60)), lw=8 * 2.835 * 0.35, color="#b9975b", zorder=2, solid_joinstyle="round")
    # piston, seals, rod, nuts
    pb = z0 + 18.3
    _poly(ax, [P(-21.95, pb), P(21.95, pb), P(21.95, pb + 30), P(-21.95, pb + 30)], BR2, "\\\\\\\\")
    for g in (pb + 4, pb + 17):
        for sg in (1, -1): _poly(ax, [P(sg * 22, g), P(sg * 18, g), P(sg * 18, g + 5.6), P(sg * 22, g + 5.6)], "#333", lw=0.4, z=4)
    rod0 = pb + 30 - 14
    ax.add_patch(Rectangle(P(-5, rod0), 10, 98 - 14, fc="#dddddd", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Rectangle(P(-4, rod0 + 84), 8, 14, fc="#dddddd", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Circle(P(0, D["ROD_PIN_Z"]), 3.05, fc="white", ec=INK, lw=0.5, zorder=5))
    _poly(ax, [P(-7.5, 294), P(7.5, 294), P(7.5, 300), P(-7.5, 300)], "#e8e8e8", z=5)
    _poly(ax, [P(-7.5, 300), P(7.5, 300), P(7.5, 305), P(5, 309), P(0, 310), P(-5, 309), P(-7.5, 305)], "#e8e8e8", z=5)
    for zz, w, fc in ((z0 + top - 8, 1, "#222"), (z0 + top - 7, 1, "#999"), (z0 + top - 6, 4, "white")):
        for sg in (1, -1): ax.add_patch(Rectangle(P(sg * 5.1 if sg > 0 else -10, zz), 4.9, w, fc=fc, ec=INK, lw=0.3, hatch="...." if fc == "white" else None, zorder=5))
    # column, fulcrum, roller, lever cheek phantom
    c0, c1 = D["COL_X0"] - gx, D["COL_X1"] - gx
    _poly(ax, [P(c0, D["BODY_Z1"] - 4), P(c1, D["BODY_Z1"] - 4), P(c1, D["YOKE_Z1"]), P(c0, D["YOKE_Z1"])], "#eeeeee")
    ax.add_patch(Circle(P(D["FX"] - gx, D["FZ"]), 5.05, fc=BR2, ec=INK, lw=0.5, zorder=5)); ax.add_patch(Circle(P(D["FX"] - gx, D["FZ"]), 3, fc=ST, ec=INK, lw=0.5, zorder=6))
    la = math.radians(D["LEV_ANG"]); fx, fz = D["FX"] - gx, D["FZ"]
    ch = [(-14, -8), (49.6, -8), (49.6, 8), (-14, 8)]
    rot = lambda x, y: P(fx + x * math.cos(la) + y * math.sin(la), fz - x * math.sin(la) + y * math.cos(la))
    ax.add_patch(Polygon([rot(*p) for p in ch], closed=True, fc="none", ec="#555", lw=0.6, ls=(0, (6, 2, 1.5, 2)), zorder=7))
    ax.add_patch(Circle(P(0, D["ROD_PIN_Z"]), 3, fc=ST, ec=INK, lw=0.5, zorder=8))
    # portafilter, gasket, screen, basket, spout
    for sg in (1, -1):
        _poly(ax, [P(sg * 26, 188), P(sg * 30, 188), P(sg * 28, 164), P(sg * 7, 160), P(sg * 7, 164), P(sg * 26, 166)], BR, "////")
    _poly(ax, [P(-28.85, 188), P(-23.5, 188), P(-23.5, 193.3), P(-28.85, 193.3)], "#333"); _poly(ax, [P(23.5, 188), P(28.85, 188), P(28.85, 193.3), P(23.5, 193.3)], "#333")
    ax.add_patch(Rectangle(P(-26, 193.3), 52, 1, fc="#999", ec=INK, lw=0.3, zorder=5))
    ax.plot(*zip(P(-24.5, 187.5), P(-21, 168), P(21, 168), P(24.5, 187.5)), lw=0.7, color=INK, zorder=5)
    _poly(ax, [P(-7, 160), P(7, 160), P(6, 146), P(-6, 146)], BR2, "////")
    ax.plot(*zip(P(-5, 147), P(-15, 135)), lw=1.8, color=INK); ax.plot(*zip(P(5, 147), P(15, 135)), lw=1.8, color=INK)
    cl(ax, P(0, 130), P(0, 316)); cl(ax, P(-75, pz), P(-15, pz))
    # ---- dimensions: ordinate Z column (machine Z)
    xr = P(48, 0)[0]
    zlist = [(135, "135 spout tip"), (160, "160 PF bottom"), (176, "176 bell / skirt bottom"), (188, "188 skirt top = gasket seat"), (193.3, "193.3 screen"),
             (194.3, "194.3 piston face (rest)"), (196, "196 bell top"), (pz, f"{pz} port C/L"), (224.3, "224.3 piston top (rest)"), (z0 + btop, f"{z0 + btop:g} bore top / circlip"),
             (D["BODY_Z1"], f"{D['BODY_Z1']} body top"), (D["ROD_PIN_Z"], f"{D['ROD_PIN_Z']} rod pin"), (D["FZ"], f"{D['FZ']} fulcrum"),
             (D["YOKE_Z1"], f"{D['YOKE_Z1']} column top"), (294, "294 check nut"), (310, "310 acorn top")]
    ys = []
    for i, (z, lab) in enumerate(zlist):
        y = P(0, z)[1]; ly = max(y, (ys[-1] + 3.2) if ys else y); ys.append(ly)
        ax.plot([P(36, z)[0], xr - 2], [y, y], lw=0.15, color=DIMC, zorder=20); ax.plot([xr - 2, xr], [y, ly], lw=0.15, color=DIMC, zorder=20)
        ax.text(xr + 1, ly, lab, fontsize=4.5, color=DIMC, va="center", zorder=22, bbox=dict(fc="white", ec="none", pad=0.1))
    ax.plot([xr - 2, xr - 2], [P(0, 135)[1], P(0, 310)[1]], lw=0.25, color=DIMC)
    ax.text(xr - 2, P(0, 312)[1] + 2, "Z (machine)", fontsize=5, color=DIMC, ha="center", weight="bold")
    hdim(ax, P(-22, 0)[0], P(22, 0)[0], P(-22, 236)[1], P(22, 236)[1], P(0, 236)[1], "Ø44 H8 bore [D]")
    hdim(ax, P(-36, 0)[0], P(36, 0)[0], P(-36, 176)[1], P(36, 176)[1], P(0, 176)[1] - 26, "Ø72 bell [D]")
    hdim(ax, P(shx, 0)[0], P(0, 0)[0], P(shx, pz + 40)[1], P(0, pz + 52)[1], P(0, pz + 52)[1], f"{-shx:g} shell OD to group axis")
    vdim(ax, P(0, 194.3)[1], P(0, z0 + btop - 30)[1], P(-22, 194.3)[0], P(-22, z0 + btop - 30)[0], P(-30, 0)[0], f"stroke {z0 + btop - 30 - 194.3:.1f}")
    leader(ax, P(-17, 232), (P(-60, 0)[0], P(0, 262)[1]), "37 piston seals 44x36x5.5, lips DOWN")
    leader(ax, P(8, z0 + top - 4), (P(30, 0)[0] + 8, P(0, 286)[1]), "41 circlip / 40 washer / 39 rod seal (Ø20 x 6 recess)")
    leader(ax, P(D["FX"] - gx, D["FZ"]), (P(-60, 0)[0], P(0, 300)[1]), "52 roller Ø10x16 in column bore Ø10.1, 50 pin Ø6")
    leader(ax, P(fl0 + 0.4, pz + 6), (P(-70, 0)[0], P(0, pz + 30)[1]), "44 Cu washer 16x8.2x1.5 in pad recess")
    leader(ax, P(fl1 + 2, pz + 19), (P(-30, 0)[0], P(0, pz + 44)[1]), "46 hex bolt M6x10 A2-70 (2)")
    ax.text(14, 283, "NOTES", fontsize=7, weight="bold", va="top")
    ax.text(14, 277, "\n".join([
        f"Stroke: piston face 194.3 (rest) -> {z0 + btop - 30:.1f} (lever up, piston top at circlip {z0 + btop:g}) = {z0 + btop - 30 - 194.3:.1f} mm.",
        f"Displacement = π/4 x 4.4² x {(z0 + btop - 30 - 194.3) / 10:.2f} = {math.pi / 4 * 4.4 ** 2 * (z0 + btop - 30 - 194.3) / 10:.0f} ml  (Wright: 44 mm, 28 mm, 43 ml [D]).",
        f"Port Ø8 at Z{pz} spans Z{pz - 4}-{pz + 4}: fully uncovered when piston face is at Z{z0 + btop - 30:.0f}.",
        "Lever down = piston at bottom = brew position shown. Water enters only with lever up.",
        "Basket (56) 49 mm sits on PF ledge; screen 43 held by gasket 42.",
    ]), fontsize=5.2, va="top", linespacing=1.35)
    sh.save(pdf)

def sheet_joint(pdf, Sheet):
    sh = Sheet(None, "GROUP-TO-BOILER JOINT - boss, flange, bolts, seal", "2:1")
    ax = sh.ax; gx = D["GX"]; pz = D["PORT_Z"]; X0 = D["BX"]
    # -------- VIEW A: section X-Z on C/L, scale 2:1, machine coordinates
    s = 2.0; ox, oy = 36 - 96 * s, 76 - (pz - 32) * s
    P = lambda x, z: (ox + x * s, oy + z * s)
    shell_x = X0 + D["SH_D"] / 2
    _poly(ax, [P(shell_x - 1.5, pz - 32), P(shell_x, pz - 32), P(shell_x, pz + 32), P(shell_x - 1.5, pz + 32)], BR, "////")
    ax.add_patch(Rectangle(P(shell_x - 1.6, pz - 7), 1.7 * s, 14 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    _poly(ax, [P(shell_x, pz - 24), P(D["PAD_X1"], pz - 24), P(D["PAD_X1"], pz + 24), P(shell_x, pz + 24)], BR2, "\\\\\\\\")
    # pad bores
    ax.add_patch(Rectangle(P(shell_x, pz - 4), 4 * s, 8 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    ax.add_patch(Rectangle(P(shell_x + 4, pz - 3), (D["PAD_X1"] - shell_x - 4) * s, 6 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    ax.add_patch(Rectangle(P(D["PAD_X1"] - 1.2, pz - 8), 1.2 * s, 16 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    for zb in (pz - 19, pz + 19):
        ax.add_patch(Rectangle(P(D["PAD_X1"] - 7.5, zb - 2.5), 7.5 * s, 5 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    # flange + neck + body wall
    fl1 = D["FL_X1"]; bw = gx - D["BODY_D"] / 2
    _poly(ax, [P(D["PAD_X1"], pz - 24), P(fl1, pz - 24), P(fl1, pz - 11), P(bw, pz - 11), P(bw, pz - 30), P(bw + 3, pz - 30), P(bw + 3, pz + 30), P(bw, pz + 30),
               P(bw, pz + 11), P(fl1, pz + 11), P(fl1, pz + 24), P(D["PAD_X1"], pz + 24)], BR, "////")
    ax.add_patch(Rectangle(P(D["PAD_X1"], pz - 4), (bw + 3 - D["PAD_X1"]) * s, 8 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    for zb in (pz - 19, pz + 19):
        ax.add_patch(Rectangle(P(D["PAD_X1"], zb - 3.2), 5 * s, 6.4 * s, fc="white", ec=INK, lw=0.4, zorder=4))
        _poly(ax, [P(fl1, zb - 5), P(fl1 + 4, zb - 5), P(fl1 + 4, zb + 5), P(fl1, zb + 5)], ST, z=6)
        _poly(ax, [P(D["PAD_X1"] - 5, zb - 3), P(fl1, zb - 3), P(fl1, zb + 3), P(D["PAD_X1"] - 5, zb + 3)], ST, z=6)
        for k in range(5): ax.plot([P(D["PAD_X1"] - 5 + k, zb - 3)[0]] * 2, [P(0, zb - 3)[1], P(0, zb + 3)[1]], lw=0.2, color="#666", zorder=7)
    _poly(ax, [P(D["PAD_X1"] - 1.2, pz - 8), P(D["PAD_X1"] + 0.3, pz - 8), P(D["PAD_X1"] + 0.3, pz - 4.1), P(D["PAD_X1"] - 1.2, pz - 4.1)], "#c87f4a", z=6)
    _poly(ax, [P(D["PAD_X1"] - 1.2, pz + 4.1), P(D["PAD_X1"] + 0.3, pz + 4.1), P(D["PAD_X1"] + 0.3, pz + 8), P(D["PAD_X1"] - 1.2, pz + 8)], "#c87f4a", z=6)
    # L-tube
    for sg in (1, -1):
        _poly(ax, [P(96, pz + sg * 3), P(shell_x + 4, pz + sg * 3), P(shell_x + 4, pz + sg * 4), P(96, pz + sg * 4)], "#b9975b", z=5)
    ax.text(*P(97, pz + 6), "45 L-tube Ø8x1 -> bends down to Z140", fontsize=4.4)
    cl(ax, P(95, pz), P(bw + 6, pz))
    for zb in (pz - 19, pz + 19): cl(ax, P(D["PAD_X1"] - 10, zb), P(fl1 + 7, zb))
    # dims (X chain at top, machine X)
    yt = P(0, pz + 32)[1] + 5
    xs = [(shell_x, f"X{shell_x:g} shell OD"), (fl1 - 10, "X113 bolt tip"), (shell_x + 4, ""), (D["PAD_X1"], f"X{D['PAD_X1']} pad face"), (fl1, f"X{fl1} flange"),
          (fl1 + 4, "X127 head"), (bw, f"X{bw:g} body"), (bw + 3, f"X{bw + 3:g} bore")]
    for (a, la_), (b, lb) in zip(xs[:-1], xs[1:]):
        hdim(ax, P(a, 0)[0], P(b, 0)[0], P(a, pz + 24)[1], P(b, pz + 24)[1], yt, f"{b - a:g}", size=4.4)
    for k, (xv, lab) in enumerate([t for t in xs if t[1]]):
        ax.text(P(xv, 0)[0], yt + 6 + 4 * (k % 2), lab, fontsize=4.2, ha="center", color=DIMC)
    xl = P(shell_x, 0)[0] - 10
    for a, b, lab in ((pz - 24, pz - 19, "5"), (pz - 19, pz, "19"), (pz, pz + 19, "19"), (pz + 19, pz + 24, "5")):
        vdim(ax, P(0, a)[1], P(0, b)[1], P(shell_x, a)[0], P(shell_x, b)[0], xl, lab, size=4.4)
    vdim(ax, P(0, pz - 24)[1], P(0, pz + 24)[1], xl, xl, xl - 8, "48 pad / flange", size=4.4)
    RX = P(bw + 14, 0)[0]
    leader(ax, P(D["PAD_X1"] - 4, pz + 19), (RX, P(0, pz + 40)[1]), "boss 69: drill Ø5 ↧7.5, M6-6H ↧6 (2)")
    leader(ax, P(D["PAD_X1"] - 0.6, pz - 6), (RX, P(0, pz + 10)[1]), "recess Ø16 x 1.2 for Cu washer 44")
    leader(ax, P(shell_x + 6, pz), (RX, P(0, pz + 4)[1]), "port Ø6 x 4 (face) / Ø8 H7 x 4 (tube)")
    leader(ax, P(shell_x - 0.7, pz - 9), (RX, P(0, pz - 12)[1]), "shell hole Ø14; boss Ag-brazed, R40 seat")
    leader(ax, P(fl1 + 2, pz - 19), (P(bw + 14, 0)[0], P(0, pz - 32)[1]), "46 M6x10 ISO 4017 A2-70, AF10, 6 Nm, 5 engaged")
    leader(ax, P(D["PAD_X1"] + 2.5, pz + 19), (RX, P(0, pz + 30)[1]), "flange hole Ø6.4 THRU (2)")
    ax.text(*P(96, pz - 34), "VIEW A - SECTION ON C/L (X-Z), scale 2:1, machine coordinates", fontsize=5.5, weight="bold")
    # -------- VIEW B: pad face (looking -X), 2:1
    bx0, by0 = 268, 200
    Q = lambda y, z: (bx0 + y * s, by0 + (z - pz) * s)
    _poly(ax, [Q(-13, pz - 24), Q(13, pz - 24), Q(13, pz + 24), Q(-13, pz + 24)], BR2)
    for zb in (pz - 19, pz + 19):
        ax.add_patch(Circle(Q(0, zb), 2.5 * s, fc="white", ec=INK, lw=0.5, zorder=4)); ax.add_patch(Circle(Q(0, zb), 3 * s, fc="none", ec=INK, lw=0.3, zorder=4))
    ax.add_patch(Circle(Q(0, pz), 8 * s, fc="#eeeeee", ec=INK, lw=0.5, zorder=4)); ax.add_patch(Circle(Q(0, pz), 3 * s, fc="white", ec=INK, lw=0.5, zorder=5))
    cl(ax, Q(-17, pz), Q(17, pz)); cl(ax, Q(0, pz - 28), Q(0, pz + 28))
    hdim(ax, Q(-13, 0)[0], Q(13, 0)[0], Q(0, pz - 24)[1], Q(0, pz - 24)[1], Q(0, pz - 24)[1] - 5, "26")
    vdim(ax, Q(0, pz - 19)[1], Q(0, pz + 19)[1], Q(13, 0)[0], Q(13, 0)[0], Q(13, 0)[0] + 6, "38 c/c", side="right")
    leader(ax, Q(5.6, pz + 5.6), (Q(18, 0)[0] + 6, Q(0, pz + 10)[1]), "Ø16 recess")
    leader(ax, Q(-2.1, pz - 2.1), (Q(-18, 0)[0] - 6, Q(0, pz - 8)[1]), "Ø6 port")
    ax.text(bx0, Q(0, pz + 30)[1], "VIEW B - BOSS FACE (from group side), 2:1", fontsize=5.5, weight="bold", ha="center")
    # -------- VIEW C: plan section through port (X-Y)
    cx0, cy0 = 352, 128
    R_ = lambda x, y: (cx0 + (x - D["PAD_X1"]) * s, cy0 + y * s)
    import numpy as np
    arc = [(X0 + 40 * math.cos(t), 40 * math.sin(t)) for t in np.linspace(-0.4, 0.4, 30)]
    _poly(ax, [R_(*p) for p in arc] + [R_(X0 + 38.5 * math.cos(t), 38.5 * math.sin(t)) for t in np.linspace(0.4, -0.4, 30)], BR, "////")
    pad = [(X0 + 40 * math.cos(t), 40 * math.sin(t)) for t in np.linspace(math.asin(-13 / 40), math.asin(13 / 40), 20)]
    _poly(ax, [R_(*p) for p in pad] + [R_(D["PAD_X1"], 13), R_(D["PAD_X1"], -13)], BR2, "\\\\\\\\")
    _poly(ax, [R_(D["PAD_X1"], -13), R_(fl1, -13), R_(fl1, 13), R_(D["PAD_X1"], 13)], BR, "////")
    hdim(ax, R_(X0 + math.sqrt(1600 - 169), 0)[0], R_(D["PAD_X1"], 0)[0], R_(0, 13)[1], R_(0, 13)[1], R_(0, 13)[1] + 5, f"{D['PAD_X1'] - X0 - math.sqrt(1600 - 169):.1f} at edge", size=4.2)
    hdim(ax, R_(shell_x, 0)[0], R_(D["PAD_X1"], 0)[0], R_(0, 0)[1], R_(0, 0)[1], R_(0, -13)[1] - 5, f"{D['PAD_X1'] - shell_x:g} at C/L", size=4.2)
    vdim(ax, R_(0, -13)[1], R_(0, 13)[1], R_(fl1, 0)[0], R_(fl1, 0)[0], R_(fl1, 0)[0] + 5, "26", side="right", size=4.2)
    leader(ax, R_(X0 + 40 * math.cos(0.3), 40 * math.sin(0.3)), (R_(100, 0)[0] + 6, R_(0, 34)[1]), "R40 seat on Ø80 shell")
    ax.text(cx0 - 5, cy0 - 40, "VIEW C - PLAN SECTION AT Z" + f"{pz}" + ", 2:1", fontsize=5.5, weight="bold", ha="center")
    # notes
    ax.text(14, 52 - 2, "\n".join([
        "Joint stack (boiler -> group): shell Ø80 (hole Ø14) | brazed boss 69 (8 thick on C/L, face X118) | Cu washer 44 (recess 1.2, compressed 0.3) | group flange 5 thick (X118-123) | 2 x M6x10 bolt heads on X123.",
        "Bolt engagement 5 mm in brass boss = 0.83 d. Tighten alternately to 6 Nm (A2-70 in brass) [E]; renew Cu washer each time (anneal: heat cherry red, quench).",
        "L-tube 45 pressed into Ø8 H7 port from inside the boiler (element out) before the group is fitted; it reaches down to Z140 so the group draws water, not steam.",
        "Alternative seal used by later kits: O-ring OR 3112 (10.77 x 2.62) EPDM in a groove Ø11 / Ø16.2 x 2.0 deep [D for OR size]."]),
        fontsize=4.9, va="top", linespacing=1.4)
    sh.save(pdf)

FASTENERS = [
 ("46", 2, "Hex bolt", "ISO 4017", "M6x10", "A2-70", "Group flange -> boiler boss 69", "AF10", "6 Nm", "none / anti-seize"),
 ("8", 3, "Socket head cap screw", "ISO 4762", "M6x16", "8.8 Zn", "Element flange -> ring nut ears", "hex 5", "4 Nm, 3 passes", "-"),
 ("12", 1, "Socket head cap screw", "ISO 4762", "M8x35", "A2-70", "Cap knob -> cap insert", "hex 6", "hand tight", "Loctite 243"),
 ("47", 1, "Hex check nut", "DIN 439", "M8", "Brass Cr", "Piston rod top", "AF13", "snug", "-"),
 ("48", 1, "Acorn (cap) nut", "DIN 1587", "M8", "Brass Cr", "Piston rod top", "AF13", "snug against 47", "-"),
 ("50", 2, "Grooved pin", "custom", "Ø6 h8 x 34", "AISI 303", "Lever fulcrum + rod pin", "-", "-", "-"),
 ("51", 4, "Retaining washer (E-clip)", "DIN 6799", "5", "Spring steel", "On pins 50", "E-clip tool", "-", "-"),
 ("41", 1, "Internal circlip", "DIN 472", "20 x 1", "Spring steel", "Rod seal retainer in group", "circlip pliers", "-", "-"),
 ("31", 1, "Spring pin", "ISO 8752", "Ø2.5 x 30", "Stainless", "Steam knob -> stem", "Ø2.5 drift", "press", "-"),
 ("4", 1, "Ring nut (3 ears)", "custom", "M80x1.25", "Brass", "Boiler spigot -> base", "3-lug / filter wrench", "hand + 1/8 turn", "food grease"),
 ("20", 2, "Gland nut", "custom", "M16x1", "Brass Cr", "Sight glass retainers", "AF17", "hand + 1/4 turn", "-"),
 ("21", 2, "Hex nut (D12)", "custom", "M12x1", "Brass", "Sight-glass spigots inside boiler", "AF17 box", "firm", "food-grade sealant"),
 ("24/70", 2, "Slotted plug", "custom", "M10x1 x 6", "Brass Cr", "Sight-glass blocks top/bottom", "slot 1.6", "snug + fibre washer", "-"),
 ("27", 1, "Packing nut", "custom", "M12x1", "Brass Cr", "Steam valve stem gland", "AF14", "until stem drags lightly", "-"),
 ("33", 1, "Union nut", "custom", "M10x1", "Brass Cr", "Steam wand -> valve", "AF14", "snug", "-"),
 ("13", 1, "Safety valve body", "custom", "M12x1.5", "Brass Cr", "Shoulder boss", "AF14", "10 Nm", "PTFE tape 1 wrap"),
 ("25", 1, "Steam valve body", "custom", "M12x1", "Brass Cr", "Shoulder boss (rear)", "AF17", "10 Nm", "PTFE tape / 2 O-rings"),
 ("9", 1, "Cap insert", "custom", "M38x1.5", "Brass", "Boiler neck", "by knob", "hand", "-"),
 ("59", 1, "Threaded stud", "DIN 976", "M8x75", "A2", "Portafilter handle", "-", "-", "Loctite 243"),
 ("55", 1, "Spout", "custom", "M10x1", "Brass Cr", "Portafilter", "by hand / AF10", "snug", "-"),
 ("53", 1, "Lever handle insert", "custom", "M8", "Brass insert in wood", "Lever rod end", "-", "hand", "Loctite 243 (food grade)"),
 ("66", 1, "Cable gland", "EN 62444", "M16x1.5", "Ni brass", "Base rear wall", "AF22", "5 Nm", "-"),
 ("64", 2, "Badge pins", "-", "Ø2.2", "Brass", "Badge -> base front", "bent over inside", "-", "-"),
 ("PE", 1, "Earth stud + nut", "ISO 4032", "M4", "Brass", "Element flange", "AF7", "1.5 Nm", "star washer"),
 ("T1-4", 4, "Terminal studs + nuts", "ISO 4032", "M4", "Brass", "Element terminals", "AF7", "1.2 Nm", "-"),
]

def sheet_fasteners(pdf, Sheet):
    sh = Sheet(None, "FASTENER MASTER TABLE - every screw, bolt, nut, pin, clip and threaded joint", "-")
    ax = sh.ax
    cols = [("ITEM", 12), ("QTY", 9), ("TYPE", 40), ("STANDARD", 20), ("SIZE", 26), ("MATERIAL", 26), ("LOCATION / JOINT", 72), ("TOOL", 26), ("TIGHTENING", 34), ("LOCKING", 34)]
    x0, y0, rh = 14, 283, 6.6
    x = x0
    for n, w in cols:
        ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc="#dde6f3", ec=INK, lw=0.4)); ax.text(x + 1, y0 - rh / 2, n, fontsize=5, va="center", weight="bold"); x += w
    for i, r in enumerate(FASTENERS):
        y = y0 - rh * (i + 2); x = x0
        for (n, w), v in zip(cols, r):
            ax.add_patch(Rectangle((x, y), w, rh, fc="white" if i % 2 else "#f7f7f7", ec="#999", lw=0.2)); ax.text(x + 1, y + rh / 2, str(v), fontsize=4.6, va="center"); x += w
    tot = sum(r[1] for r in FASTENERS)
    ax.text(14, y0 - rh * (len(FASTENERS) + 2) - 3, f"{len(FASTENERS)} fastener positions, {tot} pieces. Torques are estimates for brass threads [E]; use food-grade (NSF H1 / NSF 61) lubricants and sealants only.",
            fontsize=5, va="top", color=NOTE)
    sh.save(pdf)

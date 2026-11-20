"""Detail drawing sheets: one cell per part, every feature dimensioned."""
import math
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, Arc
from partdraw import Cell, turned, ring, plate, pipe, hdim, vdim, leader, cl, pick_scale, scale_label, INK, DIMC, NOTE, HATCH_FC
from views import D, rounded_trap

BR = "Brass CW617N (CuZn40Pb2)"; BRB = "Brass CW614N bar"; CHR = ", Cu/Ni/Cr plated"; SS = "Stainless AISI 303"; SS4 = "Stainless AISI 304"

def grid(ax, rows, cols, x0=14, y0=56, x1=406, y1=283, gap=3):
    w = (x1 - x0 - gap * (cols - 1)) / cols; h = (y1 - y0 - gap * (rows - 1)) / rows
    return [(x0 + c * (w + gap), y1 - (r + 1) * h - r * gap, w, h) for r in range(rows) for c in range(cols)]

def lower_cells(n):
    w = (205 - 14 - 3 * (n - 1)) / n
    return [(14 + i * (w + 3), 12, w, 41) for i in range(n)]

# ================================================================== custom drawers
def shell_drawing(cell):
    """Item 1: boiler shell - section + developed (flat) hole layout."""
    ax = cell.ax; L = 184; OD = D["SH_D"]; t = 1.5; z0 = 64
    s = pick_scale(L + 30, OD + 26, cell.w - 20, cell.h * 0.42); cell.set_scale(s)
    ox, oy = cell.x + 16, cell.y + cell.h - 18 - OD / 2 * s - 6
    P = lambda z, r: (ox + z * s, oy + r * s)
    for sgn in (1, -1):
        ax.add_patch(Polygon([P(0, sgn * (OD / 2 - t)), P(L, sgn * (OD / 2 - t)), P(L, sgn * OD / 2), P(0, sgn * OD / 2)], closed=True, fc=HATCH_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    cl(ax, P(-3, 0), P(L + 3, 0))
    hdim(ax, *[P(0, 0)[0], P(L, 0)[0]], P(0, -OD / 2)[1], P(L, -OD / 2)[1], P(0, -OD / 2)[1] - 5, f"{L} (Z{z0}-Z{z0 + L})")
    vdim(ax, P(0, -OD / 2)[1], P(0, OD / 2)[1], P(0, 0)[0], P(0, 0)[0], P(0, 0)[0] - 5, f"Ø{OD} OD [D]")
    leader(ax, P(L * 0.6, OD / 2 - t / 2), (P(L * 0.6, 0)[0] + 6, P(0, OD / 2)[1] + 5), f"wall {t} [E] -> ID {OD - 2 * t:g}")
    # developed layout
    circ = math.pi * OD
    s2 = pick_scale(circ + 20, L + 25, cell.w - 24, cell.h * 0.48)
    dx, dy = cell.x + 14, cell.y + 14
    Q = lambda a, z: (dx + ((a + 90) % 360) / 360 * circ * s2, dy + z * s2)
    ax.add_patch(Polygon([(dx, dy), (dx + circ * s2, dy), (dx + circ * s2, dy + L * s2), (dx, dy + L * s2)], closed=True, fc="#f2f2f2", ec=INK, lw=0.6, zorder=3))
    for a_ in (0, 90, 180, 270): ax.text(*Q(a_, -4), f"{a_}°", fontsize=3.8, ha="center", color="#555")
    sg_ang = math.degrees(math.atan2(D["SG_Y"], D["SG_X"] - D["BX"])) % 360
    holes = [("H1", 0, D["PORT_Z"] - z0, 14, "group port Ø14 (pad 69 brazed over)"), ("H2", sg_ang, D["SG_Z0"] - z0, 12.5, "sight glass lower Ø12.5"),
             ("H3", sg_ang, D["SG_Z1"] - z0, 12.5, "sight glass upper Ø12.5")]
    for hid, a, z, d_, note in holes:
        c = Q(a, z); ax.add_patch(Circle(c, d_ / 2 * s2, fc="white", ec=INK, lw=0.5, zorder=4))
        ax.text(c[0] + 2, c[1] + 2, hid, fontsize=4, color=DIMC, zorder=5)
    ax.text(dx, dy + L * s2 + 2, f"DEVELOPED SHELL (seam at -90°; 0° = +X towards group, CCW seen from above)   scale {scale_label(s2)}", fontsize=4.2, zorder=5)
    hdim(ax, dx, dx + circ * s2, dy, dy, dy - 7, f"{circ:.1f} = π x {OD}")
    for hid, a, z, d_, note in holes:
        vdim(ax, dy, Q(a, z)[1], Q(a, z)[0], Q(a, z)[0], Q(a, z)[0] + 7, f"{z:g}", side="right", size=4)
        hdim(ax, dx, Q(a, z)[0], dy + L * s2, Q(a, z)[1], dy + L * s2 + 6 + 4 * holes.index((hid, a, z, d_, note)), f"{((a + 90) % 360) / 360 * circ:.1f}", size=4)
    ty = cell.y + cell.h - 11
    for i, (hid, a, z, d_, note) in enumerate(holes):
        ax.text(cell.x + 3, ty - 3.8 * i, f"{hid}: {note}, at {a:.1f}° ({a / 360 * circ:.1f} along arc), {z:g} from shell bottom (Z{z + z0:g})", fontsize=4.1, va="top", zorder=5)

def group_body(cell):
    """Item 35: group body casting - vertical section through X-Z + top view."""
    ax = cell.ax; gx = D["GX"]; z0 = D["BELL_Z0"]
    s = 1.0; cell.set_scale(s)
    ox, oy = cell.x + 72, cell.y + 22
    P = lambda x, z: (ox + x * s, oy + z * s)       # x rel. group axis, z rel. bell bottom (Z176)
    rb = D["BODY_D"] / 2; top = D["BODY_Z1"] - z0
    sk_d = 12; gr0, gr1 = sk_d, sk_d + 5.3; scr = gr1 + 1; bore_top = top - 8
    fl0, fl1 = D["PAD_X1"] - gx, D["FL_X1"] - gx; pz = D["PORT_Z"] - z0
    c0, c1 = D["COL_X0"] - gx, D["COL_X1"] - gx; ctop = D["YOKE_Z1"] - z0; fz = D["FZ"] - z0; fx = D["FX"] - gx
    for sg in (1, -1):
        prof = [(sg * 31.25, 0), (sg * 36, 0), (sg * 36, 20), (sg * rb, 30), (sg * rb, top), (sg * 5.25, top), (sg * 5.25, top - 2),
                (sg * 10, top - 2), (sg * 10, bore_top), (sg * 22, bore_top), (sg * 22, scr), (sg * 26, scr), (sg * 26, gr1),
                (sg * 28.85, gr1), (sg * 28.85, gr0), (sg * 31.25, gr0)]
        ax.add_patch(Polygon([P(*p) for p in prof], closed=True, fc=HATCH_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    # flange + neck (left = rear, towards boiler)
    ax.add_patch(Polygon([P(fl0, pz - 24), P(fl1, pz - 24), P(fl1, pz - 11), P(-rb, pz - 11), P(-rb, pz + 11), P(fl1, pz + 11), P(fl1, pz + 24), P(fl0, pz + 24)],
                         closed=True, fc=HATCH_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Rectangle(P(fl0, pz - 4), (-22 - fl0) * s, 8 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    for zb in (pz - 19, pz + 19):
        ax.add_patch(Rectangle(P(fl0, zb - 3.2), (fl1 - fl0) * s, 6.4 * s, fc="white", ec=INK, lw=0.4, zorder=4))
    # column
    ax.add_patch(Polygon([P(c0, top - 4), P(c1, top - 4), P(c1, ctop), P(c0, ctop)], closed=True, fc="#eeeeee", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Circle(P(fx, fz), 5.05, fc="white", ec=INK, lw=0.5, zorder=4))
    cl(ax, P(0, -4), P(0, ctop + 4)); cl(ax, P(fl0 - 4, pz), P(-15, pz))
    # dims - vertical chain on the right
    xr = P(36, 0)[0] + 6
    for a, b, lab in ((0, sk_d, f"{sk_d} skirt"), (sk_d, gr1, "5.3"), (gr1, scr, "1"), (scr, bore_top, f"{bore_top - scr:.1f} bore"), (bore_top, top - 2, "6 recess"), (top - 2, top, "2"),
                      (top, ctop, f"{ctop - top:g}")):
        vdim(ax, P(0, a)[1], P(0, b)[1], P(36, a)[0], P(36, b)[0], xr, lab, side="right")
    vdim(ax, P(0, 0)[1], P(0, top)[1], xr, xr, xr + 9, f"{top} body", side="right")
    vdim(ax, P(0, 0)[1], P(0, 20)[1], P(-36, 0)[0], P(-36, 20)[0], P(-36, 0)[0] - 5, "20 bell")
    hdim(ax, P(-36, 0)[0], P(36, 0)[0], P(0, 0)[1], P(0, 0)[1], P(0, 0)[1] - 5, "Ø72 bell [D]")
    hdim(ax, P(-31.25, 0)[0], P(31.25, 0)[0], P(0, 0)[1], P(0, 0)[1], P(0, 0)[1] - 10, "Ø62.5 skirt ID")
    hdim(ax, P(-22, 0)[0], P(22, 0)[0], P(0, scr + 10)[1], P(0, scr + 10)[1], P(0, scr + 10)[1], "Ø44 H8 bore [D]")
    hdim(ax, P(-28.85, 0)[0], P(28.85, 0)[0], P(0, gr0)[1], P(0, gr0)[1], P(0, gr0)[1] + 2.4, "Ø57.7 groove", size=4)
    hdim(ax, P(-rb, 0)[0], P(rb, 0)[0], P(0, top)[1], P(0, top)[1], P(0, top)[1] + 4, f"Ø{D['BODY_D']} body [E]")
    leader(ax, P(8, bore_top + 1), (P(8, 0)[0] + 18, P(0, top)[1] + 12), "Ø20 x 6 seal recess (circlip groove Ø21 x 1.1 at its foot), 2 lip, Ø10.5 rod hole")
    leader(ax, P(fl0 + 1, pz + 19), (P(fl0, 0)[0] - 5, P(0, pz + 34)[1]), "2x Ø6.4 THRU on 38 c/c (M6x10 bolts)")
    leader(ax, P(-28, pz), (P(fl0, 0)[0] - 5, P(0, pz + 8)[1]), "port Ø8 THRU to bore")
    vdim(ax, P(0, 0)[1], P(0, pz)[1], P(fl0, pz)[0], P(fl0, pz)[0], P(fl0, 0)[0] - 4, f"{pz:g} port C/L")
    hdim(ax, P(fl0, 0)[0], P(0, 0)[0], P(fl0, pz - 24)[1], P(0, 0)[1], P(0, pz - 32)[1], f"{-fl0:g}")
    hdim(ax, P(fl0, 0)[0], P(fl1, 0)[0], P(fl0, pz + 24)[1], P(fl1, pz + 24)[1], P(0, pz + 30)[1], f"{fl1 - fl0:g}", size=4)
    vdim(ax, P(0, pz - 24)[1], P(0, pz + 24)[1], P(fl0, 0)[0], P(fl0, 0)[0], P(fl0, 0)[0] - 12, "48 flange")
    hdim(ax, P(c0, 0)[0], P(c1, 0)[0], P(0, ctop)[1], P(0, ctop)[1], P(0, ctop)[1] + 4, f"{c1 - c0} column")
    leader(ax, P(fx, fz), (P(c0, 0)[0] - 10, P(0, ctop + 6)[1]), f"fulcrum bore Ø10.1 H8 (roller 52) @ x{fx:g}, z{fz:g}")
    ax.text(cell.x + 3, cell.y + cell.h - 11, "Section on X-Z plane. x from group axis (- = towards boiler), z from bell bottom face (= Z176 machine).\n"
            "Column 16 wide (Y), flange 26 wide (Y). Bayonet: 2 ramps 45° long, 3.5 deep, 1:12 rise inside skirt.", fontsize=4.2, va="top", color=NOTE)
    # top view (right)
    tx, ty = cell.x + cell.w - 62, cell.y + cell.h * 0.48
    T = lambda x, y: (tx + x * 0.8, ty + y * 0.8)
    ax.add_patch(Circle(T(0, 0), 36 * 0.8, fc="#eeeeee", ec=INK, lw=0.5, zorder=3)); ax.add_patch(Circle(T(0, 0), rb * 0.8, fc="#e2e2e2", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Rectangle(T(c0, -8), (c1 - c0) * 0.8, 16 * 0.8, fc="#d8d8d8", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Rectangle(T(fl0, -13), (fl1 - fl0) * 0.8, 26 * 0.8, fc="#d8d8d8", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Circle(T(0, 0), 5.25 * 0.8, fc="white", ec=INK, lw=0.5, zorder=5))
    ax.text(tx, ty - 36 * 0.8 - 4, "TOP VIEW (1:1.25)", fontsize=4.4, ha="center")
    hdim(ax, T(c0, 0)[0], T(0, 0)[0], T(c0, 8)[1], T(0, 0)[1], T(0, 30)[1], f"{-c0:g}", size=4)
    vdim(ax, T(0, -8)[1], T(0, 8)[1], T(c1, -8)[0], T(c1, 8)[0], T(c1, 0)[0] + 3, "16", size=4, side="right")
    vdim(ax, T(0, -13)[1], T(0, 13)[1], T(fl0, -13)[0], T(fl0, 13)[0], T(fl0, 0)[0] - 3, "26", size=4)

def pad_drawing(cell):
    """Item 69: boiler boss / pad (brazed to shell)."""
    holes = [("A", 13, 5, 5, "Ø5 ↧7.5, M6 ↧6"), ("B", 13, 43, 5, "Ø5 ↧7.5, M6 ↧6"), ("C", 13, 24, 6, "Ø6 ↧4; Ø8 H7 ↧4 from back"),
             ("D", 13, 24, 16, "seal recess Ø16 x 1.2 deep")]
    P, s = plate(cell, [(0, 0), (26, 0), (26, 48), (0, 48)], holes, 10, "face Ra 1.6, flat 0.02. Back R40 concave on Ø80 shell: 8 thick on C/L, 10 at edges.")
    ax = cell.ax
    hdim(ax, P(0, 0)[0], P(13, 0)[0], P(0, 48)[1], P(13, 48)[1], P(0, 48)[1] + 4, "13", size=4)
    vdim(ax, P(0, 0)[1], P(0, 5)[1], P(26, 0)[0], P(26, 5)[0], P(26, 0)[0] + 4, "5", side="right", size=4)
    vdim(ax, P(0, 5)[1], P(0, 43)[1], P(26, 5)[0], P(26, 43)[0], P(26, 0)[0] + 10, "38 c/c", side="right", size=4)
    vdim(ax, P(0, 0)[1], P(0, 24)[1], P(0, 0)[0], P(13, 24)[0], P(0, 0)[0] - 12, "24 port", size=4)

def _eared(rc, pcd_r, er, n=3, start=90, res=720):
    pts = []
    for k in range(res):
        a = 2 * math.pi * k / res; r = rc
        for e in range(n):
            ea = math.radians(start + 360 / n * e); d = (a - ea + math.pi) % (2 * math.pi) - math.pi
            h = pcd_r * math.sin(d)
            if abs(h) <= er and abs(d) < math.pi / 2: r = max(r, pcd_r * math.cos(d) + math.sqrt(er * er - h * h))
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

def ringnut_drawing(cell):
    """Item 4: boiler-to-base ring nut with 3 ears."""
    ax = cell.ax
    pts = _eared(49, 52, 8)
    holes = [(f"E{e + 1}", round(52 * math.cos(math.radians(90 + 120 * e)), 2), round(52 * math.sin(math.radians(90 + 120 * e)), 2), 5, "M6 THRU (element screws)") for e in range(3)]
    holes.append(("T", 0, 0, 80, "M80x1.25-6H THRU (fine pitch, 1978-96)"))
    P, s = plate(cell, pts, holes, 12, "3 ears R8 on PCD 104 @ 90/210/330°. Chamfer thread 1x45° both ends.")
    ax.add_patch(Circle(P(0, 0), 52 * s, fc="none", ec=DIMC, lw=0.3, ls=(0, (6, 2, 1, 2)), zorder=5))
    leader(ax, P(52 * math.cos(math.radians(30)), 52 * math.sin(math.radians(30))), (P(60, 40)[0], P(60, 40)[1]), "PCD 104")
    leader(ax, P(-49 * 0.707, -49 * 0.707), (P(-60, -55)[0], P(-60, -55)[1]), "Ø98 OD")

def element_drawing(cell):
    """Item 6: heating element 200 W + 800 W, brass flange."""
    ax = cell.ax
    pts = _eared(42, 52, 7.5)
    holes = [(f"E{e + 1}", round(52 * math.cos(math.radians(90 + 120 * e)), 2), round(52 * math.sin(math.radians(90 + 120 * e)), 2), 6.5, "Ø6.5 THRU") for e in range(3)]
    for k, (nm, a) in enumerate((("T1 (R1)", 45), ("T2 (R1/R2 common)", 135), ("T3 (R2)", 225), ("T4", 315))):
        holes.append((nm.split()[0], round(17 * math.cos(math.radians(a)), 2), round(17 * math.sin(math.radians(a)), 2), 8, nm + ": ceramic bush Ø8, M4 stud, 6.3 tab"))
    holes.append(("PE", 0, -30, 4.2, "M4 earth stud"))
    plate(cell, pts, holes, 8, "Flange brass, sealing face Ø68-82 Ra 3.2. Coils: copper sheath Ø8 [V].")
    ax.text(cell.x + 3, cell.y + 9, "R2 800 W: 6 turns on Ø52 coil C/L, pitch 12, legs 12 high.  R1 200 W: 4 turns on Ø30, pitch 12.\n"
            "Coil stack height 72 above flange (Z52-Z124). Leads brazed through flange. Resistance @20°C: R1 242 Ω, R2 60.5 Ω (220 V).",
            fontsize=4.1, va="bottom", color=NOTE)

def base_drawing(cell):
    """Item 61: base shell - plan with every hole + side elevation."""
    outline = rounded_trap(D["W_REAR"], D["W_FRONT"], D["L"], D["BASE_R"], n=12)
    outline = [(x, y) for x, y in outline]
    holes = [("B", D["BX"], 0, 81, "Ø81 boiler hole (top face)"), ("G", D["TRAY_X0"] + 70.5, 0, 6, "Ø6 tray drain (recess floor)"),
             ("S", D["SW_X"], -90, 0, f"switch cut-out 30x22 in LEFT wall, centre Z{D['SW_Z']}"),
             ("L1", 265, D["BADGE_Y"] - 6, 2.2, "badge pin Ø2.2 (FRONT wall Z33)"), ("L2", 265, D["BADGE_Y"] + 6, 2.2, "badge pin Ø2.2 (FRONT wall Z33)"),
             ("C", 0, 40, 16.5, "Ø16.5 gland hole (REAR wall Z25)"),
             ("R", D["TRAY_X0"], 0, 0, f"tray recess {D['TRAY_L']}x{D['TRAY_W']}, R26 corners, 1 deep")]
    P, s = plate(cell, outline, holes, 1.0, "Deep drawn DC04 steel, walls drafted 6 mm in over 52 high, height 60 [V]. Top flange turned in 8.")
    ax = cell.ax
    for x0, y0 in [(D["TRAY_X0"], 0)]:
        tr = [(x + x0, y) for x, y in rounded_trap(D["TRAY_W"], D["TRAY_W"] - 4, D["TRAY_L"], 26)]
        ax.add_patch(Polygon([P(*p) for p in tr], closed=True, fc="none", ec=INK, lw=0.5, ls=(0, (3, 1.5)), zorder=5))
    hdim(ax, P(0, 0)[0], P(D["BX"], 0)[0], P(0, 0)[1], P(D["BX"], 0)[1], P(0, 95)[1], f"{D['BX']}", size=4)
    hdim(ax, P(D["BX"], 0)[0], P(D["TRAY_X0"], 0)[0], P(D["BX"], 0)[1], P(D["TRAY_X0"], 0)[1], P(0, 95)[1], f"{D['TRAY_X0'] - D['BX']}", size=4)
    hdim(ax, P(D["TRAY_X0"], 0)[0], P(D["TRAY_X0"] + D["TRAY_L"], 0)[0], P(0, 0)[1], P(0, 0)[1], P(0, 95)[1], f"{D['TRAY_L']}", size=4)
    vdim(ax, P(0, -D["W_FRONT"] / 2)[1], P(0, D["W_FRONT"] / 2)[1], P(D["L"], 0)[0], P(D["L"], 0)[0], P(D["L"], 0)[0] + 5, f"{D['W_FRONT']} front", side="right", size=4)

def sgblock_drawing(cell):
    """Item 19: sight-glass block (upper shown; lower is mirrored)."""
    ax = cell.ax; s = 3; cell.set_scale(s)
    ox, oy = cell.x + 34, cell.y + 24
    P = lambda x, z: (ox + x * s, oy + z * s)
    ax.add_patch(Polygon([P(0, 0), P(18, 0), P(18, 18), P(0, 18)], closed=True, fc=HATCH_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(18, 3), P(32, 3), P(32, 15), P(18, 15)], closed=True, fc=HATCH_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Rectangle(P(5, 6.5), 27 * s, 5 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Rectangle(P(2.9, 0), 12.2 * s, 9 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Rectangle(P(4.6, 9), 8.8 * s, 3.5 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Polygon([P(0, -8), P(18, -8), P(18, 0), P(0, 0)], closed=True, fc=HATCH_FC, hatch="\\\\\\\\", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Rectangle(P(2.9, -8), 12.2 * s, 8 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Rectangle(P(4.5, 18), 9 * s, 0.01, fc="none", zorder=4))
    for x in np.arange(18, 32, 1): ax.plot([P(x, 3)[0], P(x + 0.5, 15)[0]], [P(x, 3)[1], P(x + 0.5, 3.6)[1]], lw=0, zorder=2)
    cl(ax, P(9, -12), P(9, 22)); cl(ax, P(-3, 9), P(35, 9))
    hdim(ax, P(0, 0)[0], P(18, 0)[0], P(0, -8)[1], P(18, -8)[1], P(0, -8)[1] - 5, "18 sq.")
    hdim(ax, P(18, 0)[0], P(32, 0)[0], P(18, 3)[1], P(32, 3)[1], P(0, -8)[1] - 5, "14 spigot")
    vdim(ax, P(0, -8)[1], P(0, 0)[1], P(0, -8)[0], P(0, 0)[0], P(0, 0)[0] - 5, "8")
    vdim(ax, P(0, 0)[1], P(0, 18)[1], P(0, 0)[0], P(0, 18)[0], P(0, 0)[0] - 5, "18")
    leader(ax, P(25, 15), (P(28, 0)[0], P(0, 22)[1]), "M12x1-6g x 14 (spigot to boiler) [D: D12 nut]")
    leader(ax, P(20, 9), (P(36, 0)[0], P(0, 12)[1]), "Ø5 passage")
    leader(ax, P(9, 4), (P(36, 0)[0], P(0, 3)[1]), "Ø12.2 ↧9 glass bore")
    leader(ax, P(9, 11), (P(36, 0)[0], P(0, 7)[1]), "M10x1 ↧3.5 plug thread (top end)")
    leader(ax, P(9, -5), (P(36, 0)[0], P(0, -6)[1]), "M16x1-6g x 8 gland boss, Ø12.2 bore")
    ax.text(cell.x + 3, cell.y + 3, "Upper block: gland boss DOWN, plug UP. Lower block: mirror (gland UP, plug DOWN). Hatch: section through C/L.", fontsize=4.1, color=NOTE)

def _branch(ax, X, Y, s):
    ax.add_patch(Polygon([(X(21), Y(-7.5)), (X(35), Y(-7.5)), (X(35), Y(-14.5)), (X(21), Y(-14.5))], closed=True, fc="#f3f3f3", ec=INK, lw=0.6, zorder=6))
    ax.add_patch(Polygon([(X(23), Y(-14.5)), (X(33), Y(-14.5)), (X(33), Y(-22.5)), (X(23), Y(-22.5))], closed=True, fc="#f3f3f3", ec=INK, lw=0.6, zorder=6))
    for xx in (23.6, 32.4): ax.plot([X(xx), X(xx)], [Y(-14.5), Y(-22.5)], lw=0.3, color=INK, zorder=7)
    for xx in (26.5, 29.5): ax.plot([X(xx), X(xx)], [Y(-3), Y(-22.5)], lw=0.3, ls=(0, (3, 1.5)), color=INK, zorder=7)
    vdim(ax, Y(-7.5), Y(-14.5), X(35), X(35), X(35) + 4, "7", side="right", size=4)
    vdim(ax, Y(-14.5), Y(-22.5), X(33), X(33), X(35) + 4, "8 M10x1", side="right", size=4)
    hdim(ax, X(21), X(35), Y(-14.5), Y(-14.5), Y(-22.5) - 4, "Ø14 boss", size=4)

def valvebody_drawing(cell):
    """Item 25: steam valve body (T piece)."""
    spec = dict(segs=[dict(L=8, D=12, t="M12x1"), dict(L=6, hex=17), dict(L=24, D=15), dict(L=10, D=12, t="M12x1")],
                bl=[(14, 4)], br=[(10, 10.1, "M12x1-6H"), (10, 8, "M8x1-6H"), (8, 5)], xholes=[(28, 3, "outlet to wand branch")], fc=HATCH_FC, extra=_branch,
                notes=["Branch at x28: boss Ø14 x 7 down, M10x1-6g, bore Ø3 (wand union).",
                       "Seat: 90° cone at Ø4 / Ø5 step (x14). Internal threads left->right from rear end."])
    turned(cell, spec)

def lever_drawing(cell):
    """Item 49: lever = 2 fork cheeks + Ø16 boss + Ø11 rod (+ handle 53 on M8 stud). Side view + top view, lever laid horizontal."""
    ax = cell.ax; pin = 27.6; L = D["LEV_L"]; hl = D["HANDLE_L"]
    s = 0.4; cell.set_scale(s)
    ox, oy = cell.x + 16, cell.y + cell.h * 0.66
    P = lambda x, y: (ox + (x + 14) * s, oy + y * s)
    cheek = [(-14, -8), (pin + 10, -8), (pin + 22, -6), (pin + 22, 6), (pin + 10, 8), (-14, 8)]
    ax.add_patch(Polygon([P(*p) for p in cheek], closed=True, fc="#3a3a3a", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(pin + 22, -8), P(pin + 37, -8), P(pin + 37, 8), P(pin + 22, 8)], closed=True, fc="#d8d8d8", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(pin + 37, -5.5), P(L - hl, -5.5), P(L - hl, 5.5), P(pin + 37, 5.5)], closed=True, fc="#eeeeee", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(L - hl, -10), P(L, -11), P(L, 11), P(L - hl, 10)], closed=True, fc="#e8d2b0", ec=INK, lw=0.6, zorder=3, hatch="----"))
    for x in (0, pin): ax.add_patch(Circle(P(x, 0), 3.05 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    cl(ax, P(-18, 0), P(L + 4, 0))
    yb = P(0, -11)[1] - 4
    hdim(ax, P(0, 0)[0], P(pin, 0)[0], P(0, 0)[1], P(pin, 0)[1], yb, f"{pin} pin c/c", size=4)
    hdim(ax, P(-14, 0)[0], P(0, 0)[0], P(-14, -8)[1], P(0, 0)[1], yb, "14", size=4)
    hdim(ax, P(pin, 0)[0], P(pin + 22, 0)[0], P(pin, 0)[1], P(pin + 22, -6)[1], yb, "22", size=4)
    hdim(ax, P(pin + 22, 0)[0], P(pin + 37, 0)[0], P(pin + 22, -8)[1], P(pin + 37, -8)[1], yb, "15 boss", size=4)
    hdim(ax, P(pin + 37, 0)[0], P(L - hl, 0)[0], P(pin + 37, -5.5)[1], P(L - hl, -5.5)[1], yb, f"{L - hl - pin - 37:.1f} rod Ø11 (+15 in boss)", size=4)
    hdim(ax, P(L - hl, 0)[0], P(L, 0)[0], P(L - hl, -10)[1], P(L, -11)[1], yb, f"{hl} handle", size=4)
    hdim(ax, P(0, 0)[0], P(L, 0)[0], P(0, 0)[1], P(L, -11)[1], yb - 7, f"{L} fulcrum to handle end", size=4.4)
    vdim(ax, P(0, -8)[1], P(0, 8)[1], P(-14, -8)[0], P(-14, 8)[0], P(-14, 0)[0] - 4, "16", size=4)
    leader(ax, P(pin + 30, 8), (P(pin + 30, 0)[0] + 8, P(0, 8)[1] + 9), "boss Ø16, rod pressed ↧15 + Ag-braze")
    leader(ax, P(0, 0), (P(0, 0)[0] - 2, P(0, 8)[1] + 9), "Ø6.1 H8 fulcrum")
    leader(ax, P(pin, 0), (P(pin, 0)[0] + 2, P(0, 8)[1] + 15), "Ø6.1 H8 rod pin")
    leader(ax, P(L - 40, 10.5), (P(L - 40, 0)[0] - 6, P(0, 11)[1] + 9), "handle Ø20→Ø22, M8 insert ↧25")
    # top view
    oy2 = cell.y + cell.h * 0.26
    Q = lambda x, y: (ox + (x + 14) * s, oy2 + y * s)
    for yy in (9, -12):
        ax.add_patch(Polygon([Q(-14, yy), Q(pin + 22, yy), Q(pin + 22, yy + 3), Q(-14, yy + 3)], closed=True, fc="#3a3a3a", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Polygon([Q(pin + 22, -8), Q(pin + 37, -8), Q(pin + 37, 8), Q(pin + 22, 8)], closed=True, fc="#d8d8d8", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Polygon([Q(pin + 37, -5.5), Q(L - hl, -5.5), Q(L - hl, 5.5), Q(pin + 37, 5.5)], closed=True, fc="#eeeeee", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Polygon([Q(L - hl, -10), Q(L, -11), Q(L, 11), Q(L - hl, 10)], closed=True, fc="#e8d2b0", ec=INK, lw=0.5, zorder=3))
    for yy in (-16, 16): ax.plot([Q(0, yy)[0], Q(0, yy)[0]], [Q(0, yy)[1], Q(0, -yy)[1]], lw=0.2, color="#555", ls=(0, (3, 1.5)), zorder=4)
    vdim(ax, Q(0, -12)[1], Q(0, 12)[1], Q(-14, -12)[0], Q(-14, 12)[0], Q(-14, 0)[0] - 4, "24", size=4)
    vdim(ax, Q(0, -9)[1], Q(0, 9)[1], Q(pin + 22, -9)[0], Q(pin + 22, 9)[0], Q(pin + 22, 0)[0] + 3, "18 gap", size=4, side="right")
    ax.text(*Q(L / 2, -22), "TOP VIEW: cheeks 3 thick, 18 gap straddles column (16) + rod eye", fontsize=4.2, ha="center")
    ax.text(cell.x + 3, cell.y + 3, f"Assembled: fulcrum X{D['FX']} Z{D['FZ']}, rod pin X{D['ROD_PIN_X']} Z{D['ROD_PIN_Z']}, rest {D['LEV_ANG']}° below horizontal. Ratio {L}/{pin} = {L / pin:.1f}:1.",
            fontsize=4.1, va="bottom", color=NOTE)

def grid_drawing(cell):
    outline = [(x - D["TRAY_X0"], y) for x, y in rounded_trap(112, 108, 141, 26, x0=D["TRAY_X0"])]
    P, s = plate(cell, outline, [("P", 12, -44, 8, "pattern: 10 x 8 holes Ø8, pitch 13 x 12.6, first at X12 Y-44; 4 centre holes omitted; centre Ø5")], 0.8,
                 "AISI 304, deburred; 76 holes Ø8 + Ø5 centre.")
    ax = cell.ax
    for i in range(10):
        for j in range(8):
            if abs(i - 4.5) < 1 and abs(j - 3.5) < 1: continue
            ax.add_patch(Circle(P(12 + i * 13, -44 + j * 12.6), 4 * s, fc="white", ec=INK, lw=0.3, zorder=4))
    ax.add_patch(Circle(P(70.5, 0), 2.5 * s, fc="white", ec=INK, lw=0.3, zorder=4))
    hdim(ax, P(12, 0)[0], P(25, 0)[0], P(12, -44)[1], P(25, -44)[1], P(0, -60)[1], "13", size=4)
    vdim(ax, P(0, -44)[1], P(0, -31.4)[1], P(12, -44)[0], P(12, -31.4)[0], P(0, 0)[0] - 3, "12.6", size=4)

# ================================================================== part catalogue: (item, name, material, qty, conf, kind, data, note)
TURNED = {
 3: ("Foot casting (flare + spigot)", BR + CHR + " (flare only)", 1, "D/V/E", dict(
     segs=[dict(L=20, D=80, t="M80x1.25"), dict(L=3, D=92), dict(L=6, D=92, D2=83)], bl=[(29, 68)], br=[(7, 80.2)],
     notes=["Spigot M80x1.25-6g (fine pitch 1978-96) [D].", "Socket Ø80.2 x 7 receives shell; Ag-braze.", "Spigot end face = element seal face, Ra 3.2."])),
 2: ("Shoulder / neck casting", BR + CHR, 1, "V/E", dict(
     segs=[dict(L=8, D=83), dict(L=15, D=83, D2=48), dict(L=4, D=48, D2=44), dict(L=10, D=44)], bl=[(8, 80.2), (15, 76)], br=[(12, 38, "M38x1.5-6H"), (2, 36)],
     notes=["x0 = Z240. Socket Ø80.2 x 8 on shell.", "Bosses: safety valve M12x1.5 ↧10 @ Z252 r32 (+X+Y 20°);", "steam valve M12x1 ↧8 radial @ Z258 (-X)."])),
 9: ("Cap insert", BRB, 1, "V/E", dict(segs=[dict(L=16, D=38, t="M38x1.5"), dict(L=3, D=44), dict(L=6, D=20)], bl=[(25, 6.8)], br=[(14, 8, "M8-6H")],
     notes=["Screws INTO the neck (v2 cap) [D].", "Gasket 10 seats under the Ø44 flange."])),
 11: ("Cap knob, 6-lobe", "Birdseye maple, hard-wax oil (orig. black phenolic)", 1, "V", dict(
     segs=[dict(L=27, D=28, D2=38), dict(L=20, D=58, lobes=6)], bl=[(6, 20.5), (33, 8.5)], br=[(8, 13.5)], fc="#e8d2b0", hatch="----",
     notes=["Lobe root Ø49, 6 lobes R8.", "Counterbore Ø13.5 x 8 for M8 cap screw head."])),
 12: ("Cap screw M8x35", "Stainless A2-70, ISO 4762", 1, "V/E", dict(segs=[dict(L=8, D=13), dict(L=35, D=8, t="M8")], bl=[(5, 6.9)], notes=["Hex socket AF6 x 5 deep."])),
 13: ("Safety-valve body", BRB + CHR, 1, "D/E", dict(segs=[dict(L=8, D=12, t="M12x1.5"), dict(L=6, hex=14), dict(L=8, D=10, t="M10x1")],
     bl=[(8, 4)], br=[(14, 6.5)], notes=["Ball seat: 90° cone Ø4->Ø6.5 at x8.", "M12 thread [D] (P37 type, pre-millennium)."])),
 16: ("Safety-valve cup", BRB + CHR, 1, "V/E", dict(segs=[dict(L=24, D=22)], bl=[(8, 9, "M10x1-6H"), (14, 18)], xholes=[(16, 5, "drain-tube socket")],
     notes=["Top closed 2 thick. Spring seat Ø6.5 boss inside top."])),
 17: ("Sight-glass tube", "Borosilicate 3.3 glass", 1, "V/E", dict(segs=[dict(L=123, D=12)], bl=[(123, 9)], fc="#cfe8f5", hatch="",
     notes=["Ends fire-polished, square ±0.3.", "Later models use 12x106 (different block c/c)."])),
 18: ("Glass guard (slotted sleeve)", "Brass tube" + CHR, 1, "V/E", dict(segs=[dict(L=97, D=16)], bl=[(97, 14.4)],
     notes=["Front slot 8 wide x 80 long, centred.", "Original is chrome brass (1979); later ABS."])),
 20: ("Gland nut M16x1", BRB + CHR, 2, "V/E", dict(segs=[dict(L=6, hex=17)], bl=[(4, 14.9, "M16x1-6H"), (2, 12.5)])),
 21: ("Lock nut M12x1 (D12)", BRB, 2, "D/E", dict(segs=[dict(L=5, hex=17)], bl=[(5, 10.9, "M12x1-6H")])),
 24: ("Plug M10x1, slotted (top)", BRB + CHR, 2, "V/E", dict(segs=[dict(L=3, D=14), dict(L=6, D=10, t="M10x1")], notes=["Slot 1.6 x 1.5 deep. Item 70 = bottom plug, identical."])),
 26: ("Steam-valve stem (needle)", SS, 1, "V/E", dict(segs=[dict(L=4, D=1.5, D2=5), dict(L=10, D=5), dict(L=14, D=8, t="M8x1"), dict(L=34, D=6)],
     xholes=[(57, 2.5, "knob pin")], notes=["Needle 60° included.", "Ø6 polished Ra 0.4 through packing."])),
 27: ("Packing nut", BRB + CHR, 1, "D/E", dict(segs=[dict(L=8, D=12, t="M12x1"), dict(L=5, hex=14)], bl=[(13, 6.2)], notes=["AF14 [D]."])),
 30: ("Steam knob, 6-lobe", "Birdseye maple (orig. phenolic)", 1, "V", dict(segs=[dict(L=22, D=37, D2=31, lobes=6)], bl=[(18, 6)],
     xholes=[(9, 2.5, "pin, through")], fc="#e8d2b0", hatch="----")),
 31: ("Knob pin", "Stainless spring pin ISO 8752", 1, "E", dict(segs=[dict(L=30, D=2.5)])),
 33: ("Wand union nut", BRB + CHR, 1, "V/E", dict(segs=[dict(L=8, hex=14)], bl=[(6, 8.9, "M10x1-6H"), (2, 8.2)])),
 34: ("Steam tip (ball end)", BRB + CHR, 1, "V/E", dict(segs=[dict(L=6, D=8), dict(L=7, D=9)], bl=[(4, 6.1)], br=[(9, 1.2)], notes=["Brazed on wand; Ø9 spherical end, 1 hole Ø1.2."])),
 36: ("Piston", BRB, 1, "D/E", dict(segs=[dict(L=4, D=43.9, tol="f7"), dict(L=5.6, D=36), dict(L=7.4, D=43.9), dict(L=5.6, D=36), dict(L=7.4, D=43.9)],
     br=[(16, 6.8, "M8-6H")], notes=["Grooves take 44x36x5.5 lip seals, lips DOWN.", "Stroke 27.7 -> 42 ml displacement."])),
 38: ("Piston rod", "Steel, hard chrome 20 µm (or AISI 303)", 1, "V/E", dict(segs=[dict(L=14, D=8, t="M8"), dict(L=39, D=10, tol="f7"), dict(L=12, D=10),
     dict(L=19, D=10), dict(L=14, D=8, t="M8")], xholes=[(59.1, 6.1, "rod pin, H8")], notes=["Ø10 f7 Ra 0.2 through rod seal.", "Top M8: check nut 47 + acorn 48."])),
 40: ("Rod washer", SS4, 1, "D/E", dict(segs=[dict(L=1, D=20)], bl=[(1, 10.5)])),
 43: ("Shower screen", SS4 + " 0.3 sheet + mesh", 1, "D", dict(segs=[dict(L=1, D=52)], notes=["Ø52 (IMS PA200IM52 fits) [D]."])),
 46: ("Group bolt M6x10", "Stainless A2-70, ISO 4017", 2, "D/V", dict(segs=[dict(L=4, hex=10), dict(L=10, D=6, t="M6")], notes=["5 mm engagement in boss 69; 6 Nm [E]."])),
 47: ("Check nut M8", "Brass" + CHR, 1, "D/E", dict(segs=[dict(L=6, hex=13)], bl=[(6, 6.8, "M8-6H")])),
 48: ("Acorn nut M8", "Brass" + CHR + ", DIN 1587", 1, "D", dict(segs=[dict(L=10, hex=13), dict(L=5, D=12, D2=6)], bl=[(9, 6.8, "M8-6H")])),
 50: ("Lever pin Ø6", SS, 2, "D/V", dict(segs=[dict(L=1.5, D=6), dict(L=0.7, D=5), dict(L=29.6, D=6, tol="h8"), dict(L=0.7, D=5), dict(L=1.5, D=6)],
     notes=["Grooves Ø5 x 0.7 for E-clip DIN 6799-5."])),
 52: ("Lever roller / bush", BRB, 1, "D/E", dict(segs=[dict(L=16, D=10, tol="f7")], bl=[(16, 6.05)], notes=["Runs in column bore Ø10.1 H8 on fulcrum pin 50."])),
 53: ("Lever handle", "Birdseye maple (orig. black ribbed ABS)", 1, "V", dict(segs=[dict(L=101, D=20, D2=22)], bl=[(25, 6.8, "M8 insert")], fc="#e8d2b0", hatch="----")),
 54: ("Portafilter body", BR + CHR, 1, "D/V", dict(segs=[dict(L=4, D=26), dict(L=24, D=56, D2=60)], bl=[(4, 10, "M10x1-6H")], br=[(24, 52)],
     notes=["2 bayonet lugs 8 wide x 4 radial at 180°, 3.5 thick, top flush.", "Handle boss Ø15 radial, M8 x 14 (stud 59).", "Inside Ø52 [D]; basket seat 49."])),
 55: ("Double spout", BR + CHR, 1, "V", dict(segs=[dict(L=6, D=10, t="M10x1"), dict(L=8, D=14, D2=12)], bl=[(14, 5)], notes=["2 outlets Ø4 at ±40°, 30 c/c at tip [V]."])),
 59: ("Handle stud M8x75", "Stainless A2", 1, "V/E", dict(segs=[dict(L=75, D=8, t="M8")])),
 60: ("Portafilter handle", "Birdseye maple (orig. black PP)", 1, "V", dict(segs=[dict(L=100, D=22, D2=24)], bl=[(60, 6.8, "M8 insert")], fc="#e8d2b0", hatch="----")),
 66: ("Cable gland M16x1.5", "Nickel-plated brass + PA insert", 1, "V/E", dict(segs=[dict(L=7, D=16, t="M16x1.5"), dict(L=3, hex=22), dict(L=10, D=18, D2=12)], bl=[(20, 8)])),
 25: None,
}
RINGS = {
 5: ("Boiler / base gasket", "Fibre AFM34, food safe", 2, "D", (93, 80, 2, "flat"), "La Pavoni 362019."),
 7: ("Element gasket", "Fibre AFM34", 1, "D", (82, 68, 2, "flat"), "La Pavoni 362018 (1959-96, brass element)."),
 10: ("Cap gasket", "Silicone VMQ 60 ShA", 1, "E", (44, 38.5, 2, "flat"), ""),
 22: ("Glass seal", "Silicone VMQ, square section", 2, "E", (17, 12, 4, "flat"), ""),
 23: ("Spigot washer", "PTFE", 4, "D/V", (18, 12, 1, "flat"), "Teflon + brass washers per parts list [D]."),
 28: ("Stem packing", "EPDM 70 ShA", 1, "V/E", (11, 6, 6, "flat"), ""),
 29: ("Stem washer", "Brass", 2, "V", (11, 6.2, 0.8, "flat"), ""),
 37: ("Piston seal (lip)", "Silicone VMQ 70 ShA (orig. NBR)", 2, "D", (44, 36, 5.5, "lip"), "Some kits list 44x33x5.5."),
 39: ("Rod seal (lip)", "PTFE / silicone", 1, "D/E", (20, 10, 4, "lip"), "'Lip gasket for piston shaft' [D]."),
 41: ("Circlip DIN 472-20", "Spring steel", 1, "D", (20, 17, 1, "flat"), "'C-lock ring 20 mm' [D]. Groove Ø21 x 1.1."),
 42: ("Group gasket", "Silicone VMQ (orig. NBR 70)", 1, "D", (57.7, 47, 5.3, "flat"), "Pre-millennium 'old group' [D]."),
 44: ("Port seal (Cu washer)", "Annealed copper (alt. OR 3112 EPDM)", 1, "D/V", (16, 8.2, 1.5, "flat"), "Copper seen in video 26:52."),
 51: ("E-clip DIN 6799-5", "Spring steel", 4, "D", (9, 5, 0.7, "flat"), "For shaft Ø6-8."),
 58: ("Basket spring", "Stainless wire Ø1", 1, "V", (52, 50, 1, "oring"), ""),
 62: None,
}
PIPES = {
 32: ("Steam wand", "Brass tube Ø8 x 1" + CHR, 1, "V/E", [(18, 0, D["STK_Z"] - 23), (18, 0, 212), (16, -22, 178), (14, -34, 136), (18, -38, 124)], 8, 1, 12,
      ("flared under union nut 33", "steam tip 34 brazed")),
 45: ("L-tube (boiler pick-up)", "Brass tube Ø8 x 1", 1, "V/E", [(D["PAD_X1"] - 1.5, 0, D["PORT_Z"]), (96, 0, D["PORT_Z"]), (86, 0, D["PORT_Z"] - 10), (86, 0, 140)], 8, 1, 10,
      ("pressed into pad 69 Ø8 H7 x 6", "open end, 45° cut")),
 16: ("Safety-valve drain tube", "Copper tube Ø5 x 0.5", 1, "V", [(D["SV_X"] + 9, D["SV_Y"] + 6, 270), (118, 26, 262), (124, 26, 236), (124, 26, 120), (128, 26, 62)], 5, 0.5, 8,
      ("brazed into cup 16", "ends over drip tray")),
}

def build(pdf, Sheet):
    def page(title, layout, cells):
        sh = Sheet(None, title, "see cells")
        boxes = grid(sh.ax, *layout)
        for (x, y, w, h), fn in zip(boxes, cells): fn(sh.ax, x, y, w, h)
        sh.save(pdf)
    def T(it):
        def f(ax, x, y, w, h):
            n, m, q, c, spec = TURNED[it]; turned(Cell(ax, x, y, w, h, it, n, m, q, c), spec)
        return f
    def R(it):
        def f(ax, x, y, w, h):
            n, m, q, c, (od, id_, t, k), note = RINGS[it]; ring(Cell(ax, x, y, w, h, it, n, m, q, c), od, id_, t, k, note)
        return f
    def PI(it):
        def f(ax, x, y, w, h):
            n, m, q, c, pts, od, wl, r, ends = PIPES[it]; pipe(Cell(ax, x, y, w, h, it, n, m, q, c), pts, od, wl, r, ends)
        return f
    def C(it, name, mat, qty, conf, fn):
        return lambda ax, x, y, w, h: fn(Cell(ax, x, y, w, h, it, name, mat, qty, conf))
    page("PART DRAWINGS 1 - BOILER SHELL, GROUP BODY", (1, 2), [C(1, "Boiler shell", "Brass tube CuZn37 Ø80 x 1.5" + CHR, 1, "D/E", shell_drawing),
                                                              C(35, "Group body", BR + CHR, 1, "D/V/E", group_body)])
    page("PART DRAWINGS 2 - BOILER CASTINGS & FIXINGS", (2, 3), [T(2), T(3), C(4, "Ring nut, 3 ears", BR, 1, "D/V", ringnut_drawing),
                                                              C(69, "Boiler boss / pad", BR + ", Ag-brazed to 1", 1, "V/E", pad_drawing), T(9), T(11)])
    page("PART DRAWINGS 3 - ELEMENT, BASE, GRID", (2, 2), [C(6, "Heating element 200+800 W 220 V", "Cu sheath, brass flange", 1, "D/V", element_drawing),
                                                        C(61, "Base shell", "Steel DC04 1.0, painted / powder RAL 6027", 1, "D/V/E", base_drawing),
                                                        C(62, "Drip grid", SS4 + " 0.8", 1, "V", grid_drawing), T(12)])
    page("PART DRAWINGS 4 - SIGHT GLASS ASSEMBLY", (2, 3), [C(19, "Sight-glass block", BRB + CHR, 2, "D/V/E", sgblock_drawing), T(17), T(18), T(20), T(21), T(24)])
    page("PART DRAWINGS 5 - STEAM VALVE & SAFETY VALVE", (2, 3), [C(25, "Steam-valve body", BRB + CHR, 1, "D/V/E", valvebody_drawing), T(26), T(27), T(30), T(13), T(16)])
    page("PART DRAWINGS 6 - PISTON, ROD, LEVER", (2, 3), [T(36), T(38), C(49, "Lever fork + rod", "Steel, chromed", 1, "V/E", lever_drawing), T(50), T(52), T(53)])
    page("PART DRAWINGS 7 - PORTAFILTER, NUTS, SMALL PARTS", (3, 4), [T(54), T(55), T(59), T(60), T(46), T(47), T(48), T(33), T(34), T(31), T(66), T(40)])
    page("PART DRAWINGS 8 - PIPES & BENT TUBES (bend tables)", (3, 1), [PI(32), PI(45), PI(16)])
    page("PART DRAWINGS 9 - SEALS, GASKETS, WASHERS, CLIPS", (3, 5), [R(5), R(7), R(10), R(22), R(23), R(28), R(29), R(37), R(39), R(41), R(42), R(44), R(51), R(58), T(43)])

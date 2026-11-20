"""Part drawings for the La Pavoni Professional v3.1 copper/brass. Every feature dimensioned."""
import math
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle
from partdraw import Cell, turned, ring, plate, pipe, hdim, vdim, leader, cl, pick_scale, scale_label, INK, DIMC, NOTE, HATCH_FC
from views import D, rounded_trap
import parts_sheets as PS

BR = "Brass CW617N (CuZn40Pb2)"; BRB = "Brass CW614N bar"; POL = ", polished + clear lacquer"; SS = "Stainless AISI 303"; SS4 = "Stainless AISI 304"
CU = "Copper Cu-DHP (CW024A)"
grid = PS.grid
COP_FC = "#f2c4a6"

# ================================================================== custom drawers
def shell_drawing(cell, which):
    """Items 1 / 85: lower and upper copper shells (Ø100 x 1.5), section + developed hole layout."""
    ax = cell.ax; OD = D["SH_D"]; t = 1.5
    if which == "lower":
        z0, z1 = 70, D["SEAM_Z"]; holes = [("H1", math.degrees(math.atan2(D["SG_Y"], D["SG_X"] - D["BX"])) % 360, D["SG_Z0"], 12.5, "sight glass lower Ø12.5")]
        notes = f"Bottom 6 into foot socket (Z70-76), Ag-braze. Top: joggled 4 into seam ring 84 at Z{D['SEAM_Z']}."
    else:
        z0, z1 = D["SEAM_Z"], D["SH_Z1"] + 8; sg_a = math.degrees(math.atan2(D["SG_Y"], D["SG_X"] - D["BX"])) % 360
        holes = [("H1", 0, D["PORT_Z"], 14, "group port Ø14 (boss 69 brazed over)"), ("H2", sg_a, D["SG_Z1"], 12.5, "sight glass upper Ø12.5")]
        notes = f"Top 8 inside dome 2 skirt (Z{D['SH_Z1']}-{D['SH_Z1'] + 8}), Ag-braze."
    L = z1 - z0
    s = pick_scale(L + 30, OD + 26, cell.w * 0.40, cell.h - 30); cell.set_scale(s)
    ox, oy = cell.x + 16, cell.y + cell.h / 2 - 4
    P = lambda z, r: (ox + (z - z0) * s, oy + r * s)
    for sg in (1, -1):
        ax.add_patch(Polygon([P(z0, sg * (OD / 2 - t)), P(z1, sg * (OD / 2 - t)), P(z1, sg * OD / 2), P(z0, sg * OD / 2)], closed=True, fc=COP_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    cl(ax, P(z0 - 3, 0), P(z1 + 3, 0))
    hdim(ax, P(z0, 0)[0], P(z1, 0)[0], P(z0, -OD / 2)[1], P(z1, -OD / 2)[1], P(z0, -OD / 2)[1] - 5, f"{L} (Z{z0}-Z{z1})")
    vdim(ax, P(z0, -OD / 2)[1], P(z0, OD / 2)[1], P(z0, 0)[0], P(z0, 0)[0], P(z0, 0)[0] - 5, f"Ø{OD} OD [D]")
    leader(ax, P((z0 + z1) / 2, OD / 2 - t / 2), (P((z0 + z1) / 2, 0)[0] + 4, P(z0, OD / 2)[1] + 6), f"wall {t} [E] -> ID {OD - 2 * t:g}")
    circ = math.pi * OD
    s2 = pick_scale(circ + 20, L + 24, cell.w * 0.55, cell.h - 26)
    dx, dy = cell.x + cell.w * 0.42, cell.y + 14
    Q = lambda a, z: (dx + ((a + 90) % 360) / 360 * circ * s2, dy + (z - z0) * s2)
    ax.add_patch(Polygon([(dx, dy), (dx + circ * s2, dy), (dx + circ * s2, dy + L * s2), (dx, dy + L * s2)], closed=True, fc="#fbe8dc", ec=INK, lw=0.6, zorder=3))
    for a_ in (0, 90, 180, 270): ax.text(*Q(a_, z0 - 4 / s2), f"{a_}°", fontsize=3.8, ha="center", color="#555")
    for k, (hid, a, z, d_, note) in enumerate(holes):
        c = Q(a, z); ax.add_patch(Circle(c, d_ / 2 * s2, fc="white", ec=INK, lw=0.5, zorder=4)); ax.text(c[0] + 2, c[1] + 2, hid, fontsize=4, color=DIMC, zorder=5)
        vdim(ax, dy, c[1], c[0], c[0], c[0] + 6, f"{z - z0:g}", side="right", size=4)
        hdim(ax, dx, c[0], dy + L * s2, c[1], dy + L * s2 + 5 + 4 * k, f"{((a + 90) % 360) / 360 * circ:.1f}", size=4)
    hdim(ax, dx, dx + circ * s2, dy, dy, dy - 6, f"{circ:.1f} = π x {OD}")
    ax.text(dx, dy + L * s2 + 14, f"DEVELOPED (seam at -90°, 0° = +X, CCW from above)  {scale_label(s2)}", fontsize=4.1)
    ty = cell.y + cell.h - 11
    for k, (hid, a, z, d_, note) in enumerate(holes):
        ax.text(cell.x + 3, ty - 3.8 * k, f"{hid}: {note} at {a:.1f}°, Z{z} ({z - z0:g} from shell end)", fontsize=4.1, va="top")
    ax.text(cell.x + 3, cell.y + 3, notes, fontsize=4.1, color=NOTE)

def group_body(cell):
    """Item 35: Millennium group body (bolts in Y), X-Z section + top view."""
    ax = cell.ax; gx = D["GX"]; z0 = D["BELL_Z0"]
    s = 1.0; cell.set_scale(s)
    ox, oy = cell.x + 80, cell.y + 20
    P = lambda x, z: (ox + x * s, oy + z * s)
    rb = D["BODY_D"] / 2; top = D["BODY_Z1"] - z0; sk = 12; g1 = sk + 5.5; scr = g1 + 1; bt = top - 8
    fl0, fl1 = D["PAD_X1"] - gx, D["FL_X1"] - gx; pz = D["PORT_Z"] - z0
    c0, c1 = D["COL_X0"] - gx, D["COL_X1"] - gx; ctop = D["YOKE_Z1"] - z0; fz = D["FZ"] - z0; fx = D["FX"] - gx
    for sg in (1, -1):
        prof = [(sg * 32.25, 0), (sg * 38, 0), (sg * 38, 22), (sg * rb, 34), (sg * rb, top), (sg * 5.25, top), (sg * 5.25, top - 2),
                (sg * 10, top - 2), (sg * 10, bt), (sg * 25.1, bt), (sg * 25.1, scr), (sg * 27, scr), (sg * 27, g1), (sg * 30, g1), (sg * 30, sk), (sg * 32.25, sk)]
        ax.add_patch(Polygon([P(*p) for p in prof], closed=True, fc=HATCH_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(fl0, pz - 13), P(fl1, pz - 13), P(fl1, pz - 11), P(-rb, pz - 11), P(-rb, pz + 11), P(fl1, pz + 11), P(fl1, pz + 13), P(fl0, pz + 13)],
                         closed=True, fc=HATCH_FC, hatch="////", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Rectangle(P(fl0, pz - 4), (-25.1 - fl0) * s, 8 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Polygon([P(c0, top - 4), P(c1, top - 4), P(c1, ctop), P(c0, ctop)], closed=True, fc="#eeeeee", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Circle(P(fx, fz), 5.05, fc="white", ec=INK, lw=0.5, zorder=4))
    cl(ax, P(0, -4), P(0, ctop + 4)); cl(ax, P(fl0 - 4, pz), P(-15, pz))
    xr = P(38, 0)[0] + 6
    for a, b, lab in ((0, sk, f"{sk} skirt"), (sk, g1, "5.5"), (g1, scr, "1"), (scr, bt, f"{bt - scr:.1f} sleeve bore"), (bt, top - 2, "6"), (top - 2, top, "2"), (top, ctop, f"{ctop - top:g}")):
        vdim(ax, P(0, a)[1], P(0, b)[1], P(38, a)[0], P(38, b)[0], xr, lab, side="right")
    vdim(ax, P(0, 0)[1], P(0, top)[1], xr, xr, xr + 10, f"{top} body", side="right")
    vdim(ax, P(0, 0)[1], P(0, 22)[1], P(-38, 0)[0], P(-38, 22)[0], P(-38, 0)[0] - 5, "22 bell")
    hdim(ax, P(-38, 0)[0], P(38, 0)[0], P(0, 0)[1], P(0, 0)[1], P(0, 0)[1] - 5, f"Ø{D['BELL_D']} bell [V]")
    hdim(ax, P(-32.25, 0)[0], P(32.25, 0)[0], P(0, 0)[1], P(0, 0)[1], P(0, 0)[1] - 10, "Ø64.5 skirt ID")
    hdim(ax, P(-25.1, 0)[0], P(25.1, 0)[0], P(0, scr + 14)[1], P(0, scr + 14)[1], P(0, scr + 14)[1], "Ø50.2 H8 sleeve bore")
    hdim(ax, P(-30, 0)[0], P(30, 0)[0], P(0, sk)[1], P(0, sk)[1], P(0, sk)[1] + 2.4, "Ø60 groove", size=4)
    hdim(ax, P(-rb, 0)[0], P(rb, 0)[0], P(0, top)[1], P(0, top)[1], P(0, top)[1] + 4, f"Ø{D['BODY_D']} body [E]")
    leader(ax, P(8, bt + 1), (P(8, 0)[0] + 18, P(0, top)[1] + 12), "Ø20 x 6 seal recess (C-clip groove Ø21 x 1.1), 2 lip, Ø10.5 rod hole")
    leader(ax, P(-28, pz), (P(fl0, 0)[0] - 5, P(0, pz + 8)[1]), "port Ø8 THRU to sleeve")
    vdim(ax, P(0, 0)[1], P(0, pz)[1], P(fl0, pz)[0], P(fl0, pz)[0], P(fl0, 0)[0] - 4, f"{pz:g} port C/L")
    hdim(ax, P(fl0, 0)[0], P(0, 0)[0], P(fl0, pz - 13)[1], P(0, 0)[1], P(0, pz - 32)[1], f"{-fl0:g}")
    vdim(ax, P(0, pz - 13)[1], P(0, pz + 13)[1], P(fl0, 0)[0], P(fl0, 0)[0], P(fl0, 0)[0] - 12, "26 flange")
    hdim(ax, P(c0, 0)[0], P(c1, 0)[0], P(0, ctop)[1], P(0, ctop)[1], P(0, ctop)[1] + 4, f"{c1 - c0} column")
    leader(ax, P(fx, fz), (P(c0, 0)[0] - 10, P(0, ctop + 6)[1]), f"fulcrum bore Ø10.1 H8 @ x{fx:g}, z{fz:g}")
    ax.text(cell.x + 3, cell.y + cell.h - 11, "Section X-Z. x from group axis (- = boiler side), z from bell face (= Z176). Flange 60 (Y) x 26 (Z) x 5 with\n"
            f"2 x Ø6.4 on {D['BOLT_CC']} c/c along Y (not in section plane). Bayonet: 2 ramps 45°, 3.5 deep, 1:12 rise in skirt.", fontsize=4.2, va="top", color=NOTE)
    tx, ty = cell.x + cell.w - 60, cell.y + cell.h * 0.48
    T = lambda x, y: (tx + x * 0.75, ty + y * 0.75)
    ax.add_patch(Circle(T(0, 0), 38 * 0.75, fc="#eeeeee", ec=INK, lw=0.5, zorder=3)); ax.add_patch(Circle(T(0, 0), rb * 0.75, fc="#e2e2e2", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Rectangle(T(c0, -8), (c1 - c0) * 0.75, 16 * 0.75, fc="#d8d8d8", ec=INK, lw=0.5, zorder=4))
    ax.add_patch(Rectangle(T(fl0, -30), (fl1 - fl0) * 0.75, 60 * 0.75, fc="#d8d8d8", ec=INK, lw=0.5, zorder=4))
    for yy in (-22, 22): ax.add_patch(Circle(T(fl0 + 2.5, yy), 3.2 * 0.75, fc="white", ec=INK, lw=0.4, zorder=5))
    ax.add_patch(Circle(T(0, 0), 5.25 * 0.75, fc="white", ec=INK, lw=0.5, zorder=5))
    ax.text(tx, ty - 38 * 0.75 - 4, "TOP VIEW (1:1.33)", fontsize=4.4, ha="center")
    vdim(ax, T(0, -22)[1], T(0, 22)[1], T(fl0, -22)[0], T(fl0, 22)[0], T(fl0, 0)[0] - 3, f"{D['BOLT_CC']} c/c", size=4)
    vdim(ax, T(0, -30)[1], T(0, 30)[1], T(fl1, -30)[0], T(fl1, 30)[0], T(fl1, 0)[0] + 3, "60", size=4, side="right")

def pad_drawing(cell):
    """Item 69: boiler boss / pad - ears horizontal (Y)."""
    holes = [("A", 8, 13, 5, "Ø5 ↧7.5, M6 ↧6"), ("B", 52, 13, 5, "Ø5 ↧7.5, M6 ↧6"), ("C", 30, 13, 6, "Ø6 ↧4; Ø8 H7 ↧4 from back"),
             ("D", 30, 13, 16, "O-ring groove Ø11/Ø16.2 x 2.0")]
    P, s = plate(cell, [(0, 0), (60, 0), (60, 26), (0, 26)], holes, 10, "face Ra 1.6 µm, flatness 0.02. Back R50 concave on Ø100 shell: 8 thick on C/L, 15 at ends.")
    ax = cell.ax
    hdim(ax, P(0, 0)[0], P(8, 0)[0], P(0, 26)[1], P(8, 26)[1], P(0, 26)[1] + 4, "8", size=4)
    hdim(ax, P(8, 0)[0], P(52, 0)[0], P(8, 26)[1], P(52, 26)[1], P(0, 26)[1] + 4, f"{D['BOLT_CC']} c/c", size=4)
    vdim(ax, P(0, 0)[1], P(0, 13)[1], P(60, 0)[0], P(60, 13)[0], P(60, 0)[0] + 4, "13", side="right", size=4)

def element_drawing(cell):
    """Item 6: SS heating element 1000 W, flange Ø84."""
    ax = cell.ax
    pts = PS._eared(42, 52, 7.5)
    holes = [(f"E{e + 1}", round(52 * math.cos(math.radians(90 + 120 * e)), 2), round(52 * math.sin(math.radians(90 + 120 * e)), 2), 5.5, "Ø5.5 THRU (M5x12 [D])") for e in range(3)]
    holes += [("T1", round(17 * math.cos(math.radians(45)), 2), round(17 * math.sin(math.radians(45)), 2), 6, "terminal L, M4 + 6.3 tab"),
              ("T2", round(17 * math.cos(math.radians(225)), 2), round(17 * math.sin(math.radians(225)), 2), 6, "terminal N, M4 + 6.3 tab"),
              ("PS", 20, 10, 8, "pressurestat port G1/8, boss Ø14"), ("TH", -20, -15, 16, "thermostat seat Ø16 flat, 2x M3"), ("PE", 0, -30, 4.2, "M4 earth stud")]
    plate(cell, pts, holes, 6, "AISI 316 flange + sheath, O-ring groove Ø74 x 3.6 on top face.")
    ax.text(cell.x + 3, cell.y + 9, "1000 W at 230 V (R = 52.9 Ω) [D]; 120 V version 14.4 Ω. Sheath Ø8, 6 turns on Ø56 coil C/L, pitch 13, stack 80.\n"
            "Seals on the spigot face with O-ring 7 (3.53 x 73.98, La Pavoni 465225) [D].", fontsize=4.1, va="bottom", color=NOTE)

def base_drawing(cell):
    outline = rounded_trap(D["W_REAR"], D["W_FRONT"], D["L"], D["BASE_R"], n=12)
    holes = [("B", D["BX"], 0, 82, "Ø82 boiler hole (top face)"), ("G", D["TRAY_X0"] + 68, 0, 6, "Ø6 sub-base screw boss (under tray)"),
             ("S", D["SW_X"], -100, 0, f"switch cut-out 22 x 30 in LEFT wall, centre Z{D['SW_Z']}"),
             ("L1", 285, D["BADGE_Y"] - 6, 2.2, "badge pin Ø2.2 (FRONT wall Z38)"), ("L2", 285, D["BADGE_Y"] + 6, 2.2, "badge pin Ø2.2 (FRONT wall Z38)"),
             ("C", 0, 45, 16.5, "Ø16.5 gland hole (REAR wall Z30)"), ("R", D["TRAY_X0"], 0, 0, f"tray opening {D['TRAY_L']} x {D['TRAY_W']}, R24")]
    P, s = plate(cell, outline, holes, 0.8, "Brass CuZn37 0.8 deep drawn, polished + lacquer; walls drafted 7 in over 55 high [V].")
    ax = cell.ax
    tr = rounded_trap(D["TRAY_W"], D["TRAY_W"] - 6, D["TRAY_L"], 24, x0=D["TRAY_X0"])
    ax.add_patch(Polygon([P(*p) for p in tr], closed=True, fc="none", ec=INK, lw=0.5, ls=(0, (3, 1.5)), zorder=5))
    hdim(ax, P(0, 0)[0], P(D["BX"], 0)[0], P(0, 0)[1], P(D["BX"], 0)[1], P(0, 106)[1], f"{D['BX']}", size=4)
    hdim(ax, P(D["BX"], 0)[0], P(D["TRAY_X0"], 0)[0], P(D["BX"], 0)[1], P(D["TRAY_X0"], 0)[1], P(0, 106)[1], f"{D['TRAY_X0'] - D['BX']}", size=4)
    hdim(ax, P(D["TRAY_X0"], 0)[0], P(D["TRAY_X0"] + D["TRAY_L"], 0)[0], P(0, 0)[1], P(0, 0)[1], P(0, 106)[1], f"{D['TRAY_L']}", size=4)
    vdim(ax, P(0, -D["W_FRONT"] / 2)[1], P(0, D["W_FRONT"] / 2)[1], P(D["L"], 0)[0], P(D["L"], 0)[0], P(D["L"], 0)[0] + 5, f"{D['W_FRONT']} front", side="right", size=4)

def subbase_drawing(cell):
    outline = rounded_trap(D["W_REAR"] + 2, D["W_FRONT"] + 2, D["L"] + 2, D["BASE_R"] + 1, n=12, x0=-1)
    holes = [("F1", 30, -70, 6, "foot 80 snap hole Ø6"), ("F2", 30, 70, 6, "foot 80 snap hole Ø6"), ("F3", 255, -62, 6, "foot 80 snap hole Ø6"),
             ("F4", 255, 62, 6, "foot 80 snap hole Ø6"), ("S", D["TRAY_X0"] + 68, 0, 4.5, "Ø4.5 csk for screw 81 (M4x20)"),
             ("V1", 100, 30, 5, "vent Ø5 (x12 pattern, pitch 15)"), ("PS", D["BX"] + 85, 46, 4, "pressurestat bracket M4 (x2)")]
    plate(cell, outline, holes, 2.5, "Black ABS, 2.5 wall, 6 high rim, central post Ø12 x 50 with M4 insert to base boss.")

def grid_drawing(cell):
    tg = [(x - D["TRAY_X0"] - 4, y) for x, y in rounded_trap(D["TRAY_W"] - 8, D["TRAY_W"] - 14, D["TRAY_L"] - 8, 20, x0=D["TRAY_X0"] + 4)]
    P, s = plate(cell, tg, [("P", 10, -45, 7.2, "10 x 8 holes Ø7.2, pitch 12.2 x 12.8, first X10 Y-45; 4 centre holes omitted; centre Ø5")], 0.8,
                 "Brass CuZn37 0.8, polished + lacquer; 76 holes Ø7.2 + Ø5 centre.")
    ax = cell.ax
    for a in range(10):
        for b in range(8):
            if abs(a - 4.5) < 1 and abs(b - 3.5) < 1: continue
            ax.add_patch(Circle(P(10 + a * 12.2, -45 + b * 12.8), 3.6 * s, fc="white", ec=INK, lw=0.3, zorder=4))
    ax.add_patch(Circle(P(64.9, 0), 2.5 * s, fc="white", ec=INK, lw=0.3, zorder=4))
    hdim(ax, P(10, 0)[0], P(22.2, 0)[0], P(10, -45)[1], P(22.2, -45)[1], P(0, -62)[1], "12.2", size=4)

def gauge_drawing(cell):
    """Item 71: pressure gauge (bought-in) - envelope."""
    ax = cell.ax; s = 2.0; cell.set_scale(s)
    cx, cy = cell.x + cell.w * 0.30, cell.y + cell.h * 0.52
    ax.add_patch(Circle((cx, cy), 22 * s, fc="#ecc865", ec=INK, lw=0.6, zorder=3)); ax.add_patch(Circle((cx, cy), 19 * s, fc="#fbfbf3", ec=INK, lw=0.5, zorder=4))
    for k in range(6):
        a = math.radians(225 - k * 54); ax.plot([cx + 15 * s * math.cos(a), cx + 18 * s * math.cos(a)], [cy + 15 * s * math.sin(a), cy + 18 * s * math.sin(a)], lw=0.5, color=INK, zorder=5)
        ax.text(cx + 12 * s * math.cos(a), cy + 12 * s * math.sin(a), f"{k * 0.5:g}", fontsize=4.2, ha="center", va="center", zorder=5)
    ax.plot([cx, cx + 14 * s * math.cos(math.radians(90))], [cy, cy + 14 * s * math.sin(math.radians(90))], lw=0.8, color="#c00", zorder=6)
    hdim(ax, cx - 22 * s, cx + 22 * s, cy, cy, cy + 22 * s + 5, "Ø44 bezel")
    hdim(ax, cx - 19 * s, cx + 19 * s, cy, cy, cy - 22 * s - 5, "Ø40 dial [D]")
    sx = cell.x + cell.w * 0.72
    ax.add_patch(Rectangle((sx - 13 * s, cy - 22 * s), 26 * s, 44 * s, fc="#ecc865", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((sx - 3 * s, cy - 22 * s - 14 * s), 6 * s, 14 * s, fc="#ecc865", ec=INK, lw=0.6, zorder=3))
    hdim(ax, sx - 13 * s, sx + 13 * s, cy + 22 * s, cy + 22 * s, cy + 22 * s + 5, "26 deep")
    vdim(ax, cy - 36 * s, cy - 22 * s, sx + 3 * s, sx + 3 * s, sx + 3 * s + 5, "14 stem", side="right")
    leader(ax, (sx, cy - 30 * s), (sx + 22, cy - 34 * s), "G1/8 male (ISO 228, Ø9.73) [D]")
    ax.text(cell.x + 3, cell.y + 3, "Range 0-250 kPa (dial 0-2.5 bar), class 2.5, brass case, glass lens [D, La Pavoni 453040 type].", fontsize=4.1, color=NOTE)

# ================================================================== catalogue
TURNED = dict(PS.TURNED)
TURNED.update({
 2: ("Dome (shoulder)", CU + ", spun 1.5, polished + lacquer", 1, "V/E", dict(
     segs=[dict(L=8, D=103), dict(L=20, D=103, D2=48)], bl=[(8, 100.2), (20, 97, )], notes=["x0 = Z254. Skirt Ø100.2 x 8 over upper shell.", "Bosses brazed: steam riser Ø18 @ X45 Y-12, SV Ø19 @ X108 Y18.", "Neck ring 86 brazed into Ø46 top opening."])),
 86: ("Neck ring", BR + POL, 1, "V/E", dict(segs=[dict(L=10, D=46)], bl=[(10, 40, "M40x1.5-6H")], notes=["Ag-brazed into dome; cap insert 9 screws in."])),
 3: ("Foot casting (flare + spigot)", BR + POL + " (flare)", 1, "D/V/E", dict(
     segs=[dict(L=22, D=80, t="M80x1.5"), dict(L=5, D=112), dict(L=6, D=112, D2=102)], bl=[(33, 68)], br=[(6, 100.2)],
     notes=["Spigot M80x1.5-6g coarse (since 1996) [D] - same as Europiccola.", "Socket Ø100.2 x 6 for lower shell.", "Spigot end face = element O-ring face, Ra 3.2 µm."])),
 9: ("Cap insert", BRB, 1, "V/E", dict(segs=[dict(L=16, D=40, t="M40x1.5"), dict(L=3, D=46), dict(L=6, D=20)], bl=[(25, 6.8)], br=[(14, 8, "M8-6H")])),
 12: ("Cap screw M8x40", "Stainless A2-70, ISO 4762", 1, "V/E", dict(segs=[dict(L=8, D=13), dict(L=40, D=8, t="M8")], bl=[(5, 6.9)])),
 13: ("Safety-valve body (anti-vacuum)", BRB + POL, 1, "D/E", dict(segs=[dict(L=8, D=12, t="M12x1.5"), dict(L=6, hex=14), dict(L=8, D=10, t="M10x1")],
     bl=[(8, 4)], br=[(14, 6.5)], notes=["Poppet seat 90° at Ø4/Ø6.5. Opens ~150 kPa,", "anti-vacuum lifts below 0 kPa gauge [D type]."])),
 16: ("Safety-valve cup", BRB + POL, 1, "V/E", dict(segs=[dict(L=22, D=22)], bl=[(8, 9, "M10x1-6H"), (12, 18)], xholes=[(14, 5, "exhaust-tube socket")])),
 17: ("Sight-glass tube", "Borosilicate glass 3.3", 1, "V/E", dict(segs=[dict(L=135, D=12)], bl=[(135, 9)], fc="#cfe8f5", hatch="",
     notes=["Blocks 137 c/c [V]. Ends fire-polished."])),
 18: ("Glass guard (clear)", "Polycarbonate tube, clear", 1, "V/E", dict(segs=[dict(L=109, D=18)], bl=[(109, 16)], notes=["Clear protector between gland nuts [D type]."])),
 72: ("Gauge adapter", BRB + POL, 1, "D/E", dict(segs=[dict(L=8, D=10, t="M10x1"), dict(L=6, hex=14), dict(L=12, D=12)], bl=[(14, 3)], br=[(12, 8.4, "G1/8-F (ISO 228)")],
     notes=["'Special nut adapter for gauge' [D]. Replaces upper plug."])),
 76: ("Group sleeve (Millennium)", "PTFE (Teflon) 25% glass [D: Teflon sleeve]", 1, "D/E", dict(
     segs=[dict(L=4, D=50, tol="h8"), dict(L=3.6, D=44.6), dict(L=51.9, D=50, tol="h8")], bl=[(59.5, 44, "Ø44 H8 bore")],
     xholes=[(23.5, 6, "2 inlet holes at ±90°")], notes=["Groove for O-ring 77 at bottom.", "Fits Ø50.2 group bore; top bears on C-clip."])),
 36: ("Piston (brass, v3.1)", BRB, 1, "D/E", dict(segs=[dict(L=4, D=43.9, tol="f7"), dict(L=5.6, D=36), dict(L=7.4, D=43.9), dict(L=5.6, D=36), dict(L=7.4, D=43.9)],
     br=[(16, 6.8, "M8-6H")], notes=["Brass piston from 2007 (v3.1) [D].", "Stroke 29.5 -> 45 ml."])),
 54: ("Portafilter body", BR + POL, 1, "D/V", dict(segs=[dict(L=4, D=26), dict(L=24.8, D=58, D2=62)], bl=[(4, 10, "M10x1-6H")], br=[(24.8, 54)],
     notes=["OD 60 rim [D, +2 mm vs 1998]; 2 lugs 8 x 5 x 3.5.", "Baskets 60 OD rim / 51 nominal [D]."])),
 87: ("Steam riser", BRB + POL, 1, "V/E", dict(segs=[dict(L=8, D=12, t="M12x1"), dict(L=24, D=14), dict(L=6, D=10, t="M10x1")], bl=[(38, 4)],
     notes=["Screws into dome boss; top into valve body 25."])),
 89: ("Auto-frother (cappuccinatore)", "Brass" + POL + " + silicone O-ring", 1, "D/E", dict(segs=[dict(L=20, D=18), dict(L=12, D=14, D2=8)], bl=[(20, 8.3)],
     xholes=[(10, 1.5, "air inlet")], notes=["Slides on wand, O-ring 47 inside [D]."])),
 46: ("Group bolt M6x10", "Brass" + POL + " (chromed on chrome models) [D: 'bolts for group']", 2, "D/V", dict(segs=[dict(L=4, hex=10), dict(L=10, D=6, t="M6")])),
 59: ("Handle stud M8x80", "Stainless A2", 1, "V/E", dict(segs=[dict(L=80, D=8, t="M8")])),
 60: ("Portafilter handle", "Rosewood, oiled (PRG) / black PP", 1, "V", dict(segs=[dict(L=100, D=24, D2=26)], bl=[(60, 6.8, "M8 insert")], fc="#c9956a", hatch="----")),
 53: ("Lever handle", "Rosewood, oiled", 1, "V", dict(segs=[dict(L=101, D=22, D2=24)], bl=[(25, 6.8, "M8 insert")], fc="#c9956a", hatch="----")),
 11: ("Cap knob, 6-lobe", "Rosewood, oiled", 1, "V", dict(segs=[dict(L=40, D=28, D2=38), dict(L=21, D=58, lobes=6)], bl=[(6, 20.5), (47, 8.5)], br=[(8, 13.5)], fc="#c9956a", hatch="----")),
 30: ("Steam knob, 6-lobe", "Rosewood, oiled", 1, "V", dict(segs=[dict(L=22, D=37, D2=31, lobes=6)], bl=[(18, 6)], xholes=[(9, 2.5, "pin, through")], fc="#c9956a", hatch="----")),
})
RINGS = dict(PS.RINGS)
RINGS.update({
 5: ("Boiler / base gaskets", "Fibre AFM34 (upper 112x82x2 [E]; lower 93x80x2 [D])", 2, "D/E", (112, 82, 2, "flat"), "Upper 'Professional tank to base gasket' P-4P [D]; lower = Europiccola 362019."),
 7: ("Element O-ring", "Silicone VMQ 70 (food grade, 200 °C)", 1, "D", (81.04, 73.98, 3.53, "oring"), "3.53 x 73.98, La Pavoni 465225 (SS element) [D]."),
 10: ("Cap gasket", "Silicone VMQ 60 ShA", 1, "E", (46, 40.5, 2, "flat"), "'O-ring for boiler's knob' P-2 [D]."),
 42: ("Group gasket (quad)", "Silicone VMQ (orange/black)", 1, "D", (60, 50, 5.5, "flat"), "Post-millennium 60 x 50 x 5.5 (Pavoni 361028) [D]."),
 44: ("Group-to-boiler O-ring", "EPDM 70 / silicone", 1, "D", (16.01, 10.77, 2.62, "oring"), "OR 3112 (10.77 x 2.62) [D]."),
 77: ("Sleeve O-ring", "Viton FKM 75", 1, "D/E", (51.26, 44.2, 3.53, "oring"), "Cross-section 3.53 [D]; ID 44.2 [E]."),
 43: None,
 47: ("Frother O-ring", "Silicone VMQ", 1, "D/E", (12, 8, 2, "oring"), "Auto frother o'ring (item 47 on La Pavoni list) [D]."),
})
RINGS = {k: v for k, v in RINGS.items() if v}
PIPES = {
 32: ("Steam wand", "Brass tube Ø8 x 1" + POL, 1, "V/E", [(150, 24, D["STK_Z"] - 6), (156, 26, D["STK_Z"] - 14), (196, 34, 236)], 8, 1, 14, ("swivel 33 (union)", "steam tip 34 brazed")),
 88: ("Steam pipe (valve -> swivel)", "Brass tube Ø8 x 1" + POL, 1, "V/E", [(D["STK_X"], D["STK_Y1"], D["STK_Z"]), (D["STK_X"] + 8, D["STK_Y1"] + 4, D["STK_Z"]), (150, 24, D["STK_Z"])], 8, 1, 12,
      ("brazed into valve body 25", "brazed into swivel 33")),
 45: ("Pick-up tube", "Brass tube Ø8 x 1", 1, "V/E", [(D["PAD_X1"] - 1.5, 0, D["PORT_Z"]), (110, 0, D["PORT_Z"]), (100, 0, D["PORT_Z"] - 10), (100, 0, 140)], 8, 1, 10,
      ("pressed into boss 69 Ø8 H7 x 4", "open, 45° cut")),
 16: ("Safety-valve exhaust tube", "Copper tube Ø5 x 0.5", 1, "V/E", [(D["SV_X"] + 9, D["SV_Y"] + 6, 276), (136, 34, 266), (140, 36, 240), (140, 36, 120), (146, 36, 66)], 5, 0.5, 8,
      ("brazed into cup 16", "into drip tray")),
 74: ("Pressurestat pipe", "Copper tube Ø4 x 0.7 + G1/8 & G1/4 nuts", 1, "D/V", [(D["BX"] + 20, 10, 30), (D["BX"] + 30, 14, 26), (D["BX"] + 60, 20, 28), (D["BX"] + 85, 24, 29)], 4, 0.7, 10,
      ("G1/8 nut on element port [D]", "G1/4 nut on pressurestat [D]")),
}

def build(pdf, Sheet):
    def page(title, layout, cells):
        sh = Sheet(None, title, "see cells")
        for (x, y, w, h), fn in zip(grid(sh.ax, *layout), cells): fn(sh.ax, x, y, w, h)
        sh.save(pdf)
    T = lambda it: (lambda ax, x, y, w, h: turned(Cell(ax, x, y, w, h, it, *TURNED[it][:4]), TURNED[it][4]))
    R = lambda it: (lambda ax, x, y, w, h: ring(Cell(ax, x, y, w, h, it, *RINGS[it][:4]), *RINGS[it][4], RINGS[it][5]))
    PI = lambda it: (lambda ax, x, y, w, h: pipe(Cell(ax, x, y, w, h, it, *PIPES[it][:4]), *PIPES[it][4:]))
    C = lambda it, name, mat, qty, conf, fn: (lambda ax, x, y, w, h: fn(Cell(ax, x, y, w, h, it, name, mat, qty, conf)))
    page("PART DRAWINGS 1 - COPPER SHELLS", (1, 2), [C(1, "Lower shell", CU + " tube Ø100 x 1.5, polished + lacquer", 1, "D/E", lambda c: shell_drawing(c, "lower")),
                                                      C(85, "Upper shell", CU + " tube Ø100 x 1.5, polished + lacquer", 1, "D/E", lambda c: shell_drawing(c, "upper"))])
    page("PART DRAWINGS 2 - GROUP BODY (MILLENNIUM)", (1, 1), [C(35, "Group body", BR + POL, 1, "D/V/E", group_body)])
    page("PART DRAWINGS 3 - BOILER CASTINGS & FIXINGS", (2, 3), [T(2), T(3), C(4, "Fixing ring nut, 3 ears", BR, 1, "D/V", lambda c: ringnut_drawing(c)),
                                                              C(69, "Boiler boss / pad", BR + ", Ag-brazed to 85", 1, "V/E", pad_drawing), T(86), T(9)])
    page("PART DRAWINGS 4 - ELEMENT, BASE, SUB-BASE, GRID", (2, 3), [C(6, "Heating element 1000 W", "AISI 316 sheath + flange", 1, "D/V", element_drawing),
                                                                   C(61, "Base shell", "Brass 0.8 deep drawn" + POL, 1, "D/V/E", base_drawing),
                                                                   C(79, "Sub-base", "ABS black", 1, "D/E", subbase_drawing), C(62, "Drip grid", "Brass 0.8" + POL, 1, "V", grid_drawing),
                                                                   T(11), T(12)])
    page("PART DRAWINGS 5 - SIGHT GLASS & GAUGE", (2, 3), [C(19, "Sight-glass block", BRB + POL, 2, "D/V/E", PS.sgblock_drawing), T(17), T(18),
                                                       C(71, "Pressure gauge Ø40, 0-2.5 bar", "Bought-in, brass case", 1, "D", gauge_drawing), T(72), T(21)])
    page("PART DRAWINGS 6 - STEAM VALVE, SAFETY VALVE, FROTHER", (2, 4), [C(25, "Steam-valve body", BRB + POL, 1, "D/V/E", PS.valvebody_drawing), T(26), T(27), T(30),
                                                                        T(87), T(13), T(16), T(89)])
    page("PART DRAWINGS 7 - PISTON, SLEEVE, ROD, LEVER", (2, 3), [T(36), T(76), T(38), C(49, "Lever fork + rod", "Brass" + POL, 1, "V/E", PS.lever_drawing), T(50), T(52)])
    page("PART DRAWINGS 8 - PORTAFILTER, HANDLES, NUTS", (3, 4), [T(54), T(55), T(59), T(60), T(53), T(46), T(47), T(48), T(33), T(34), T(31), T(66)])
    page("PART DRAWINGS 9 - PIPES & TUBES (bend tables)", (3, 2), [PI(32), PI(88), PI(45), PI(16), PI(74), T(20)])
    page("PART DRAWINGS 10 - SEALS, GASKETS, WASHERS, CLIPS", (3, 5), [R(5), R(7), R(10), R(22), R(23), R(28), R(29), R(37), R(39), R(41), R(42), R(44), R(77), R(51), R(47)])

def ringnut_drawing(cell):
    pts = PS._eared(49, 52, 8)
    holes = [(f"E{e + 1}", round(52 * math.cos(math.radians(90 + 120 * e)), 2), round(52 * math.sin(math.radians(90 + 120 * e)), 2), 4.2, "M5-6H THRU (element screws M5x12 [D])") for e in range(3)]
    holes.append(("T", 0, 0, 80, "M80x1.5-6H THRU (coarse, since 1996) [D]"))
    P, s = plate(cell, pts, holes, 12, "'Flange brass coarse thread' P-6 [D]. 3 ears R8 on PCD 104 @ 90/210/330°.")
    cell.ax.add_patch(Circle(P(0, 0), 52 * s, fc="none", ec=DIMC, lw=0.3, ls=(0, (6, 2, 1, 2)), zorder=5))

TURNED.update({
 33: ("Steam swivel", BRB + POL, 1, "V/E", dict(segs=[dict(L=12, hex=14)], bl=[(12, 8.2)], xholes=[(6, 8, "side port for steam pipe 88")],
      notes=["Wand 32 brazed into bottom; O-ring seals swivel on pipe stub."])),
 38: ("Piston rod", "Steel, hard chrome 20 µm (or AISI 303)", 1, "V/E", dict(segs=[dict(L=14, D=8, t="M8"), dict(L=41, D=10, tol="f7"), dict(L=12, D=10),
      dict(L=17.5, D=10), dict(L=14, D=8, t="M8")], xholes=[(60.9, 6.1, "rod pin, H8")], notes=["Ø10 f7 Ra 0.2 through rod seal.", "Top M8: check nut 47 + acorn 48."])),
})

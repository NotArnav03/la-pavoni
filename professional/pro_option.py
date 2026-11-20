"""OPTION: piston-shaft group pressure-gauge kit (Coffee Sensor type / La Pavoni 5530014 gauge).
Second gauge on top of the lever, reads brew pressure under the piston through a hollow piston + hollow rod.
Items 91-97. All dimensions mm (SI). Kit parts are not factory-drawn: geometry [V] from owner photo, rest [E]."""
import math
import numpy as np
from matplotlib.patches import Circle, Rectangle, Polygon
from partdraw import Cell, hdim, vdim, leader, cl, pick_scale, scale_label, INK, DIMC, NOTE, HATCH_FC
import simple_parts as SP
import iso as ISO
from pro_parts import BRB, POL, grid

CHR = "#d9dde2"; BRASS = "#e6c98f"

TURNED = {
 92: ("Gauge adapter (kit)", BRB + ", nickel/chrome", 1, "E", dict(segs=[dict(L=6, D=8, t="M8x1"), dict(L=8, hex=14)], bl=[(6, 2)], br=[(9, 8.4, "G1/8-F (ISO 228)")],
      notes=["G1/8 thread sealed with PTFE tape or Loctite 243."])),
 93: ("Gauge extension (kit)", "Brass, chrome plated", 1, "V/E", dict(segs=[dict(L=38, D=14)], bl=[(12, 9, "M10x1-6H")], br=[(10, 6.9, "M8x1-6H")],
      notes=["Ø2.5 drilled through between the threads.", "2 spanner flats 12 AF, 6 long, at the top [E]."])),
 94: ("Hollow piston rod (kit)", "Stainless AISI 303, Ra 0.2 µm on Ø10", 1, "E", dict(
      segs=[dict(L=14, D=8, t="M8"), dict(L=41, D=10, tol="f7"), dict(L=12, D=10), dict(L=13.5, D=10), dict(L=18, D=10, t="M10x1")],
      bl=[(98.5, 3)], xholes=[(60.9, 4.2, "2 side holes M5, 3.5 deep, opposite")],
      notes=["Replaces rod 38. Ø3 gun-drilled full length.", "Side holes take lever screws 97 (no rod pin)."])),
 95: ("Hollow piston (kit)", BRB, 1, "D/E", dict(segs=[dict(L=4, D=43.9, tol="f7"), dict(L=5.6, D=36), dict(L=7.4, D=43.9), dict(L=5.6, D=36), dict(L=7.4, D=43.9)],
      bl=[(14, 3)], br=[(16, 6.8, "M8-6H")], notes=["As piston 36 + Ø3 hole through the crown", "so brew pressure reaches the rod bore."])),
 96: ("Stop nut M10x1", "Stainless A2, ISO 8675 thin nut", 1, "E", dict(segs=[dict(L=5, hex=16)], bl=[(5, 9, "M10x1-6H")],
      notes=["Lever-down stop: sits on the rod under the extension."])),
 97: ("Lever screw M5x10 + washer", "Stainless A2-70, ISO 4017 + ISO 7089", 2, "E", dict(segs=[dict(L=3.5, hex=8), dict(L=10, D=5, t="M5")],
      notes=["Clamp kit-lever cheeks to the rod; Loctite 243."])),
}

def gauge16_drawing(sub):
    """Item 91: group pressure gauge 0-16 bar (bought-in) - envelope, same body as gauge 71."""
    ax = sub.ax; s = min(2.0, (sub.h - 30) / 80, (sub.w - 30) / 95); s = max(v for v in (2, 1.5, 1.25, 1, 0.8, 0.5) if v <= s) if s >= 0.5 else s; sub.set_scale(s)
    cx, cy = sub.x + sub.w * 0.30, sub.y + sub.h * 0.55
    ax.add_patch(Circle((cx, cy), 22 * s, fc="#cfd3d8", ec=INK, lw=0.6, zorder=3)); ax.add_patch(Circle((cx, cy), 19 * s, fc="#fbfbf3", ec=INK, lw=0.5, zorder=4))
    for k in range(5):
        a = math.radians(225 - k * 67.5)
        ax.plot([cx + 15 * s * math.cos(a), cx + 18 * s * math.cos(a)], [cy + 15 * s * math.sin(a), cy + 18 * s * math.sin(a)], lw=0.5, color=INK, zorder=5)
        ax.text(cx + 12 * s * math.cos(a), cy + 12 * s * math.sin(a), f"{k * 4}", fontsize=4.2, ha="center", va="center", zorder=5)
    a = math.radians(225 - 9 / 16 * 270)
    ax.plot([cx, cx + 14 * s * math.cos(a)], [cy, cy + 14 * s * math.sin(a)], lw=0.8, color="#c00", zorder=6)
    ax.text(cx, cy - 8 * s, "bar", fontsize=3.8, ha="center", zorder=5)
    SP.tag(ax, cx - 26 * s, cy + 18 * s, "A"); SP.tag(ax, cx + 26 * s, cy + 18 * s, "B")
    sx = cx + 22 * s + 30 * s
    ax.add_patch(Rectangle((sx - 13 * s, cy - 22 * s), 26 * s, 44 * s, fc="#cfd3d8", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((sx - 6 * s, cy - 22 * s - 6 * s), 12 * s, 6 * s, fc=BRASS, ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Rectangle((sx - 4.9 * s, cy - 28 * s - 8 * s), 9.8 * s, 8 * s, fc=BRASS, ec=INK, lw=0.6, zorder=3, hatch="////"))
    SP.tag(ax, sx + 16 * s, cy, "C"); SP.tag(ax, sx + 9 * s, cy - 32 * s, "D")
    vdim(ax, cy - 36 * s, cy - 22 * s, sx + 5 * s, sx + 5 * s, sx + 12 * s, "14", side="right")
    hdim(ax, sx - 13 * s, sx + 13 * s, cy + 22 * s, cy + 22 * s, cy + 22 * s + 5, "26")

KEYS91 = [("A", "Dial Ø40 [V]: same size as boiler gauge 71"), ("B", "Case / bezel Ø44, chrome"), ("C", "Case depth 26"),
          ("D", "Stem G1/8 male (Ø9.73), 14 long, bottom entry"), ("", "Range 0-1600 kPa (dial 0-16 bar) [V photo]"),
          ("", "EN 837-1, accuracy class 1.6 [V photo dial]"), ("", "= ±26 kPa; brew pressure 600-900 kPa"), ("", "Type: La Pavoni 5530014 / Coffee Sensor [D]")]

# ------------------------------------------------------------------ assembly section through the kit
# Z = 0 at piston bottom face (water side); stack along the rod axis.
STACK = dict(PISTON=(0, 30), ROD=(16, 114.5), PIN=76.9, NUT=(96.5, 101.5), EXT=(102.5, 140.5), ADP=(134.5, 148.5), GAUGE_C=175.5, GAUGE_TOP=197.5)

def assembly_drawing(sub):
    ax = sub.ax; H = 200; s = pick_scale(110, H + 10, sub.w - 60, sub.h - 14); sub.set_scale(s)
    ox = sub.x + sub.w * 0.40; oy = sub.y + 7
    P = lambda r, z: (ox + r * s, oy + z * s)
    def rect(r0, r1, z0, z1, fc, hatch="////", lw=0.5):
        ax.add_patch(Rectangle(P(r0, z0), (r1 - r0) * s, (z1 - z0) * s, fc=fc, ec=INK, lw=lw, hatch=hatch, zorder=4))
    def both(r_in, r_out, z0, z1, fc, hatch="////"):
        rect(-r_out, -r_in, z0, z1, fc, hatch); rect(r_in, r_out, z0, z1, fc, hatch)
    # cylinder wall (sleeve 76) for reference, thin phantom
    for sg in (-1, 1):
        ax.plot([P(sg * 22, -2)[0]] * 2, [P(0, -2)[1], P(0, 62)[1]], lw=0.4, color="#888", ls=(0, (4, 2)), zorder=2)
    ax.text(*P(-23, 66), "sleeve 76 bore Ø44 ", ha="right", fontsize=3.6, color="#777", va="top")
    # piston 95 (grooves shown as steps)
    prof = [(0, 4, 21.95), (4, 9.6, 18), (9.6, 17, 21.95), (17, 22.6, 18), (22.6, 30, 21.95)]
    for z0, z1, r in prof: both(1.5, r, z0, z1, BRASS)
    for z0, z1, r in prof:
        if r == 18: both(18, 21.95, z0, z1, "#333", hatch="")          # lip seals 37
    # rod 94 (bore Ø3) - bottom M8 inside the piston
    both(1.5, 4, 16, 30, CHR); both(1.5, 5, 30, 96.5, CHR); both(1.5, 5, 96.5, 114.5, CHR, hatch="....")
    # water/pressure channel
    ax.add_patch(Rectangle(P(-1.5, 0), 3 * s, 114.5 * s, fc="#cfe8f5", ec="none", zorder=3))
    # kit lever cheeks + screws 97 at pin height
    z = STACK["PIN"]
    both(5.1, 8.1, z - 11, z + 11, "#bfc5cc", hatch="\\\\\\\\")
    for sg in (-1, 1):
        x0, x1 = sorted([sg * 8.1, sg * 11.6]); rect(x0, x1, z - 4.6, z + 4.6, "#9aa1a8", hatch="")
        x0, x1 = sorted([sg * 2.0, sg * 8.1]); rect(x0, x1, z - 2.5, z + 2.5, "#9aa1a8", hatch="")
    # stop nut 96, extension 93, adapter 92
    both(5, 9.2, 96.5, 101.5, "#bfc5cc")
    both(1.25, 7, 102.5, 140.5, CHR); both(5, 7, 102.5, 114.5, CHR, hatch="....")
    ax.add_patch(Rectangle(P(-1.25, 114.5), 2.5 * s, 26 * s, fc="#cfe8f5", ec="none", zorder=3))
    both(1, 4, 134.5, 140.5, BRASS); both(1, 8.1, 140.5, 148.5, BRASS)
    # gauge 91 (stem + case seen from front)
    both(0.8, 4.86, 139.5, 153.5, BRASS, hatch="")
    ax.add_patch(Circle(P(0, STACK["GAUGE_C"]), 22 * s, fc="#cfd3d8", ec=INK, lw=0.6, zorder=4))
    ax.add_patch(Circle(P(0, STACK["GAUGE_C"]), 19 * s, fc="#fbfbf3", ec=INK, lw=0.4, zorder=5))
    ax.text(*P(0, STACK["GAUGE_C"]), "0-16 bar", fontsize=4, ha="center", va="center", zorder=6)
    cl(ax, P(0, -6), P(0, H + 2))
    # height chain on the left
    chain = [0, 30, 96.5, 102.5, 140.5, 148.5, 197.5]
    xr = P(-30, 0)[0]
    for a, b in zip(chain, chain[1:]): vdim(ax, P(0, a)[1], P(0, b)[1], P(-22, a)[0], P(-8, b)[0], xr, f"{b - a:g}", size=3.8)
    vdim(ax, P(0, 0)[1], P(0, 197.5)[1], xr, xr, xr - 9, "197.5 overall", size=3.8)
    # tags on the right
    for k, zz, rr in [("A", 15, 22), ("B", 60, 5), ("C", z, 11.6), ("D", 99, 9.2), ("E", 120, 7), ("F", 144, 8.1), ("G", 175.5, 22), ("H", 50, 1.5)]:
        x, y = P(rr, zz); SP.tag(ax, x + 6, y, k); ax.plot([P(rr, 0)[0], x + 4.4], [y, y], lw=0.3, color=DIMC, zorder=24)

KEYS_ASM = [("", "Height chain from the piston bottom face (Z 0):"), ("A", "Hollow piston 95, 30 tall, Ø43.9"), ("B", "Hollow rod 94, Ø10, top 114.5"),
            ("C", "Kit lever cheeks + 2 screws M5 (97) at Z 76.9"), ("D", "Stop nut 96, Z 96.5 to 101.5"), ("E", "Extension 93, Ø14, Z 102.5 to 140.5"),
            ("F", "Adapter 92, hex 14, top Z 148.5"), ("G", "Gauge 91 Ø44, top Z 197.5"), ("H", "Pressure channel Ø3 / Ø2.5 / Ø2, water filled"),
            ("", "Channel volume ≈ 1 mL (dead volume, fills on 1st pull)"), ("", "Gauge rides with the rod: +29.5 mm at lever down"),
            ("", "Lever: kit lever with screwed cheeks replaces 49"), ("", "  (original rod-pin holes do not fit)"),
            ("", "Install: lever off -> piston out (14 AF top) ->"), ("", "  grease, fit 95+94 -> refit lever -> nut 96 ->"),
            ("", "  extension + gauge (PTFE tape) -> screws 97.")]

def faces_asm():
    F = []
    F += ISO.cyl((0, 0, 0), (0, 0, 30), 21.95, col=BRASS, n=32)
    F += ISO.cyl((0, 0, 30), (0, 0, 114.5), 5, col=CHR, n=16)
    F += ISO.box(-8.1, 8.1, -6, 6, 66, 88, col="#bfc5cc")
    F += ISO.cyl((0, 0, 96.5), (0, 0, 101.5), 9.2, col="#bfc5cc", shape="hex")
    F += ISO.cyl((0, 0, 102.5), (0, 0, 140.5), 7, col=CHR, n=20)
    F += ISO.cyl((0, 0, 140.5), (0, 0, 148.5), 8.1, col=BRASS, shape="hex")
    F += ISO.cyl((0, 0, 148.5), (0, 0, 153.5), 4.9, col=BRASS, n=12)
    F += gauge_faces(175.5)
    return F

def gauge_faces(zc):
    """Case Ø44 x 26 with the dial facing the viewer (-Y), cream dial Ø40 and needle."""
    F = ISO.cyl((0, 13, zc), (0, -13, zc), 22, col="#9aa1a8", n=40)
    # dial + needle: shifted along the view direction (no change in the picture) so the painter's sort draws them on top of the case
    V = ISO.VIEW
    ring = [np.array([19 * np.cos(t), -13.05, zc + 19 * np.sin(t)]) + 25 * V for t in np.linspace(0, 2 * np.pi, 48, endpoint=False)]
    F += [(np.array(ring), "#fbf8ec")]
    a = np.radians(225 - 9 / 16 * 270)
    F += [(np.array([[0, -13.2, zc - 0.9], [14 * np.cos(a), -13.2, zc + 14 * np.sin(a)], [0, -13.2, zc + 0.9]]) + 50 * V, "#c00000")]
    for k in range(5):
        b = np.radians(225 - k * 67.5)
        F += [(np.array([[15.5 * np.cos(b) - 0.5 * np.sin(b), -13.2, zc + 15.5 * np.sin(b) + 0.5 * np.cos(b)], [15.5 * np.cos(b) + 0.5 * np.sin(b), -13.2, zc + 15.5 * np.sin(b) - 0.5 * np.cos(b)],
                         [18.5 * np.cos(b) + 0.5 * np.sin(b), -13.2, zc + 18.5 * np.sin(b) - 0.5 * np.cos(b)], [18.5 * np.cos(b) - 0.5 * np.sin(b), -13.2, zc + 18.5 * np.sin(b) + 0.5 * np.cos(b)]]) + 40 * V, "#222222")]
    return F

def faces_gauge():
    return ISO.cyl((0, 0, -14), (0, 0, 0), 4.9, col=BRASS, n=12) + gauge_faces(22)

def build(pdf, Sheet):
    sh = Sheet(None, "OPTION - GROUP PRESSURE-GAUGE KIT 1 (second gauge on the lever: assembly + gauge)", "see cells")
    (x, y, w, h), (x2, y2, w2, h2) = grid(sh.ax, 1, 2)
    c = Cell(sh.ax, x, y, w, h, "OPT", "Piston pressure-gauge kit - assembly section", "Kit: Coffee Sensor type (items 91-97)", "1 set", "V/E")
    isob, tab, sub = SP.split(c, 0.42); assembly_drawing(sub); SP.key_table(sh.ax, tab, KEYS_ASM); SP.iso_thumb(sh.ax, faces_asm(), isob)
    c = Cell(sh.ax, x2, y2, w2, h2, 91, "Group pressure gauge 0-16 bar", "Bought-in: chrome case, glass lens, brass G1/8 stem", 1, "D/V")
    isob, tab, sub = SP.split(c, 0.42); gauge16_drawing(sub); SP.key_table(sh.ax, tab, KEYS91); SP.iso_thumb(sh.ax, faces_gauge(), isob)
    sh.ax.text(14, 50, "WHAT IT IS: the second gauge seen on some Professionals is NOT factory standard on the PL/PB-16. It is a retrofit kit (or the Esperto models' factory part):\n"
               "hollow piston + hollow rod carry the brew pressure up to a 0-16 bar gauge that rides on top of the rod. The sight-glass gauge 71 (0-2.5 bar) still reads boiler pressure.",
               fontsize=5, va="top", color=NOTE, linespacing=1.4)
    sh.save(pdf)
    sh = Sheet(None, "OPTION - GROUP PRESSURE-GAUGE KIT 2 (kit parts)", "see cells")
    for (x, y, w, h), it in zip(grid(sh.ax, 2, 3), [92, 93, 94, 95, 96, 97]):
        SP.cell_turned(sh.ax, x, y, w, h, it, *TURNED[it][:4], TURNED[it][4], col=BRASS if it in (92, 95) else CHR)
    sh.save(pdf)

BOM = [("91", 1, "Group pressure gauge (option)", "Chrome case, glass, brass stem", "Ø40 dial, 0-1600 kPa, G1/8, EN 837-1 cl.1.6", "D/V", "opt 1"),
       ("92", 1, "Gauge adapter (option)", BRB, "hex 14, M8x1 / G1/8-F", "E", "opt 2"),
       ("93", 1, "Gauge extension (option)", "Brass, chromed", "Ø14 x 38, M10x1-F / M8x1-F", "V/E", "opt 2"),
       ("94", 1, "Hollow piston rod (option, replaces 38)", "AISI 303", "Ø10 x 98.5, Ø3 bore, M10x1 top", "E", "opt 2"),
       ("95", 1, "Hollow piston (option, replaces 36)", BRB, "Ø43.9 x 30, Ø3 through", "D/E", "opt 2"),
       ("96", 1, "Stop nut M10x1 (option)", "A2", "16 AF x 5", "E", "opt 2"),
       ("97", 2, "Lever screw M5x10 + washer (option)", "A2-70", "M5 x 10", "E", "opt 2"),
       ("98", 1, "Kit lever, screwed cheeks (option, replaces 49)", "Brass, chromed", "as 49, cheek gap 10.2", "E", "opt 1")]
FASTENERS = [("97", 2, "Hex screw + washer", "ISO 4017/7089", "M5 x 10", "A2-70", "OPTION: kit lever cheeks -> hollow rod 94", "8 mm AF", "4 N·m + Loctite 243"),
             ("92/93", 1, "Threaded joints", "ISO 228 / ISO 261", "G1/8, M8x1, M10x1", "Brass", "OPTION: gauge -> adapter -> extension -> rod", "14 mm AF", "hand + 1/4 turn, PTFE")]

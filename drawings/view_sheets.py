"""Six fully dimensioned orthographic views (sheets 1-3)."""
import math
from matplotlib.patches import Circle
from views import D, model, ViewPort, rounded_trap, DIMC, INK

M = model()
NOTE = "#7a1f1f"
a_pf = math.radians(D["PF_ANG"])
PF_END = (D["GX"] + 152 * math.cos(a_pf), 152 * math.sin(a_pf), 165)
la = math.radians(D["LEV_ANG"])
LEV_END = (D["FX"] + D["LEV_L"] * math.cos(la), 0, D["FZ"] - D["LEV_L"] * math.sin(la))
X_MIN = D["STK_X0"]; X_MAX = LEV_END[0] + 11 * math.cos(la)   # round end cap of the handle
Y_MIN = PF_END[1] - 12 * abs(math.sin(a_pf))

# ------------------------------------------------------------------ ordinate dimension helpers
def _spread(vals, gap):
    order = sorted(range(len(vals)), key=lambda i: vals[i]); out = list(vals); last = -1e9
    for i in order:
        out[i] = max(vals[i], last + gap); last = out[i]
    shift = (sum(out) - sum(vals)) / len(vals) if vals else 0          # re-centre the stack
    return [o - shift * 0.5 for o in out]

def ord_v(vp, items, xcol, side=1, gap=3.1, size=4.6, title="Z"):
    """Vertical ordinate column (heights). items: [(model point, label)]. side=+1 labels to the right of xcol."""
    ax = vp.ax; F = [vp.P(*p) for p, _ in items]
    ly = _spread([f[1] for f in F], gap)
    ys = [f[1] for f in F]
    ax.plot([xcol, xcol], [min(ys + ly) - 1, max(ys + ly) + 1], lw=0.25, color=DIMC, zorder=20)
    for (p, lab), f, y in zip(items, F, ly):
        x_end = xcol - 2.5 * side
        ax.plot([f[0] + 0.8 * side, x_end], [f[1], f[1]], lw=0.18, color=DIMC, zorder=20)
        ax.plot([x_end, xcol + 1.5 * side], [f[1], y], lw=0.18, color=DIMC, zorder=20)
        ax.plot([xcol - 0.8, xcol + 0.8], [f[1], f[1]], lw=0.4, color=DIMC, zorder=20)
        ax.text(xcol + 2 * side, y, lab, fontsize=size, color=DIMC, ha="left" if side > 0 else "right", va="center", zorder=22,
                bbox=dict(fc="white", ec="none", pad=0.1))
    ax.text(xcol, max(ys + ly) + 3, title, fontsize=5, color=DIMC, ha="center", va="bottom", weight="bold")

def ord_h(vp, items, ycol, gap=3.0, size=4.6, title="X"):
    """Horizontal ordinate row (positions). Labels rotated 90 deg below ycol."""
    ax = vp.ax; F = [vp.P(*p) for p, _ in items]
    lx = _spread([f[0] for f in F], gap)
    xs = [f[0] for f in F]
    ax.plot([min(xs + lx) - 1, max(xs + lx) + 1], [ycol, ycol], lw=0.25, color=DIMC, zorder=20)
    for (p, lab), f, x in zip(items, F, lx):
        ax.plot([f[0], f[0]], [f[1] - 0.8, ycol + 2.5], lw=0.18, color=DIMC, zorder=20)
        ax.plot([f[0], x], [ycol + 2.5, ycol - 1.5], lw=0.18, color=DIMC, zorder=20)
        ax.plot([f[0], f[0]], [ycol - 0.8, ycol + 0.8], lw=0.4, color=DIMC, zorder=20)
        ax.text(x, ycol - 2, lab, fontsize=size, color=DIMC, ha="center", va="top", rotation=90, zorder=22, bbox=dict(fc="white", ec="none", pad=0.1))
    ax.text(min(xs + lx) - 3, ycol, title, fontsize=5, color=DIMC, ha="right", va="center", weight="bold")

def view_arrow(ax, x, y, txt):
    ax.text(x, y, txt, fontsize=5.2, color=NOTE, ha="center", va="center", style="italic")

# ================================================================== SHEET 1  FRONT + REAR (1:2)
def sheet_front_rear(pdf, Sheet):
    sh = Sheet(1, "ORTHOGRAPHIC VIEWS 1/3 - FRONT VIEW & REAR VIEW", "1:2")
    s = 0.5; d = D
    # -------- FRONT (viewer at +X, user position)
    f = ViewPort(sh.ax, "FRONT", 100, 72, s); f.draw(M)
    f.cl((0, 0, -6), (0, 0, 330))
    f.label("FRONT VIEW  (from user side, +X)", 100, 270, "scale 1:2  -  Y measured from machine centre line")
    ord_v(f, [((0, 90, 0), "0 table"), ((0, 92, d["RUB_H"]), f"{d['RUB_H']} rubber lip"), ((0, 85, d["BASE_H"]), f"{d['BASE_H']} base top"),
              ((d["GX"], 15, d["SPOUT_Z"]), f"{d['SPOUT_Z']} spout tip"), ((d["GX"], 30, d["PF_Z0"]), f"{d['PF_Z0']} PF bottom"),
              ((d["GX"], 36, d["BELL_Z0"]), f"{d['BELL_Z0']} bell"), ((d["GX"], 36, d["BELL_Z1"]), f"{d['BELL_Z1']} bell top"),
              ((d["BX"], 38, d["SH_Z1"]), f"{d['SH_Z1']} shell top"), ((d["BX"], 22, d["SHO_Z"]), f"{d['SHO_Z']} shoulder"),
              ((d["GX"], 10, d["YOKE_Z1"]), f"{d['YOKE_Z1']} yoke top"), ((d["GX"], 7.5, d["ACORN_Z"]), f"{d['ACORN_Z']} acorn top"),
              ((d["BX"], 29, d["TOP"]), f"{d['TOP']} cap top [D]")], xcol=152)
    f.hdim((0, -90, 0), (0, 90, 0), 63, "180 base width", "D")
    f.hdim((0, Y_MIN, 160), (0, 90, 0), 56, f"{90 - Y_MIN:.0f} overall incl. portafilter handle", "V")
    f.hdim((d["BX"], -29, d["TOP"]), (d["BX"], 29, d["TOP"]), f.P(0, 0, d["TOP"])[1] + 3, "Ø58 cap knob", "V")
    f.hdim((d["BX"], -38, 235), (d["BX"], 38, 235), f.P(0, 0, 252)[1], "Ø76 shell", "V")
    f.hdim((d["GX"], -36, 196), (d["GX"], 36, 196), f.P(0, 0, 204)[1], "Ø72 bell", "D")
    f.hdim((d["GX"], -15, 134), (d["GX"], 15, 134), f.P(0, 0, 122)[1], "30 spout c/c", "V")
    f.dia((LEV_END[0], 0, LEV_END[2]), 11, "22 lever handle", "V", ang=30, ext=14)
    f.leader((270, d["BADGE_Y"], d["BADGE_Z"]), f"badge Ø{d['BADGE_D']} @ Y{d['BADGE_Y']}, Z{d['BADGE_Z']} [V]", -18, 16)
    f.leader(PF_END, "PF handle end (locked) [V]", -2, 22)
    # -------- REAR (viewer at -X)
    r = ViewPort(sh.ax, "REAR", 282, 72, s); r.draw(M)
    r.cl((0, 0, -6), (0, 0, 330))
    r.label("REAR VIEW  (from -X)", 282, 270, "scale 1:2  -  note: left/right mirrored vs front view")
    ord_v(r, [((0, -90, 0), "0"), ((0, -92, d["RUB_H"]), f"{d['RUB_H']}"), ((0, -40, 25), "25 cable gland"), ((0, -85, d["BASE_H"]), f"{d['BASE_H']}"),
              ((d["BX"], -46, d["FOOT_Z"]), f"{d['FOOT_Z']} boiler foot"), ((d["SG_X"], d["SG_Y"] - 9, d["SG_Z0"]), f"{d['SG_Z0']} sight glass c/c low"),
              ((d["SG_X"], d["SG_Y"] - 9, d["SG_Z1"]), f"{d['SG_Z1']} sight glass c/c high"), ((d["BX"], -38, d["SH_Z1"]), f"{d['SH_Z1']}"),
              ((0, -12, d["STK_Z"]), f"{d['STK_Z']} steam valve axis"), ((d["BX"], -22, d["NECK_Z"]), f"{d['NECK_Z']} neck"),
              ((d["BX"], -19, d["CAP_Z"]), f"{d['CAP_Z']} knob base"), ((d["BX"], -29, d["TOP"]), f"{d['TOP']}")], xcol=r.P(0, -95, 0)[0] + 8)
    r.hdim((0, 90, 0), (0, -90, 0), 63, "180", "D")
    r.hdim((d["BX"], 46, 60), (d["BX"], -46, 60), 66.5, "Ø92 foot ring", "V", size=4.6)
    r.hdim((0, 0, 280), (0, d["SG_Y"], 280), r.P(0, 0, 290)[1], f"{-d['SG_Y']} sight glass offset", "V", size=4.6)
    r.dia((0, -12, d["STK_Z"]), d["STK_D"] / 2, f"{d['STK_D']} steam knob", "V", ang=150, ext=10)
    r.dia((0, 40, 25), 8, "16 gland (M16x1.5)", "E", ang=160, ext=8)
    r.hdim((0, 0, 20), (0, 40, 20), 76, "40", "V", size=4.6)
    sh.ax.text(345, 285, "READING THESE VIEWS", fontsize=6.5, weight="bold", va="top")
    sh.ax.text(345, 279, "\n".join([
        "Datums:", " Z = 0 at table (underside of rubber cover)", " X = 0 at rear end of base", " Y = 0 on boiler/group centre line",
        "  (-Y = left side = switch side)", "", "Ordinate columns give the height of",
        "each feature above the table.", "", "[D] documented value", "[V] scaled from video frame 30:31",
        "     (calibrated on Ø72 bell and 320", "     overall height; +/-3 mm)", "[E] estimate", "",
        "Knobs and handles are drawn as the", "restored maple parts; the 1979", "black phenolic originals have the",
        "same envelope.", "", "Lever drawn at rest (down, 24.9°)."]), fontsize=5, va="top", linespacing=1.35)
    sh.save(pdf)

# ================================================================== SHEET 2  LEFT + RIGHT (1:2.5)
def sheet_sides(pdf, Sheet):
    sh = Sheet(2, "ORTHOGRAPHIC VIEWS 2/3 - LEFT SIDE (SWITCH SIDE) & RIGHT SIDE", "1:2.5")
    s = 0.4; d = D
    L = ViewPort(sh.ax, "LEFT", 22 - X_MIN * s, 92, s); L.draw(M)
    L.cl((d["BX"], -95, -5), (d["BX"], -95, 328)); L.cl((d["GX"], -95, 120), (d["GX"], -95, 318))
    L.label("LEFT SIDE VIEW  (from -Y, switch side)", 105, 46, "scale 1:2.5")
    ord_v(L, [((0, -90, 0), "0"), ((5, -92, d["RUB_H"]), f"{d['RUB_H']}"), ((d["SW_X"], -91, d["SW_Z"]), f"{d['SW_Z']} switch c"),
              ((250, -85, d["BASE_H"]), f"{d['BASE_H']}"), ((d["BX"] + 46, -50, d["FOOT_Z"]), f"{d['FOOT_Z']}"),
              ((d["SG_X"] + 9, d["SG_Y"], d["SG_Z0"]), f"{d['SG_Z0']} SG"), ((d["GX"], -15, d["SPOUT_Z"]), f"{d['SPOUT_Z']} spout"),
              ((d["GX"] + 30, -10, d["PF_Z0"]), f"{d['PF_Z0']}"), (LEV_END, f"{LEV_END[2]:.0f} handle end"),
              ((d["GX"] + 36, -10, d["BELL_Z0"]), f"{d['BELL_Z0']}"), ((d["GX"] + 36, -10, d["BELL_Z1"]), f"{d['BELL_Z1']}"),
              ((134, -18, d["PORT_Z"]), f"{d['PORT_Z']} port c"), ((d["SG_X"] + 9, d["SG_Y"], d["SG_Z1"]), f"{d['SG_Z1']} SG"),
              ((d["BX"] + 38, -10, d["SH_Z1"]), f"{d['SH_Z1']}"), ((d["BX"] + 22, -10, d["SHO_Z"]), f"{d['SHO_Z']}"),
              ((d["STK_X0"], -12, d["STK_Z"]), f"{d['STK_Z']} steam"), ((d["BX"] + 22, -10, d["NECK_Z"]), f"{d['NECK_Z']}"),
              ((d["FX"], -13, d["FZ"]), f"{d['FZ']} fulcrum"), ((d["GX"] + 9, -10, d["YOKE_Z1"]), f"{d['YOKE_Z1']}"),
              ((d["BX"] + 29, -10, d["CAP_Z"]), f"{d['CAP_Z']}"), ((d["GX"] + 7, -10, d["ACORN_Z"]), f"{d['ACORN_Z']}"),
              ((d["BX"] + 29, -10, d["TOP"]), f"{d['TOP']} [D]")], xcol=L.P(X_MAX, 0, 0)[0] + 4, gap=2.9, size=4.3)
    ord_h(L, [((X_MIN, -12, d["STK_Z"] - 18), f"{X_MIN}"), ((0, -90, 0), "0"), ((d["SG_X"], d["SG_Y"], d["SG_Z0"] - 15), f"{d['SG_X']} SG"),
              ((d["SW_X"], -91, d["SW_Z"] - 13), f"{d['SW_X']} switch"), ((d["BX"], -46, 60), f"{d['BX']} boiler"),
              ((d["TRAY_X0"], -56, 60), f"{d['TRAY_X0']} grid"), ((d["FX"], -13, d["FZ"]), f"{d['FX']} fulcrum"),
              ((d["GX"], -30, d["PF_Z0"]), f"{d['GX']} group"), ((d["TRAY_X0"] + d["TRAY_L"], -56, 60), f"{d['TRAY_X0'] + d['TRAY_L']}"),
              ((d["L"], -85, 0), f"{d['L']} [D]"), (LEV_END, f"{LEV_END[0]:.0f} handle")], ycol=L.P(0, 0, 0)[1] - 6, gap=3.2, size=4.3)
    L.hdim((X_MIN, 0, 0), (X_MAX, 0, 0), L.P(0, 0, 0)[1] - 30, f"{X_MAX - X_MIN:.0f} overall depth incl. lever & steam knob", "V")
    L.angle((d["FX"], -13, d["FZ"]), 16, -d["LEV_ANG"], 0, f"{d['LEV_ANG']}° lever at rest", size=4.6)
    L.hdim((d["SW_X"] - 15, -91, d["SW_Z"] + 11), (d["SW_X"] + 15, -91, d["SW_Z"] + 11), L.P(0, 0, 46)[1], f"{d['SW_W']}x{d['SW_H']} switch", "V", size=4.3)
    # ---- RIGHT
    R = ViewPort(sh.ax, "RIGHT", 228 + X_MAX * s, 92, s); R.draw(M)
    R.cl((d["BX"], 95, -5), (d["BX"], 95, 328)); R.cl((d["GX"], 95, 120), (d["GX"], 95, 318))
    R.label("RIGHT SIDE VIEW  (from +Y)", 310, 46, "scale 1:2.5  -  front (+X) is on the LEFT in this view")
    yb = R.P(0, 0, 0)[1]
    R.hdim((d["GX"], 0, 0), (d["BX"], 0, 0), yb - 7, f"{d['GX'] - d['BX']} boiler-group c/c", "V", size=4.5)
    R.hdim((d["L"], 0, 0), (d["BX"], 0, 0), yb - 13, f"{d['L'] - d['BX']}", "V", size=4.5)
    R.hdim((d["BX"], 0, 0), (0, 0, 0), yb - 13, f"{d['BX']}", "V", size=4.5)
    R.hdim((LEV_END[0], 0, 0), (d["FX"], 0, 0), yb - 19, f"{LEV_END[0] - d['FX']:.0f} fulcrum to handle end", "V", size=4.5)
    R.vdim((d["GX"] + 20, 0, d["BASE_H"]), (d["GX"] + 20, 0, d["SPOUT_Z"]), R.P(d["GX"] + 40, 0, 0)[0], f"{d['SPOUT_Z'] - d['BASE_H']} cup clearance", "V", size=4.5)
    R.vdim((134, 18, d["PORT_Z"] - 19), (134, 18, d["PORT_Z"] + 19), R.P(150, 0, 0)[0], f"{d['BOLT_CC']} bolt c/c", "V", size=4.3)
    R.vdim((d["SV_X"], 12, 264), (d["SV_X"], 12, 288), R.P(d["SV_X"] - 16, 0, 0)[0], "24", "E", size=4.3)
    R.leader((d["SV_X"], 23, 280), "safety valve cup Ø22 [V/E]", -6, 18)
    R.leader((124, 28, 180), "drain tube Ø5 to tray [V]", 22, -8)
    R.leader((d["GX"], 0, 230), "group body Ø50 [E]", 26, 8)
    R.leader((-4, 47, 25), "cable gland / cord", 8, -14)
    R.leader((d["FX"] + 150 * math.cos(la), 6, d["FZ"] - 150 * math.sin(la)), "lever rod Ø11 [V]", -10, 16)
    R.leader((d["FX"] + 230 * math.cos(la), 12, d["FZ"] - 230 * math.sin(la)), f"handle Ø{d['HANDLE_D']} x {d['HANDLE_L']} [V]", -4, 18)
    # machine data block above
    rows = [("Model", "La Pavoni Europiccola, 2nd series v2.2 (1978-83) - pre-millennium"), ("Production stamp", "'2 79' under base = February 1979"),
            ("Capacity / supply / power", "0.8 l / 220 V 50 Hz / 200 W (I) + 800 W (II) [D]"),
            ("Envelope (H x W x D)", f"320 x 180 x 270 base [D];  with handles {90 - Y_MIN:.0f} wide, {X_MAX - X_MIN:.0f} deep [V]"),
            ("Mass", "5.5 kg dry [D]"), ("Lever ratio", f"{d['LEV_L']} / 27.6 = 9.9 : 1 [V/E]")]
    for i, (k, v) in enumerate(rows):
        y = 284 - i * 4.8
        sh.ax.text(228, y, k, fontsize=5.3, va="top", weight="bold"); sh.ax.text(272, y, v, fontsize=5.3, va="top")
    sh.save(pdf)

# ================================================================== SHEET 3  TOP + BOTTOM (1:2.5)
def grid_holes(vp):
    d = D
    for i in range(10):
        for j in range(8):
            x = d["TRAY_X0"] + 12 + i * 13; y = -44 + j * 12.6
            if abs(i - 4.5) < 1 and abs(j - 3.5) < 1: continue
            vp.ax.add_patch(Circle(vp.P(x, y, 61), 4 * vp.s, fc="#7f7f7f", ec=INK, lw=0.2, zorder=3.5))

def sheet_plan(pdf, Sheet):
    sh = Sheet(3, "ORTHOGRAPHIC VIEWS 3/3 - TOP VIEW (PLAN) & BOTTOM VIEW", "1:2.5")
    s = 0.4; d = D
    T = ViewPort(sh.ax, "TOP", 30 - X_MIN * s, 222, s); T.draw(M)
    # redraw items above the grid (group, lever, PF) by drawing model again only for prims above z 100
    T.cl((d["BX"], -100, 400), (d["BX"], 100, 400)); T.cl((X_MIN - 5, 0, 400), (X_MAX + 5, 0, 400)); T.cl((d["GX"], -100, 400), (d["GX"], 100, 400))
    T.label("TOP VIEW  (plan, from above)", 230, 284, "scale 1:2.5")
    ord_v(T, [((d["L"], -90, 0), "-90 left side [D]"), (PF_END, f"{PF_END[1]:.0f} PF handle"), ((d["SG_X"], d["SG_Y"], 250), f"{d['SG_Y']} sight glass"),
              ((d["SW_X"], -91, 30), "-91 switch face"), ((-20, -12, d["STK_Z"]), "-12 steam valve"), ((d["L"], 0, 0), "0 CL"),
              ((d["SV_X"], d["SV_Y"], 290), f"+{d['SV_Y']} safety valve"), ((126, 26, 200), "+26 drain"),
              ((-5, 40, 25), "+40 cable gland"), ((d["L"], 90, 0), "+90 right side")], xcol=T.P(X_MAX, 0, 0)[0] + 4, gap=3.0, size=4.4, title="Y")
    T.hdim((0, 95, 0), (d["L"], 95, 0), T.P(0, 95, 0)[1] + 6, "270 base [D]", "")
    T.hdim((d["TRAY_X0"], 70, 0), (d["TRAY_X0"] + d["TRAY_L"], 70, 0), T.P(0, 60, 0)[1] + 2, f"{d['TRAY_L']} grid", "V", size=4.5)
    T.vdim((d["TRAY_X0"] + d["TRAY_L"] + 5, -d["TRAY_W"] / 2, 0), (d["TRAY_X0"] + d["TRAY_L"] + 5, d["TRAY_W"] / 2, 0),
           T.P(d["TRAY_X0"] + d["TRAY_L"] + 14, 0, 0)[0], f"{d['TRAY_W']}", "V", size=4.5)
    T.vdim((d["L"] - 3, -d["W_FRONT"] / 2, 0), (d["L"] - 3, d["W_FRONT"] / 2, 0), T.P(d["L"] + 12, 0, 0)[0], f"{d['W_FRONT']} front", "V", size=4.5)
    T.dia((d["BX"], 0, 330), 29, "58 cap knob (6-lobe)", "V", ang=110, ext=12)
    T.dia((d["BX"], 0, 60), 46, "92 foot ring", "V", ang=215, ext=8)
    T.dia((d["GX"], 0, 200), 36, "72 bell", "D", ang=60, ext=26)
    T.dia((d["SV_X"], d["SV_Y"], 290), 11, "22 safety-valve cup", "V", ang=75, ext=26)
    T.angle((d["GX"], 0, 300), 20, 180, d["PF_ANG"], f"{d['PF_ANG'] - 180}° PF handle (locked)", size=4.5)
    T.leader((d["TRAY_X0"] + 125, -40, 61), "~70 holes Ø8, AISI 304 grid [V]", 22, -24)
    # ---- BOTTOM
    B = ViewPort(sh.ax, "BOTTOM", 30 - X_MIN * s, 108, s); B.draw(M)
    B.cl((X_MIN - 5, 0, -50), (X_MAX + 5, 0, -50)); B.cl((d["BX"], -100, -50), (d["BX"], 100, -50))
    B.hidden_circle((d["BX"], 0, -50), 42, "#cfcfcf"); B.hidden_circle((d["BX"], 0, -50), 40, "#cfcfcf")
    for k in range(3):
        a = math.radians(90 + 120 * k)
        B.hidden_circle((d["BX"] + 52 * math.cos(a), 52 * math.sin(a), -50), 3, "#cfcfcf")
    B.label("BOTTOM VIEW  (from below, -Z)", 110, 60, "scale 1:2.5  -  right side (+Y) at the bottom in this view")
    B.hdim((-2, -94, 0), (d["L"] + 2, -94, 0), B.P(0, -94, 0)[1] + 5, "274 rubber cover", "V", size=4.5)
    B.vdim((d["L"] - 40, -92, 0), (d["L"] - 40, 92, 0), B.P(d["L"] + 8, 0, 0)[0], "184 rubber cover", "V", size=4.5)
    B.leader((d["BX"] + 42 * math.cos(math.radians(-30)), 42 * math.sin(math.radians(-30)), -50),
             "hidden: element flange Ø84 [D], 3 screws on PCD 104 [E]", 40, -16)
    B.leader((d["BX"] + 35, 60, 0), "rubber cover SBR/NR, pressed on, no screws seen", 60, -6)
    sh.ax.text(255, 285, "PLAN NOTES", fontsize=6.5, weight="bold", va="top")
    sh.ax.text(255, 279, "\n".join([
        "Y ordinates are measured from the machine centre line through",
        "the boiler and group axes (-Y = switch side).",
        "Base outline: rounded trapezoid, rear 180 [D], front 170 [V],",
        f"corner R{D['BASE_R']} [E]; side walls drafted ~6 mm inwards over 52 mm.",
        "Boiler axis 70 from rear [V]; group axis 155 [V].",
        f"Portafilter handle shown locked at {D['PF_ANG'] - 180}° to the rear-left as in",
        "frame 30:31; its position depends on gasket wear.",
        "Drip grid recess sits 1 mm below the base top."]), fontsize=5.2, va="top", linespacing=1.35)
    sh.save(pdf)

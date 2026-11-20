"""Six fully dimensioned orthographic views (sheets 1-3)."""
import math
from matplotlib.patches import Circle
from views import D, model, ViewPort, rounded_trap, DIMC, INK

M = model()
NOTE = "#7a1f1f"
a_pf = math.radians(D["PF_ANG"])
PF_END = (D["GX"] + 154 * math.cos(a_pf), 154 * math.sin(a_pf), 165)
la = math.radians(D["LEV_ANG"])
LEV_END = (D["FX"] + D["LEV_L"] * math.cos(la), 0, D["FZ"] - D["LEV_L"] * math.sin(la))
X_MIN = -48; X_MAX = LEV_END[0] + 12 * math.cos(la)   # round end cap of the handle
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

# ================================================================== SHEET  FRONT + REAR (1:2)
def sheet_front_rear(pdf, Sheet):
    sh = Sheet(None, "ORTHOGRAPHIC VIEWS 1/3 - FRONT VIEW & REAR VIEW", "1:2")
    s = 0.5; d = D; W2 = d["W_REAR"] / 2
    f = ViewPort(sh.ax, "FRONT", 110, 66, s); f.draw(M)
    f.cl((0, 0, -6), (0, 0, 352))
    f.label("FRONT VIEW  (from user side, +X)", 110, 270, "scale 1:2  -  Y measured from machine centre line")
    ord_v(f, [((0, W2, 0), "0 table"), ((0, W2, d["RUB_H"]), f"{d['RUB_H']} sub-base top"), ((0, W2, d["BASE_H"]), f"{d['BASE_H']} base top"),
              ((d["BX"], 50, d["FOOT_Z"]), f"{d['FOOT_Z']} foot ring top"), ((d["GX"], 15, d["SPOUT_Z"]), f"{d['SPOUT_Z']} spout tip"),
              ((d["GX"], 31, d["PF_Z0"]), f"{d['PF_Z0']} PF bottom"), ((d["GX"], 38, d["BELL_Z0"]), f"{d['BELL_Z0']} bell"),
              ((d["BX"], 50, d["SEAM_Z"]), f"{d['SEAM_Z']} shell seam"), ((d["GX"], 38, d["BELL_Z1"]), f"{d['BELL_Z1']} bell top"),
              ((196, 34, 230), "230 steam tip"), ((d["BX"], 50, d["SH_Z1"]), f"{d['SH_Z1']} shoulder start"),
              ((d["GX"], 29, d["BODY_Z1"]), f"{d['BODY_Z1']} group top"), ((d["BX"], 24, d["SHO_Z"]), f"{d['SHO_Z']} neck"),
              ((d["SG_X"], d["SG_Y"], d["GAUGE_Z"]), f"{d['GAUGE_Z']} gauge C/L"), ((d["GX"], 8, d["YOKE_Z1"]), f"{d['YOKE_Z1']} column top"),
              ((d["STK_X"], 20, d["STK_Z"]), f"{d['STK_Z']} steam valve C/L"), ((d["GX"], 7.5, d["ACORN_Z"]), f"{d['ACORN_Z']} acorn"),
              ((d["BX"], 19, d["CAP_Z"]), f"{d['CAP_Z']} knob base"), ((d["BX"], 29, d["TOP"]), f"{d['TOP']} cap top [V]")], xcol=170, gap=3.0, size=4.4)
    f.hdim((0, -W2, 0), (0, W2, 0), f.P(0, 0, 0)[1] - 7, f"{d['W_REAR']} base width [D]", "")
    f.hdim((0, Y_MIN, 160), (0, W2, 0), f.P(0, 0, 0)[1] - 14, f"{W2 - Y_MIN:.0f} overall incl. portafilter handle", "V")
    f.hdim((d["BX"], -29, d["TOP"]), (d["BX"], 29, d["TOP"]), f.P(0, 0, d["TOP"])[1] + 3, "Ø58 cap knob", "V")
    f.hdim((d["BX"], -50, 236), (d["BX"], 50, 236), f.P(0, 0, 236)[1], "Ø100 copper boiler [D]", "")
    f.hdim((d["GX"], -38, 186), (d["GX"], 38, 186), f.P(0, 0, 186)[1], "Ø76 bell", "V")
    f.hdim((d["GX"], -15, 134), (d["GX"], 15, 134), f.P(0, 0, 122)[1], "30 spout c/c", "V")
    f.hdim((d["GX"], -22, d["PORT_Z"]), (d["GX"], 22, d["PORT_Z"]), f.P(0, 0, d["PORT_Z"] + 28)[1], f"{d['BOLT_CC']} group bolts c/c", "V/E", size=4.3)
    f.leader((290, d["BADGE_Y"], d["BADGE_Z"]), f"badge Ø{d['BADGE_D']} @ Y{d['BADGE_Y']}, Z{d['BADGE_Z']} [V]", -18, 14)
    f.leader(PF_END, "PF handle end (locked) [V]", -2, 22)
    f.leader((d["SG_X"], d["SG_Y"] - 14, d["GAUGE_Z"] + 8), f"gauge Ø{d['GAUGE_D']} bezel, 0-250 kPa [D]", -10, 16)
    r = ViewPort(sh.ax, "REAR", 300, 66, s); r.draw(M)
    r.cl((0, 0, -6), (0, 0, 352))
    r.label("REAR VIEW  (from -X)", 300, 270, "scale 1:2  -  left/right mirrored vs front view")
    ord_v(r, [((0, -W2, 0), "0"), ((0, 45, 30), "30 cable gland"), ((0, -W2, d["BASE_H"]), f"{d['BASE_H']}"),
              ((d["SG_X"], d["SG_Y"] - 9, d["SG_Z0"]), f"{d['SG_Z0']} sight glass c/c low"), ((d["SG_X"], d["SG_Y"] - 9, d["SG_Z1"]), f"{d['SG_Z1']} sight glass c/c high"),
              ((d["BX"], -50, d["SH_Z1"]), f"{d['SH_Z1']}"), ((d["STK_X"], d["STK_KNOB_Y"], d["STK_Z"]), f"{d['STK_Z']} steam knob C/L"),
              ((d["SG_X"], d["SG_Y"], d["GAUGE_Z"]), f"{d['GAUGE_Z']} gauge"), ((d["BX"], -24, d["NECK_Z"]), f"{d['NECK_Z']} neck top"),
              ((d["BX"], -19, d["CAP_Z"]), f"{d['CAP_Z']} knob base"), ((d["BX"], -29, d["TOP"]), f"{d['TOP']}")], xcol=r.P(0, -W2 - 6, 0)[0] + 10)
    r.hdim((0, W2, 0), (0, -W2, 0), r.P(0, 0, 0)[1] - 7, f"{d['W_REAR']}", "D")
    r.hdim((d["BX"], 56, 66), (d["BX"], -56, 66), r.P(0, 0, 0)[1] - 13, "Ø112 foot ring", "V", size=4.4)
    r.hdim((0, 0, 330), (0, d["SG_Y"], 330), r.P(0, 0, 352)[1], f"{-d['SG_Y']} sight glass offset", "V", size=4.4)
    r.hdim((0, 0, 312), (0, d["STK_KNOB_Y"], 312), r.P(0, 0, 360)[1], f"{-d['STK_KNOB_Y']} to knob end", "V", size=4.4)
    r.dia((d["STK_X"], d["STK_KNOB_Y"] + 11, d["STK_Z"]), d["STK_D"] / 2, f"{d['STK_D']} steam knob", "V", ang=150, ext=10)
    r.dia((0, 45, 30), 8, "16 gland (M16x1.5)", "E", ang=200, ext=10)
    sh.ax.text(352, 285, "READING THESE VIEWS", fontsize=6.5, weight="bold", va="top")
    sh.ax.text(352, 279, "\n".join([
        "Datums:", " Z = 0 at table (feet)", " X = 0 at rear of base", " Y = 0 boiler/group C/L", "  (-Y = left = switch,", "   sight glass, gauge)", "",
        "[D] documented value", "[V] scaled from product", "    photos, calibrated on", "    Ø40 gauge, Ø100 tank", "    (+/-5 mm)", "[E] estimate", "",
        "Lever drawn at rest", f"(down, {d['LEV_ANG']}°).", "Steam wand drawn in", "parked position."]), fontsize=5, va="top", linespacing=1.35)
    sh.save(pdf)

def sheet_sides(pdf, Sheet):
    sh = Sheet(None, "ORTHOGRAPHIC VIEWS 2/3 - LEFT SIDE (SWITCH SIDE) & RIGHT SIDE", "1:2.5")
    s = 0.4; d = D
    L = ViewPort(sh.ax, "LEFT", 24 - X_MIN * s, 96, s); L.draw(M)
    L.cl((d["BX"], -105, -5), (d["BX"], -105, 352)); L.cl((d["GX"], -105, 120), (d["GX"], -105, 320))
    L.label("LEFT SIDE VIEW  (from -Y, switch side)", 112, 50, "scale 1:2.5")
    ord_v(L, [((0, -100, 0), "0"), ((5, -100, d["RUB_H"]), f"{d['RUB_H']}"), ((d["SW_X"], -101, d["SW_Z"]), f"{d['SW_Z']} switch c"),
              ((270, -93, d["BASE_H"]), f"{d['BASE_H']}"), ((d["BX"] + 56, -50, d["FOOT_Z"]), f"{d['FOOT_Z']}"),
              ((d["SG_X"] + 9, d["SG_Y"], d["SG_Z0"]), f"{d['SG_Z0']} SG"), ((d["GX"], -15, d["SPOUT_Z"]), f"{d['SPOUT_Z']} spout"),
              ((d["GX"] + 31, -10, d["PF_Z0"]), f"{d['PF_Z0']}"), (LEV_END, f"{LEV_END[2]:.0f} handle end"),
              ((d["GX"] + 38, -10, d["BELL_Z0"]), f"{d['BELL_Z0']}"), ((d["BX"] + 50, -10, d["SEAM_Z"]), f"{d['SEAM_Z']} seam"),
              ((d["GX"] + 38, -10, d["BELL_Z1"]), f"{d['BELL_Z1']}"), ((d["PAD_X1"], -30, d["PORT_Z"]), f"{d['PORT_Z']} port c"),
              ((d["SG_X"] + 9, d["SG_Y"], d["SG_Z1"]), f"{d['SG_Z1']} SG"), ((d["BX"] + 50, -10, d["SH_Z1"]), f"{d['SH_Z1']}"),
              ((d["GX"] + 29, -10, d["BODY_Z1"]), f"{d['BODY_Z1']}"), ((d["BX"] + 24, -10, d["SHO_Z"]), f"{d['SHO_Z']}"),
              ((d["SG_X"] + 22, d["SG_Y"], d["GAUGE_Z"]), f"{d['GAUGE_Z']} gauge"), ((d["FX"], -13, d["FZ"]), f"{d['FZ']} fulcrum"),
              ((d["GX"] + 8, -10, d["YOKE_Z1"]), f"{d['YOKE_Z1']}"), ((d["STK_X"], d["STK_KNOB_Y"], d["STK_Z"]), f"{d['STK_Z']} steam"),
              ((d["GX"] + 7, -10, d["ACORN_Z"]), f"{d['ACORN_Z']}"), ((d["BX"] + 29, -10, d["CAP_Z"]), f"{d['CAP_Z']}"),
              ((d["BX"] + 29, -10, d["TOP"]), f"{d['TOP']} [V]")], xcol=L.P(X_MAX, 0, 0)[0] + 4, gap=2.8, size=4.2)
    ord_h(L, [((X_MIN, 54, 8), f"{X_MIN} cord"), ((0, -100, 0), "0"), ((d["STK_X"], d["STK_KNOB_Y"], d["STK_Z"] - 18), f"{d['STK_X']} steam knob"),
              ((d["SG_X"], d["SG_Y"], d["SG_Z0"] - 15), f"{d['SG_X']} SG"), ((d["SW_X"], -101, d["SW_Z"] - 16), f"{d['SW_X']} switch"),
              ((d["BX"], -56, 65), f"{d['BX']} boiler"), ((d["TRAY_X0"], -60, 64), f"{d['TRAY_X0']} tray"), ((d["FX"], -13, d["FZ"]), f"{d['FX']} fulcrum"),
              ((d["GX"], -31, d["PF_Z0"]), f"{d['GX']} group"), ((d["TRAY_X0"] + d["TRAY_L"], -60, 64), f"{d['TRAY_X0'] + d['TRAY_L']}"),
              ((d["L"], -93, 0), f"{d['L']} [D]"), (LEV_END, f"{LEV_END[0]:.0f} handle")], ycol=L.P(0, 0, 0)[1] - 6, gap=3.2, size=4.2)
    L.hdim((X_MIN, 0, 0), (X_MAX, 0, 0), L.P(0, 0, 0)[1] - 32, f"{X_MAX - X_MIN:.0f} overall depth incl. lever & cord gland", "V")
    L.angle((d["FX"], -13, d["FZ"]), 16, -d["LEV_ANG"], 0, f"{d['LEV_ANG']}° lever at rest", size=4.6)
    R = ViewPort(sh.ax, "RIGHT", 240 + X_MAX * s, 96, s); R.draw(M)
    R.cl((d["BX"], 105, -5), (d["BX"], 105, 352)); R.cl((d["GX"], 105, 120), (d["GX"], 105, 320))
    R.label("RIGHT SIDE VIEW  (from +Y)", 330, 50, "scale 1:2.5  -  front (+X) is on the LEFT")
    yb = R.P(0, 0, 0)[1]
    R.hdim((d["GX"], 0, 0), (d["BX"], 0, 0), yb - 7, f"{d['GX'] - d['BX']} boiler-group c/c", "V", size=4.5)
    R.hdim((d["L"], 0, 0), (d["BX"], 0, 0), yb - 13, f"{d['L'] - d['BX']}", "V", size=4.5)
    R.hdim((d["BX"], 0, 0), (0, 0, 0), yb - 13, f"{d['BX']}", "V", size=4.5)
    R.hdim((LEV_END[0], 0, 0), (d["FX"], 0, 0), yb - 19, f"{LEV_END[0] - d['FX']:.0f} fulcrum to handle end", "V", size=4.5)
    R.vdim((d["GX"] + 20, 0, d["BASE_H"]), (d["GX"] + 20, 0, d["SPOUT_Z"]), R.P(d["GX"] + 44, 0, 0)[0], f"{d['SPOUT_Z'] - d['BASE_H']} cup clearance", "V", size=4.5)
    R.vdim((d["SV_X"], 18, 268), (d["SV_X"], 18, 290), R.P(d["SV_X"] - 18, 0, 0)[0], "22", "E", size=4.3)
    R.leader((d["SV_X"], 29, 282), "safety + anti-vacuum valve, cup Ø22 [V/E]", -6, 20)
    R.leader((140, 36, 180), "exhaust tube Ø5 Cu to tray [V/E]", 26, -8)
    R.leader((150, 24, d["STK_Z"]), "steam swivel AF14 [E]", 10, 14)
    R.leader((180, 32, 248), "steam wand Ø8, parks to the front-right [V]", 30, 6)
    R.leader((-4, 50, 30), "cable gland / cord", 8, -14)
    rows = [("Model", "La Pavoni Professional, copper & brass (PB-16 / PRG), v3.1 (2007->) Millennium group"),
            ("Capacity / supply / power", "1.6 L boiler (1.1 L usable) / 230 V 50 Hz / 1000 W [D]"),
            ("Envelope (H x W x D)", f"{d['TOP']} x {d['W_REAR']} x {d['L']} base [V/D];  with handles {d['W_REAR'] / 2 - Y_MIN:.0f} wide, {X_MAX - X_MIN:.0f} deep [V]"),
            ("Mass", "6.4-7.3 kg [D, retailers]"), ("Lever ratio", f"{d['LEV_L']} / 27.6 = 9.9 : 1 [V/E]"),
            ("Pressure", "pressurestat cuts out ~90 kPa (adjustable 50-120 kPa) [D]; gauge 0-250 kPa"),]
    for i, (k, v) in enumerate(rows):
        y = 284 - i * 4.8
        sh.ax.text(228, y, k, fontsize=5.2, va="top", weight="bold"); sh.ax.text(270, y, v, fontsize=5.2, va="top")
    sh.save(pdf)

def sheet_plan(pdf, Sheet):
    sh = Sheet(None, "ORTHOGRAPHIC VIEWS 3/3 - TOP VIEW (PLAN) & BOTTOM VIEW", "1:2.5")
    s = 0.4; d = D; W2 = d["W_REAR"] / 2
    T = ViewPort(sh.ax, "TOP", 30 - X_MIN * s, 214, s); T.draw(M)
    T.cl((d["BX"], -110, 400), (d["BX"], 110, 400)); T.cl((X_MIN - 5, 0, 400), (X_MAX + 5, 0, 400)); T.cl((d["GX"], -110, 400), (d["GX"], 110, 400))
    T.label("TOP VIEW  (plan, from above)", 240, 284, "scale 1:2.5")
    ord_v(T, [((d["L"], -W2, 0), f"-{W2:g} left side"), (PF_END, f"{PF_END[1]:.0f} PF handle"), ((d["STK_X"], d["STK_KNOB_Y"], d["STK_Z"]), f"{d['STK_KNOB_Y']} steam knob end"),
              ((d["SG_X"], d["SG_Y"], 250), f"{d['SG_Y']} sight glass / gauge"), ((d["SW_X"], -101, 30), "-101 switch face"),
              ((d["GX"], -22, d["PORT_Z"]), f"-{d['BOLT_CC'] / 2:g} group bolt"), ((d["L"], 0, 0), "0 CL"), ((d["SV_X"], d["SV_Y"], 290), f"+{d['SV_Y']} safety valve"),
              ((d["GX"], 22, d["PORT_Z"]), f"+{d['BOLT_CC'] / 2:g} group bolt"), ((150, 24, 300), "+24 steam swivel"),
              ((140, 36, 200), "+36 exhaust tube"), ((-5, 45, 30), "+45 cable gland"), ((d["L"], W2, 0), f"+{W2:g} right side")],
          xcol=T.P(X_MAX, 0, 0)[0] + 4, gap=3.0, size=4.3, title="Y")
    T.hdim((0, W2 + 5, 0), (d["L"], W2 + 5, 0), T.P(0, W2 + 5, 0)[1] + 6, f"{d['L']} base [D]", "")
    T.hdim((d["TRAY_X0"], 70, 0), (d["TRAY_X0"] + d["TRAY_L"], 70, 0), T.P(0, 64, 0)[1] + 2, f"{d['TRAY_L']} tray", "V", size=4.5)
    T.vdim((d["TRAY_X0"] + d["TRAY_L"] + 5, -d["TRAY_W"] / 2, 0), (d["TRAY_X0"] + d["TRAY_L"] + 5, d["TRAY_W"] / 2, 0),
           T.P(d["TRAY_X0"] + d["TRAY_L"] + 12, 0, 0)[0], f"{d['TRAY_W']}", "V", size=4.5)
    T.vdim((d["L"] - 3, -d["W_FRONT"] / 2, 0), (d["L"] - 3, d["W_FRONT"] / 2, 0), T.P(d["L"] + 12, 0, 0)[0], f"{d['W_FRONT']} front", "V", size=4.5)
    T.dia((d["BX"], 0, 350), 29, "58 cap knob (6-lobe)", "V", ang=110, ext=12)
    T.dia((d["BX"], 0, 65), 56, "112 foot ring", "V", ang=215, ext=8)
    T.dia((d["GX"], 0, 200), 38, "76 bell", "V", ang=60, ext=26)
    T.angle((d["GX"], 0, 300), 20, 180, d["PF_ANG"], f"{d['PF_ANG'] - 180}° PF handle (locked)", size=4.5)
    T.leader((d["TRAY_X0"] + 120, -40, 65), "76 holes Ø7.2, brass grid on black tray [V]", 22, -24)
    B = ViewPort(sh.ax, "BOTTOM", 30 - X_MIN * s, 100, s); B.draw(M)
    B.cl((X_MIN - 5, 0, -50), (X_MAX + 5, 0, -50)); B.cl((d["BX"], -110, -50), (d["BX"], 110, -50))
    for r_ in (45, 43): B.hidden_circle((d["BX"], 0, -50), r_, "#bbbbbb")
    for k in range(3):
        a = math.radians(90 + 120 * k); B.hidden_circle((d["BX"] + 55 * math.cos(a), 55 * math.sin(a), -50), 3, "#bbbbbb")
    B.label("BOTTOM VIEW  (from below, -Z)", 112, 52, "scale 1:2.5  -  right side (+Y) at the bottom")
    B.hdim((-1, -101, 0), (d["L"] + 1, -101, 0), B.P(0, -101, 0)[1] + 5, f"{d['L'] + 2} sub-base", "V", size=4.5)
    for fx_, fy_ in ((30, -70), (255, -62)):
        B.leader((fx_, fy_, 0), f"foot Ø18 @ X{fx_} Y±{abs(fy_)}", 20 if fx_ > 100 else -16, -12)
    B.leader((d["BX"] + 30, 25, -50), "hidden: element flange Ø90, 3 bolts on PCD 110 [E]", 50, -14)
    sh.ax.text(262, 285, "PLAN NOTES", fontsize=6.5, weight="bold", va="top")
    sh.ax.text(262, 279, "\n".join([
        "Y measured from the boiler/group C/L (-Y = switch / sight-glass side).",
        f"Base: rounded trapezoid, rear {d['W_REAR']} [D], front {d['W_FRONT']} [V], R{d['BASE_R']} [E],",
        "polished brass deep-drawn shell on a black ABS sub-base with 4 feet.",
        f"Boiler axis X{d['BX']}, group axis X{d['GX']} [V/E].",
        "Steam valve runs across the top along Y (knob on -Y side), steam pipe",
        "forward behind the cap to a swivel; wand parks at front-right.",
        f"Portafilter handle shown locked at {d['PF_ANG'] - 180}° to the left."]), fontsize=5.1, va="top", linespacing=1.35)
    sh.save(pdf)

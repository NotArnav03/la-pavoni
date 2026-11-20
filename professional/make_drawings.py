"""Generates the La Pavoni Europiccola (v2.2, 1979) reconstruction drawing set.
A3 landscape sheets, mm coordinates. Output: PDF (all sheets) + PNG + SVG per sheet."""
import math, os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch, Arc
from matplotlib.backends.backend_pdf import PdfPages
from bom import BOM, SEALS

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 420, 297
LW = dict(thick=0.7, thin=0.25, hid=0.3, cen=0.2)
INK = "#111111"; HATCH = "#444444"; DIMC = "#0b3d91"; NOTE = "#7a1f1f"

class Sheet:
    counter = 0; total = 0
    def __init__(self, no, title, scale_note):
        Sheet.counter += 1; no = Sheet.counter
        self.fig = plt.figure(figsize=(W / 25.4, H / 25.4))
        self.ax = self.fig.add_axes([0, 0, 1, 1]); ax = self.ax
        ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")
        self.no, self.title = no, title
        ax.add_patch(Rectangle((10, 10), W - 20, H - 20, fill=False, lw=0.9, ec=INK))
        ax.add_patch(Rectangle((5, 5), W - 10, H - 10, fill=False, lw=0.3, ec=INK))
        for i in range(8):  # zone marks
            x = 10 + (W - 20) * (i + .5) / 8
            ax.text(x, 7.5, str(i + 1), ha="center", va="center", fontsize=5)
            ax.text(x, H - 7.5, str(i + 1), ha="center", va="center", fontsize=5)
        for j, L in enumerate("ABCDEF"):
            y = H - 10 - (H - 20) * (j + .5) / 6
            ax.text(7.5, y, L, ha="center", va="center", fontsize=5); ax.text(W - 7.5, y, L, ha="center", va="center", fontsize=5)
        self.title_block(scale_note)

    def title_block(self, scale_note):
        ax = self.ax; x0, y0, w, h = W - 10 - 190, 10, 190, 42
        ax.add_patch(Rectangle((x0, y0), w, h, fill=True, fc="white", lw=0.8, ec=INK, zorder=5))
        rows = [y0 + 30, y0 + 20, y0 + 10]
        for r in rows: ax.plot([x0, x0 + w], [r, r], lw=0.3, color=INK, zorder=6)
        ax.plot([x0 + 120, x0 + 120], [y0, y0 + 30], lw=0.3, color=INK, zorder=6)
        ax.plot([x0 + 155, x0 + 155], [y0, y0 + 30], lw=0.3, color=INK, zorder=6)
        t = lambda x, y, s, **k: ax.text(x, y, s, zorder=7, **k)
        t(x0 + 2, y0 + 36, "LA PAVONI PROFESSIONAL  COPPER & BRASS  v3.1 (2007->)  -  RECONSTRUCTION DRAWING", fontsize=6.8, weight="bold", va="center")
        t(x0 + 2, y0 + 25, self.title, fontsize=7.5, weight="bold", va="center")
        t(x0 + 2, y0 + 15, "Unofficial reverse-engineered reference. Not a La Pavoni document.", fontsize=5, va="center")
        t(x0 + 2, y0 + 11.5, "Sources: La Pavoni / Parts Guru / Espresso Shop diagrams, F. Ceccarelli, L. Wright, retailer data, product photos.", fontsize=5, va="center")
        t(x0 + 2, y0 + 5, "ALL DIMENSIONS IN mm (SI).  [D] documented  [V] scaled from photos  [E] estimate - VERIFY", fontsize=5.2, va="center", color=NOTE, weight="bold")
        t(x0 + 122, y0 + 25, "SCALE", fontsize=4.5); t(x0 + 122, y0 + 21.5, scale_note, fontsize=6.5, weight="bold")
        t(x0 + 122, y0 + 15, "PROJECTION", fontsize=4.5); t(x0 + 122, y0 + 11.5, "1st angle (ISO E)", fontsize=6)
        t(x0 + 122, y0 + 5, "GEN. TOL: ISO 2768-m", fontsize=5)
        t(x0 + 157, y0 + 25, "SHEET", fontsize=4.5); t(x0 + 157, y0 + 19, f"{self.no} / {Sheet.total}", fontsize=9, weight="bold")
        t(x0 + 157, y0 + 11.5, "DATE 2026-11-19", fontsize=5); t(x0 + 157, y0 + 5, "REV A", fontsize=5.5, weight="bold")

    def note(self, x, y, s, size=5.5, **k):
        self.ax.text(x, y, s, fontsize=size, va="top", ha="left", family="DejaVu Sans", **k)

    def save(self, pdf):
        name = f"sheet{self.no:02d}"
        self.fig.savefig(os.path.join(OUT, name + ".png"), dpi=220)
        self.fig.savefig(os.path.join(OUT, name + ".svg"))
        pdf.savefig(self.fig); plt.close(self.fig)

class View:
    """Draw real-size geometry (mm) at a scale with origin (ox, oy) on the sheet."""
    def __init__(self, sh, ox, oy, s, label=None, lx=None, ly=None):
        self.sh, self.ax, self.ox, self.oy, self.s = sh, sh.ax, ox, oy, s
        if label:
            self.ax.text(lx if lx is not None else ox, ly if ly is not None else oy - 12, label, fontsize=7, weight="bold", ha="center")
    def P(self, x, y): return (self.ox + x * self.s, self.oy + y * self.s)
    def line(self, pts, lw="thick", ls="-", color=INK, z=3):
        xs, ys = zip(*[self.P(*p) for p in pts])
        self.ax.plot(xs, ys, lw=LW.get(lw, lw) if isinstance(lw, str) else lw, ls=ls, color=color, zorder=z, solid_capstyle="round")
    def poly(self, pts, fc="none", hatch=None, lw="thick", z=2, ec=INK, alpha=1):
        self.ax.add_patch(Polygon([self.P(*p) for p in pts], closed=True, fc=fc, ec=ec, lw=LW[lw] if isinstance(lw, str) else lw,
                                  hatch=hatch, zorder=z, alpha=alpha))
    def rect(self, x, y, w, h, **k): self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], **k)
    def sec(self, x, y, w, h, hatch="////", fc="white", **k): self.rect(x, y, w, h, fc=fc, hatch=hatch, **k)
    def circ(self, x, y, r, lw="thick", fc="none", ls="-", z=3, hatch=None):
        self.ax.add_patch(Circle(self.P(x, y), r * self.s, fc=fc, ec=INK, lw=LW[lw], ls=ls, zorder=z, hatch=hatch))
    def arc(self, x, y, r, a0, a1, lw="thick"):
        self.ax.add_patch(Arc(self.P(x, y), 2 * r * self.s, 2 * r * self.s, theta1=a0, theta2=a1, ec=INK, lw=LW[lw], zorder=3))
    def cl(self, p0, p1):  # centre line
        self.line([p0, p1], lw="cen", ls=(0, (8, 2, 1.5, 2)), color="#555555", z=1)
    def hid(self, pts): self.line(pts, lw="hid", ls=(0, (3, 1.5)))
    def text(self, x, y, s, size=5, **k):
        X, Y = self.P(x, y); self.ax.text(X, Y, s, fontsize=size, zorder=8, **k)
    def dim(self, p0, p1, off, txt, tag="", size=5, side=1):
        """Linear dimension between p0 and p1 (real mm), offset 'off' (sheet mm) perpendicular."""
        a, b = self.P(*p0), self.P(*p1)
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * off, dx / L * off
        A, B = (a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny)
        ax = self.ax
        e = 1.2 * (1 if off >= 0 else -1)
        for p, q in ((a, A), (b, B)):
            ax.plot([p[0] + nx * 0.08, q[0] + nx / abs(off) * e if off else q[0]], [p[1] + ny * 0.08, q[1] + ny / abs(off) * e if off else q[1]],
                    lw=0.2, color=DIMC, zorder=7)
        ax.annotate("", xy=A, xytext=B, arrowprops=dict(arrowstyle="<|-|>", lw=0.3, color=DIMC, mutation_scale=4), zorder=7)
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90.01 or ang < -89.99: ang -= 180
        mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
        lab = txt + (f" [{tag}]" if tag else "")
        ax.text(mx + (-dy / L) * 1.3 * (1 if off >= 0 else -1), my + (dx / L) * 1.3 * (1 if off >= 0 else -1), lab, fontsize=size, color=DIMC,
                rotation=ang, ha="center", va="center", zorder=8, bbox=dict(fc="white", ec="none", pad=0.2))
    def dia(self, x, y, r, txt, tag="", ang=45, size=5, ext=8):
        c = self.P(x, y); R = r * self.s; a = math.radians(ang)
        p = (c[0] + R * math.cos(a), c[1] + R * math.sin(a)); q = (p[0] + ext * math.cos(a), p[1] + ext * math.sin(a))
        self.ax.annotate("", xy=p, xytext=q, arrowprops=dict(arrowstyle="-|>", lw=0.3, color=DIMC, mutation_scale=4), zorder=7)
        self.ax.text(q[0] + 0.8, q[1], txt + (f" [{tag}]" if tag else ""), fontsize=size, color=DIMC, va="center", zorder=8,
                     bbox=dict(fc="white", ec="none", pad=0.2))
    def balloon(self, x, y, n, dx=12, dy=8):
        p = self.P(x, y); q = (p[0] + dx, p[1] + dy)
        self.ax.plot([p[0], q[0]], [p[1], q[1]], lw=0.25, color=INK, zorder=9)
        self.ax.add_patch(Circle(p, 0.5, color=INK, zorder=9))
        self.ax.add_patch(Circle(q, 2.6, fc="white", ec=INK, lw=0.4, zorder=9))
        self.ax.text(q[0], q[1], str(n), fontsize=4.6, ha="center", va="center", zorder=10, weight="bold")

def mirror(pts): return [(-x, y) for x, y in pts]

def rounded_trap(rw, fw, L, r, n=12):
    """Plan outline of the base: rear width rw (x=0 end), front width fw (x=L end), corner radius r."""
    pts = []
    corners = [(L - r, fw / 2 - r, 0, 90), (r, rw / 2 - r, 90, 180), (r, -rw / 2 + r, 180, 270), (L - r, -fw / 2 + r, 270, 360)]
    for cx, cy, a0, a1 in corners:
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

# ------------------------------------------------------------------ geometry constants (mm, real)
from views import D as VD
BASE_L, BASE_RW, BASE_FW, BASE_H, BASE_R = VD["L"], VD["W_REAR"], VD["W_FRONT"], VD["BASE_H"], VD["BASE_R"]
BOIL_X = VD["BX"]
GRP_X = VD["GX"]
TRAY_X = VD["TRAY_X0"] + VD["TRAY_L"] / 2

# ================================================================== SHEET 1 : GENERAL ARRANGEMENT
def sheet1(pdf):
    sh = Sheet(1, "GENERAL ARRANGEMENT - SIDE, FRONT & PLAN VIEWS", "1:2")
    s = 0.5
    # ---- side view (looking from the left; boiler rear left, group right)
    v = View(sh, 30, 75, s, "SIDE VIEW (lever at rest)", lx=30 + 135 * s + 20, ly=56)
    v.poly([(0, 3), (BASE_L, 3), (BASE_L, 10), (0, 10)], fc="#222222", lw="thin")                     # rubber cover lip
    v.poly([(4, 10), (BASE_L - 4, 10), (BASE_L - 10, BASE_H - 6), (BASE_L - 22, BASE_H), (22, BASE_H), (8, BASE_H - 8)], fc="#d9efe6")
    v.rect(0, 0, BASE_L, 3, fc="#222222", lw="thin")
    v.rect(TRAY_X - 62, BASE_H - 1, 124, 1.5, fc="#bbbbbb", lw="thin")                                 # grid
    # boiler
    v.rect(BOIL_X - SH_OD / 2, SH_Z0, SH_OD, SH_Z1 - SH_Z0, fc="#eeeeee")
    v.poly([(BOIL_X - 44, 262), (BOIL_X + 44, 262), (BOIL_X + 28, 285), (BOIL_X - 28, 285)], fc="#eeeeee")
    v.rect(BOIL_X - 28, 285, 56, 5, fc="#eeeeee")
    v.poly([(BOIL_X - 15, 290), (BOIL_X + 15, 290), (BOIL_X + 20, 305), (BOIL_X + 28, 306), (BOIL_X + 28, 320), (BOIL_X - 28, 320),
            (BOIL_X - 28, 306), (BOIL_X - 20, 305)], fc="#c9a67a")
    v.cl((BOIL_X, 50), (BOIL_X, 328))
    # sight glass (front-left of boiler - shown on rear side here)
    v.rect(BOIL_X - 44 - 18, 75, 18, 18, fc="#eeeeee"); v.rect(BOIL_X - 44 - 18, 228, 18, 18, fc="#eeeeee")
    v.rect(BOIL_X - 44 - 17, 93, 16, 135, fc="#e8f4fb"); v.rect(BOIL_X - 44 - 12, 100, 6, 120, fc="#ffffff", lw="thin")
    # steam valve + wand (towards rear-left)
    v.rect(BOIL_X - 28 - 22, 272, 22, 12, fc="#eeeeee"); v.rect(BOIL_X - 28 - 50, 270, 28, 16, fc="#c9a67a")
    v.line([(BOIL_X - 70, 272), (BOIL_X - 74, 250), (BOIL_X - 76, 120), (BOIL_X - 70, 108)], lw=2.0 * s * 4, color="#888888")
    # group
    gx = GRP_X
    v.rect(BOIL_X + 44, GRP_Z - 14, 22, 28, fc="#eeeeee")
    v.poly([(gx - 36, 150), (gx + 36, 150), (gx + 36, 165), (gx + 26, 175), (gx + 22, 245), (gx - 22, 245), (gx - 26, 175), (gx - 36, 165)], fc="#eeeeee")
    v.rect(gx - 9, 245, 18, 52, fc="#eeeeee"); v.rect(gx - 6, 297, 12, 10, fc="#dddddd"); v.circ(gx, 311, 6, fc="#dddddd")
    v.cl((gx, 100), (gx, 320))
    # portafilter + spout
    v.poly([(gx - 31, 150), (gx + 31, 150), (gx + 28, 128), (gx - 28, 128)], fc="#e2e2e2")
    v.poly([(gx - 8, 128), (gx + 8, 128), (gx + 6, 116), (gx - 6, 116)], fc="#e2e2e2")
    v.line([(gx - 6, 116), (gx - 16, 104)]); v.line([(gx + 6, 116), (gx + 16, 104)])
    v.poly([(gx + 31, 142), (gx + 60, 136), (gx + 160, 128), (gx + 162, 116), (gx + 60, 128), (gx + 31, 132)], fc="#c9a67a")
    # lever (rest position, sloping down to the front)
    piv = (gx + 4, 293)
    v.poly([(piv[0] - 10, piv[1] + 8), (piv[0] + 60, piv[1] - 6), (piv[0] + 60, piv[1] - 20), (piv[0] - 10, piv[1] - 6)], fc="#e8e8e8")
    v.line([(piv[0] + 60, piv[1] - 13), (piv[0] + 210, piv[1] - 60)], lw=14 * s * 0.7, color="#999999")
    v.poly([(piv[0] + 205, piv[1] - 52), (piv[0] + 300, piv[1] - 82), (piv[0] + 296, piv[1] - 96), (piv[0] + 201, piv[1] - 66)], fc="#c9a67a")
    v.circ(*piv, 3.5); v.circ(piv[0] + 25, piv[1] - 6, 3.5)
    # dims
    v.dim((0, 0), (BASE_L, 0), -9, "270 base length", "D")
    v.dim((0, 0), (0, 320), 14, "320 overall height", "D")
    v.dim((BASE_L, 0), (BASE_L, BASE_H), 10, f"{BASE_H}", "V")
    v.dim((BOIL_X - 44, SH_Z1 + 2), (BOIL_X + 44, SH_Z1 + 2), 0, "OD 88 shell", "V")
    v.dim((BOIL_X + 70, BASE_H), (BOIL_X + 70, 104), 0, "~44 cup clearance", "V")
    v.dim((BOIL_X, 0), (gx, 0), -5, f"{gx - BOIL_X:.0f}", "V")
    v.dim((0, 0), (BOIL_X, 0), -5, f"{BOIL_X}", "V")
    v.text(piv[0] + 120, piv[1] - 18, "Lever ~300 from fulcrum; overhang beyond\nbase is excluded from the 270 dimension [V/E]", size=4.6, color=NOTE)
    # ---- front view (looking at group)
    f = View(sh, 255, 75, s, "FRONT VIEW", lx=200, ly=56)
    f.poly([(-BASE_FW / 2, 3), (BASE_FW / 2, 3), (BASE_FW / 2, 10), (-BASE_FW / 2, 10)], fc="#222222", lw="thin")
    f.poly([(-BASE_FW / 2 + 4, 10), (BASE_FW / 2 - 4, 10), (BASE_FW / 2 - 12, BASE_H), (-BASE_FW / 2 + 12, BASE_H)], fc="#d9efe6")
    f.rect(-BASE_RW / 2, 0, BASE_RW, 3, fc="#222222", lw="thin")
    f.hid([(-BASE_RW / 2, 3), (-BASE_RW / 2 + 6, BASE_H - 6)]); f.hid([(BASE_RW / 2, 3), (BASE_RW / 2 - 6, BASE_H - 6)])
    f.rect(-44, SH_Z0, 88, 200, fc="#f2f2f2", lw="thin")
    f.poly([(-36, 150), (36, 150), (36, 165), (26, 175), (22, 245), (-22, 245), (-26, 175), (-36, 165)], fc="#eeeeee")
    f.rect(-9, 245, 18, 52, fc="#eeeeee"); f.rect(-12, 285, 24, 22, fc="#e8e8e8"); f.circ(0, 311, 6, fc="#dddddd")
    f.poly([(-31, 150), (31, 150), (28, 128), (-28, 128)], fc="#e2e2e2")
    f.poly([(-8, 128), (8, 128), (6, 116), (-6, 116)], fc="#e2e2e2"); f.line([(-6, 116), (-20, 104)]); f.line([(6, 116), (20, 104)])
    f.poly([(-15, 290), (15, 290), (20, 305), (28, 306), (28, 320), (-28, 320), (-28, 306), (-20, 305)], fc="#c9a67a")
    f.rect(-14, 22, 28, 22, fc="#ffffff"); f.rect(-11, 33, 22, 9, fc="#d33"); f.rect(-11, 24, 22, 8, fc="#f3eedd")
    f.cl((0, -8), (0, 328))
    f.dim((-BASE_RW / 2, 0), (BASE_RW / 2, 0), -9, "180 base width (rear)", "D")
    f.dim((-36, 150), (36, 150), -40, "OD 72 group", "D")
    f.text(16, 33, "65 switch I / II", size=4.6)
    # ---- plan view
    p = View(sh, 318, 245, 0.32, "PLAN VIEW (1:3)", lx=318 + 135 * 0.32, ly=207)
    p.poly([(x, y) for x, y in rounded_trap(BASE_RW, BASE_FW, BASE_L, BASE_R)], fc="#d9efe6")
    p.poly([(x + TRAY_X - 65, y) for x, y in rounded_trap(112, 104, 130, 28)], fc="#bbbbbb")
    p.circ(BOIL_X, 0, 44, fc="#eeeeee"); p.circ(BOIL_X, 0, 28, fc="#c9a67a"); p.circ(GRP_X, 0, 36, fc="#eeeeee", lw="thin")
    p.cl((-10, 0), (BASE_L + 10, 0))
    p.dim((0, -BASE_RW / 2), (BASE_L, -BASE_RW / 2), -6, "270", "D")
    p.dim((BASE_L, -BASE_FW / 2), (BASE_L, BASE_FW / 2), 6, "~160", "V")
    # ---- data table
    rows = [("Model", "Europiccola, 2nd series v2.2 (1978-83)"), ("Production stamp", "'2 79' under base (Feb 1979)"),
            ("Boiler capacity", "0.8 l [D]"), ("Supply", "220 V 50 Hz [D]"), ("Heating", "200 W (I) + 800 W (II) [D]"),
            ("Overall H x W x D", "320 x 180 x 270 mm [D]"), ("Mass (dry)", "5.5 kg [D]"), ("Group", "pre-millennium, 2-bolt, no sleeve"),
            ("Basket", "49 mm [D]"), ("Boiler pressure", "~0.8-1.0 bar working (no pressurestat) [E]"),
            ("Safety valve", "ball/spring, M12, ~1.3-1.5 bar [E]"), ("Finish", "Cu/Ni/Cr plated brass; base painted steel")]
    x0, y0 = 312, 196
    sh.ax.text(x0, y0, "MACHINE DATA", fontsize=7, weight="bold", va="top")
    for i, (k, val) in enumerate(rows):
        y = y0 - 6 - i * 4.6
        sh.ax.text(x0, y, k, fontsize=5.3, va="top"); sh.ax.text(x0 + 30, y, val, fontsize=5.3, va="top")
    sh.save(pdf)

# ================================================================== SHEET 2 : BOILER ASSEMBLY SECTION
def sheet2(pdf):
    sh = Sheet(4, "BOILER ASSEMBLY - SECTION A-A (through boiler axis)", "1:1.25")
    s = 0.72
    v = View(sh, 130, 42, s)
    R, t = SH_OD / 2, SH_T
    # base sheet (section) & rubber
    v.sec(-110, 59, 110 - 41, 1.2, hatch=None, fc="#555555", lw="thin"); v.sec(41, 59, 70, 1.2, hatch=None, fc="#555555", lw="thin")
    v.poly([(-110, 59), (-104, 8), (-100, 8)], fc="none", lw="thin"); v.line([(-110, 59.6), (-104, 8)], lw="thin")
    v.rect(-112, 0, 224, 3, fc="#222222", lw="thin"); v.text(-108, 4, "63 rubber cover", size=4.6)
    # gaskets
    v.sec(-46.5, 60.2, 6.5, 1.8, hatch="xxxx", fc="#ddd"); v.sec(40, 60.2, 6.5, 1.8, hatch="xxxx", fc="#ddd")
    v.sec(-46.5, 57, 6.5, 2, hatch="xxxx", fc="#ddd"); v.sec(40, 57, 6.5, 2, hatch="xxxx", fc="#ddd")
    # shell
    for sgn in (-1, 1):
        v.sec(sgn * R - (t if sgn > 0 else 0), SH_Z0, t, SH_Z1 - SH_Z0, hatch="////", fc="#f4e3b5")
    # bottom threaded ring
    for sgn in (-1, 1):
        x_in, x_out = 34, 40
        pts = [(sgn * x_in, 42), (sgn * x_out, 42), (sgn * x_out, 62), (sgn * (R - t), 62), (sgn * (R - t), 70), (sgn * x_in, 70)]
        v.poly(pts, fc="#f4e3b5", hatch="\\\\\\\\")
        for k in range(9): v.line([(sgn * x_out, 44 + k * 2), (sgn * (x_out + 0.8), 45 + k * 2)], lw="thin")
    # ring nut
    for sgn in (-1, 1):
        v.poly([(sgn * 40, 45), (sgn * 49, 45), (sgn * 49, 57), (sgn * 40, 57)], fc="#f4e3b5", hatch="////")
    v.rect(49, 45, 8, 12, fc="#f4e3b5", lw="thin"); v.rect(-57, 45, 8, 12, fc="#f4e3b5", lw="thin")   # ears beyond
    # element gasket + flange
    v.sec(-41, 40, 7, 2, hatch="xxxx", fc="#ddd"); v.sec(34, 40, 7, 2, hatch="xxxx", fc="#ddd")
    v.poly([(-42, 32), (42, 32), (42, 40), (-42, 40)], fc="#f4e3b5", hatch="////")
    v.rect(42, 32, 13, 8, fc="#f4e3b5", lw="thin"); v.rect(-55, 32, 13, 8, fc="#f4e3b5", lw="thin")
    # element screws (M6 x 16)
    for sgn in (-1, 1):
        v.rect(sgn * 52 - 3, 32, 6, 22, fc="#cccccc", lw="thin"); v.rect(sgn * 52 - 5, 26, 10, 6, fc="#cccccc", lw="thin")
    # element coil (sectioned tubes)
    for i in range(7):
        z = 50 + i * 14
        for xx in (-30 + (i % 2) * 4, 22 - (i % 2) * 4):
            v.circ(xx + 4, z, 4, fc="#d9a066")
    v.line([(-26, 40), (-26, 50)], lw=2.5); v.line([(26, 40), (26, 50)], lw=2.5); v.line([(-8, 40), (-8, 50)], lw=2.5)
    # terminals
    for xx in (-22, -6, 10, 24):
        v.rect(xx - 3, 18, 6, 14, fc="#fafafa", lw="thin"); v.rect(xx - 1, 10, 2, 8, fc="#bbb", lw="thin")
    # top casting
    for sgn in (-1, 1):
        v.poly([(sgn * R, 262), (sgn * (R - t), 262), (sgn * (NECK_OD / 2 - 3), 284), (sgn * (NECK_OD / 2 - 3), 292), (sgn * NECK_OD / 2, 292),
                (sgn * NECK_OD / 2, 285), (sgn * R, 266)], fc="#f4e3b5", hatch="\\\\\\\\")
    # cap insert + gasket + knob
    v.poly([(-20, 270), (20, 270), (20, 292), (23, 292), (23, 295), (-23, 295), (-23, 292), (-20, 292)], fc="#e6c98f", hatch="....")
    v.sec(-23, 295, 10, 2.5, hatch="xxxx", fc="#ddd"); v.sec(13, 295, 10, 2.5, hatch="xxxx", fc="#ddd")
    v.poly([(-16, 297.5), (16, 297.5), (20, 306), (28, 307), (28, 320), (-28, 320), (-28, 307), (-20, 306)], fc="#c9a67a", hatch="----")
    v.rect(-4, 284, 8, 30, fc="#cccccc", lw="thin")
    # safety valve (right shoulder) & steam valve boss (left)
    v.poly([(30, 278), (36, 278), (36, 292), (30, 292)], fc="#f4e3b5", hatch="////")
    v.rect(29, 292, 9, 8, fc="#dddddd"); v.circ(33.5, 293, 3, fc="#999"); v.line([(31, 296), (36, 299), (31, 302), (36, 305)], lw="thin")
    v.rect(25, 300, 18, 22, fc="#eeeeee"); v.line([(43, 304), (55, 300), (60, 260)], lw=1.2)
    v.poly([(-R, 270), (-R - 14, 270), (-R - 14, 284), (-R + 6, 284), (-NECK_OD / 2 + 3, 278)], fc="#f4e3b5", hatch="////")
    v.rect(-R - 40, 268, 26, 18, fc="#eeeeee")
    # group port (right, behind section plane -> shown as flange pad)
    v.poly([(R, GRP_Z - 16), (R + 20, GRP_Z - 16), (R + 20, GRP_Z + 16), (R, GRP_Z + 16)], fc="#f4e3b5", hatch="////")
    v.rect(R, GRP_Z - 4, 20, 8, fc="white", lw="thin")
    v.line([(R + 4, GRP_Z), (R - 10, GRP_Z), (R - 18, GRP_Z - 8), (R - 18, GRP_Z - 85)], lw=2.6)
    v.rect(R + 20, GRP_Z - 30, 6, 60, fc="#eeeeee", lw="thin"); v.text(R + 28, GRP_Z + 22, "35 group (sheet 3)", size=4.6)
    # sight glass bosses (left)
    for z in (85, 235):
        v.rect(-R - 18, z - 9, 18, 18, fc="#eeeeee")
        v.rect(-R - 1, z - 5, 10, 10, fc="#cccccc", lw="thin")      # spigot + inner nut
        v.rect(-R + 1.5, z - 8.5, 6, 17, fc="#f4e3b5", hatch="////", lw="thin")
    v.rect(-R - 14, 94, 10, 132, fc="#e8f4fb", lw="thin"); v.rect(-R - 12, 98, 6, 124, fc="white", lw="thin")
    # water level marks
    v.line([(-R + t, 205), (R - t, 205)], lw="thin", ls=(0, (6, 2)), color="#2a6fb0"); v.text(-38, 207, "MAX (0.8 l) [E]", size=4.4, color="#2a6fb0")
    v.line([(-R + t, 140), (R - t, 140)], lw="thin", ls=(0, (6, 2)), color="#2a6fb0"); v.text(-38, 142, "MIN - keep above element & L-tube inlet", size=4.4, color="#2a6fb0")
    v.cl((0, 0), (0, 330))
    # balloons
    for (x, y, n, dx, dy) in [(R - 0.7, 180, 1, 30, 0), (-35, 285, 2, -20, 26), (37, 55, 3, 28, -4), (45, 51, 4, 25, -12), (43, 61, 5, 30, 2),
                              (0, 90, 6, 55, -10), (-37, 41, 7, -40, -2), (-52, 28, 8, -30, -6), (0, 280, 9, 30, 8), (-18, 296, 10, -30, 8),
                              (-24, 315, 11, -30, 4), (0, 310, 12, 12, 10), (33, 285, 13, 40, -6), (33, 293, 14, 40, 0), (34, 300, 15, 40, 4),
                              (34, 315, 16, 35, 8), (-R - 9, 160, 17, -25, 0), (-R - 16, 140, 18, -25, -6), (-R - 9, 235, 19, -30, 6),
                              (-R + 4, 85, 21, -30, -8), (-R - 30, 277, 25, -22, -4), (R - 18, 160, 45, 30, -12), (-6, 22, 6, -30, -14)]:
        v.balloon(x, y, n, dx, dy)
    # dims
    v.dim((-R + t, 120), (R - t, 120), 0, "OD 88 shell", "V")
    v.dim((-R, SH_Z0), (-R, SH_Z1), 46, "200 shell height", "V")
    v.dim((-40, 42), (40, 42), -18, "M80x1.25 boiler neck", "D/E")
    v.dim((-42, 32), (42, 32), -27, "OD 84 element flange", "D")
    v.dim((-NECK_OD / 2, 330), (NECK_OD / 2, 330), 0, "OD 56 neck", "V/E")
    v.dim((R + 20, 3), (R + 20, GRP_Z), -32, f"{GRP_Z} port centre", "V")
    v.dim((-R - 18, 85), (-R - 18, 235), 10, "150 c/c sight glass", "E")
    # detail: shell wall + notes
    sh.note(250, 285, "NOTES - BOILER", 7, weight="bold")
    sh.note(250, 279, "\n".join([
        "1. Shell: brass tube CuZn37, wall 1.5 [E]. Top casting and bottom ring",
        "   brazed (Ag-braze), whole assembly Cu/Ni/Cr plated outside.",
        "2. Boiler neck thread M80x1.25 fine pitch - La Pavoni used 1.25 pitch on",
        "   1978-1996 boilers, 1.5 coarse from 1996. Do NOT mix ring nuts [D].",
        "3. Base is clamped between upper and lower gasket (93x80x2 AFM34) by",
        "   ring nut 4. Ring nut needs a 3-lug or oil-filter type spanner.",
        "4. Element flange seals on the end face of the neck with flat gasket",
        "   82x68x2 and is drawn up by 3 screws into the ring-nut ears.",
        "   Tighten evenly in 3 passes, ~4 Nm [E]. Thread: M6 per fixing-ring",
        "   data; later diagrams list M5x12 - check before ordering.",
        "5. Original 1979 fibre gaskets may contain asbestos: wet them, do not",
        "   sand or blow, dispose of them as hazardous waste.",
        "6. Fill: max 0.8 l, never above the upper sight-glass mark; leave a",
        "   steam space above the L-tube inlet.",
        "7. Threads sealed with food-grade anaerobic sealant (video: green),",
        "   sight-glass spigots with PTFE washers.",
        "8. No pressurestat on v2.2: pressure is held by switching I (200 W).",
        "9. Hatching: //// brass, xxxx gasket, ---- knob, .... insert.",
    ]), 5.3)
    sh.note(250, 182, "DETAIL - THREAD DATA (verify with thread gauge)", 6.5, weight="bold")
    data = [("Boiler neck / ring nut", "M80 x 1.25", "D pitch / E dia."), ("Filler (cap insert)", "~M40 x 1.5", "E"),
            ("Safety valve boss", "M12 (x1.5)", "D/E"), ("Steam valve boss", "12 mm", "D"), ("Sight-glass spigots", "M12 x 1", "E"),
            ("Group bolts", "M6 x 1.0", "D/V"), ("Element screws", "M6 (or M5)", "D")]
    for i, (a, b, c) in enumerate(data):
        y = 175 - i * 4.6
        sh.ax.text(250, y, a, fontsize=5.3, va="top"); sh.ax.text(305, y, b, fontsize=5.3, va="top", weight="bold"); sh.ax.text(340, y, c, fontsize=5.3, va="top")
    sh.save(pdf)

# ================================================================== SHEET 3 : GROUP, PISTON, LEVER
def sheet3(pdf):
    sh = Sheet(5, "BREW GROUP, PISTON & LEVER - SECTION B-B", "1:1")
    v = View(sh, 120, 82, 1.0)
    B = 22  # bore radius
    # group body section
    for sgn in (-1, 1):
        v.poly([(sgn * B, 0), (sgn * 36, 0), (sgn * 36, 15), (sgn * 27, 25), (sgn * 23, 95), (sgn * 11, 95), (sgn * 11, 88), (sgn * B, 88)],
               fc="#f4e3b5", hatch="////")
    # bayonet lugs seat / gasket / screen
    v.sec(-28.85, 0, 5.35, 5.3, hatch="xxxx", fc="#ddd"); v.sec(23.5, 0, 5.35, 5.3, hatch="xxxx", fc="#ddd")
    v.rect(-26, 5.3, 52, 1, fc="#cccccc", lw="thin"); v.text(-24, 8, "43 shower screen d52", size=4.4)
    # cylinder & piston (piston drawn at bottom-of-stroke region)
    pz = 22
    v.poly([(-21.9, pz), (21.9, pz), (21.9, pz + 30), (-21.9, pz + 30)], fc="#e6c98f", hatch="\\\\\\\\")
    for g in (pz + 5, pz + 18):
        v.rect(-21.9, g, 4, 5.5, fc="white", lw="thin"); v.rect(17.9, g, 4, 5.5, fc="white", lw="thin")
        v.poly([(-22, g), (-18, g), (-18, g + 5.5), (-22, g + 5.5)], fc="#333", lw="thin"); v.poly([(18, g), (22, g), (22, g + 5.5), (18, g + 5.5)], fc="#333", lw="thin")
    v.rect(-5, pz + 30, 10, 75, fc="#dddddd"); v.circ(0, pz + 30 + 66, 3, fc="white")
    v.rect(-4, pz + 22, 8, 8, fc="white", lw="thin"); v.text(6, pz + 25, "M8", size=4.4)
    # rod seal + washer + circlip at top
    v.sec(-10, 82, 5, 4, hatch="....", fc="white"); v.sec(5, 82, 5, 4, hatch="....", fc="white")
    v.sec(-10, 86, 5, 1, hatch=None, fc="#888"); v.sec(5, 86, 5, 1, hatch=None, fc="#888")
    v.rect(-11, 87, 1.2, 1, fc="#222", lw="thin"); v.rect(9.8, 87, 1.2, 1, fc="#222", lw="thin")
    # yoke above (side profile)
    v.poly([(-11, 95), (11, 95), (9, 150), (5, 156), (-5, 156), (-9, 150)], fc="#eeeeee")
    v.circ(0, 142, 3, fc="white"); v.rect(-4, 156, 8, 14, fc="#cccccc", lw="thin")
    v.rect(-6.5, 166, 13, 5, fc="#e8e8e8", lw="thin"); v.poly([(-6.5, 171), (6.5, 171), (5, 178), (0, 180), (-5, 178)], fc="#e8e8e8", lw="thin")
    # boiler flange (to the left), port + L tube + bolts
    v.poly([(-36, 50), (-58, 50), (-58, 82), (-36, 82)], fc="#f4e3b5", hatch="////")
    v.rect(-58, 62, 22, 8, fc="white", lw="thin"); v.line([(-36, 66), (-B, 66)], lw="thin")
    v.circ(-58, 66, 3.6, fc="#ddd", lw="thin")
    v.rect(-62, 50, 4, 32, fc="#ddd", hatch="xxxx", lw="thin")
    for zz in (47, 85):
        v.rect(-80, zz - 3, 22, 6, fc="#cccccc", lw="thin"); v.rect(-86, zz - 5, 6, 10, fc="#bbbbbb", lw="thin")
    v.line([(-62, 66), (-78, 66), (-86, 58), (-86, -20)], lw=2.0)
    # portafilter section below
    for sgn in (-1, 1):
        v.poly([(sgn * 26, 0), (sgn * 31, 0), (sgn * 31, -4), (sgn * 29, -26), (sgn * 9, -30), (sgn * 6, -30), (sgn * 6, -26), (sgn * 26, -24)],
               fc="#f4e3b5", hatch="////")
    v.poly([(-24.5, -1), (24.5, -1), (22, -24), (-22, -24)], fc="none", lw="thin")
    v.line([(-24.5, -1), (-22, -24), (22, -24), (24.5, -1)], lw=0.5)
    v.poly([(-6, -30), (6, -30), (5, -42), (-5, -42)], fc="#e6c98f", hatch="////"); v.line([(-5, -42), (-18, -56)], lw=1.6); v.line([(5, -42), (18, -56)], lw=1.6)
    v.poly([(31, -6), (55, -10), (55, -20), (31, -16)], fc="#e2e2e2"); v.rect(55, -19, 50, 10, fc="#c9a67a", hatch="----")
    v.cl((0, -60), (0, 185))
    for (x, y, n, dx, dy) in [(30, 40, 35, 25, 10), (0, pz + 12, 36, 32, -14), (20, pz + 8, 37, 25, -2), (0, 75, 38, 25, 18),
                              (8, 84, 39, 22, 12), (8, 86.5, 40, 22, 17), (10.4, 87.5, 41, 18, 24), (26, 2.6, 42, 22, -6), (-20, 5.8, 43, -15, -16),
                              (-60, 74, 44, -18, 16), (-86, 20, 45, 12, -6), (-72, 85, 46, -10, 12), (0, 169, 47, 18, 4), (0, 176, 48, 18, 6),
                              (28, -12, 54, 22, -10), (0, -12, 56, 26, 0), (-14, -50, 55, -16, -6), (85, -14, 60, 8, -10), (0, 142, 50, -24, 10)]:
        v.balloon(x, y, n, dx, dy)
    v.dim((-B, 70), (B, 70), 0, "bore 44 H8", "D")
    v.dim((-36, 0), (36, 0), -6, "OD 72", "D")
    v.dim((-28.85, 5.3), (28.85, 5.3), -14, "gasket 57.7 x 47 x 5.3", "D")
    v.dim((-26, -1), (26, -1), -36, "basket 49 / PF bore 52", "D")
    v.dim((-58, 47), (-58, 85), -26, "38 bolt c/c", "V")
    v.dim((5, pz + 30), (5, pz + 105), 16, "rod d10 x 75 exposed", "E")
    v.dim((-21.9, pz), (-21.9, pz + 30), -10, "30", "E")
    v.text(-20, pz - 3, "stroke ~35 [E] - piston uncovers inlet port at top", size=4.5, color=NOTE)
    # ---- lever linkage side view (right)
    L = View(sh, 235, 240, 0.5, "LEVER & LINKAGE (1:2)", lx=235 + 60, ly=205)
    L.poly([(-10, -8), (40, -16), (44, -6), (-6, 6)], fc="#e8e8e8"); L.circ(0, 0, 3.5, fc="white"); L.circ(25, -9, 3.5, fc="white")
    L.line([(42, -11), (230, -68)], lw=14 * 0.5 * 0.72, color="#999999"); L.poly([(225, -60), (330, -92), (326, -106), (221, -74)], fc="#c9a67a", hatch="----")
    L.rect(-6, -40, 12, 40, fc="#eeeeee"); L.rect(20, -60, 10, 52, fc="#dddddd", lw="thin")
    L.balloon(0, 0, 50, -14, 12); L.balloon(25, -9, 52, 6, 16); L.balloon(120, -38, 49, 6, 14); L.balloon(280, -84, 53, 6, 14); L.balloon(4, 3, 51, -16, -14)
    L.dim((0, 0), (25, -9), 10, "26.6 link", "V/E"); L.dim((0, 0), (300, -90), -8, "~313 effective arm", "V/E")
    L.text(60, 10, "Lever ratio ~ 313 / 26.6 = 11.8 : 1 [E]\n15 kg at handle ~ 175 kgf on piston\n~ 11 bar over 44 mm bore (theory) [E]", size=5, color=NOTE)
    sh.note(235, 150, "NOTES - GROUP", 7, weight="bold")
    sh.note(235, 144, "\n".join([
        "1. Group is a hot-stamped brass body, plated. Mounted to boiler pad by 2 x M6x20",
        "   A2-70 hex bolts (AF10), sealed by item 44; L-tube 45 dips into the boiler.",
        "2. Piston seals: lips face DOWN (towards coffee). Grease with food-grade silicone",
        "   (Molykote 111). Original seals in video were hard and brittle black NBR.",
        "3. Group gasket and screen: push into the group, then seat with the portafilter.",
        "4. Pins d6 with E-clips DIN 6799 size 5; tap pins in, do not hammer the clips.",
        "5. Top cap: M8 lock nut + acorn nut on yoke stud, food-grade sealant.",
    ]), 5.3)
    sh.save(pdf)

# ================================================================== SHEET 4 : STEAM VALVE, SIGHT GLASS, CAP, SAFETY VALVE
def sheet4(pdf):
    sh = Sheet(6, "DETAILS - STEAM VALVE & WAND, SIGHT GLASS, BOILER CAP, SAFETY VALVE", "1:1 / 2:1")
    # steam valve (1:1.25)
    v = View(sh, 40, 215, 1.25, "DETAIL C - STEAM VALVE (1.25:1)", lx=90, ly=180)
    v.poly([(0, -8), (34, -8), (34, 8), (0, 8)], fc="#f4e3b5", hatch="////")            # body
    v.rect(-12, -4, 12, 8, fc="#f4e3b5", hatch="\\\\\\\\"); v.text(-12, 6, "12 mm to boiler", size=4.4)
    v.rect(34, -7, 14, 14, fc="#e6c98f", hatch="////")                                  # packing nut
    v.rect(10, -3, 62, 6, fc="#dddddd")                                                 # stem
    v.poly([(10, -3), (4, 0), (10, 3)], fc="#dddddd")
    v.sec(34, -6, 1, 12, hatch=None, fc="#888"); v.sec(28, -6, 6, 12, hatch="....", fc="white"); v.sec(27, -6, 1, 12, hatch=None, fc="#888")
    v.poly([(72, -10), (94, -12), (94, 12), (72, 10)], fc="#c9a67a", hatch="----"); v.circ(80, 0, 1.25, fc="white")
    v.rect(14, -20, 12, 12, fc="#e6c98f", hatch="////"); v.line([(20, -20), (20, -60)], lw=8 * 1.25 * 0.72, color="#999999")
    for (x, y, n, dx, dy) in [(17, 6, 25, 0, 14), (41, 5, 27, 6, 14), (40, -2, 26, 10, -16), (31, 4, 28, -4, 16), (27.5, -5, 29, 4, -18),
                              (85, -8, 30, 6, -14), (80, 0, 31, 12, -14), (20, -14, 33, -16, -6), (20, -45, 32, -16, 0)]:
        v.balloon(x, y, n, dx, dy)
    v.text(52, 4, "d6 stem [V]", size=4.4); v.dim((34, 7), (48, 7), 8, "AF14", "D")
    # sight glass (1:1)
    g = View(sh, 175, 120, 0.75, "DETAIL D - SIGHT GLASS (1:1.33)", lx=175, ly=104)
    for z in (0, 125):
        g.rect(-9, z - 9, 18, 18, fc="#f4e3b5", hatch="////"); g.rect(9, z - 6, 14, 12, fc="#e6c98f", hatch="\\\\\\\\")
        g.rect(23, z - 6, 2, 12, fc="#ccc", lw="thin"); g.rect(25, z - 8.5, 8, 17, fc="#e6c98f", hatch="////")
    for z0, z1 in ((9, 20), (105, 116)):
        g.rect(-8.5, z0, 17, z1 - z0, fc="#e6c98f", hatch="////")
    g.rect(-6, 9.5, 12, 106, fc="#e8f4fb"); g.rect(-4.5, 9.5, 9, 106, fc="white", lw="thin")
    g.rect(-8, 20, 16, 85, fc="none", lw="thin"); g.rect(-3, 27, 6, 72, fc="none", lw="hid")
    g.rect(-4, 134, 8, 6, fc="#e6c98f", lw="thin")
    for (x, y, n, dx, dy) in [(0, 62, 17, -22, 0), (7.5, 85, 18, 18, 0), (-8, 125, 19, -20, 6), (0, 110, 20, -24, -4), (30, 125, 21, 10, 10),
                              (0, 21, 22, -24, -10), (23.5, 0, 23, 10, -12), (0, 137, 24, 14, 10)]:
        g.balloon(x, y, n, dx, dy)
    g.dim((-6, 9.5), (-6, 115.5), -16, "glass L 106", "D"); g.dim((-6, 62), (6, 62), 0, "OD12", "D/E")
    g.dim((-9, 0), (-9, 125), -30, "125 c/c (Z113 / Z238)", "V")
    # boiler cap (1:1)
    c = View(sh, 285, 215, 1.0, "DETAIL E - BOILER CAP (1:1)", lx=285, ly=180)
    c.poly([(-20, -22), (20, -22), (20, 0), (23, 0), (23, 3), (-23, 3), (-23, 0), (-20, 0)], fc="#e6c98f", hatch="////")
    for k in range(10): c.line([(20, -21 + k * 2), (21, -20 + k * 2)], lw="thin"); c.line([(-20, -21 + k * 2), (-21, -20 + k * 2)], lw="thin")
    c.sec(-22, 3, 6, 3, hatch="xxxx", fc="#ddd"); c.sec(16, 3, 6, 3, hatch="xxxx", fc="#ddd")
    c.poly([(-16, 6), (16, 6), (20, 14), (28, 15), (28, 30), (-28, 30), (-28, 15), (-20, 14)], fc="#c9a67a", hatch="----")
    c.rect(-4, -8, 8, 30, fc="#cccccc")
    for (x, y, n, dx, dy) in [(15, -10, 9, 18, -6), (19, 4.5, 10, 16, 6), (24, 24, 11, 10, 8), (0, 10, 12, -22, 14)]:
        c.balloon(x, y, n, dx, dy)
    c.dim((-20, -22), (20, -22), -8, "~M38x1.5", "E"); c.dim((-28, 30), (28, 30), 6, "Ø58 lobes", "V"); c.dim((30, -22), (30, 30), 8, "52", "V")
    # safety valve (2:1)
    sv = View(sh, 370, 205, 2.0, "DETAIL F - SAFETY VALVE (2:1)", lx=370, ly=180)
    sv.poly([(-6, -10), (6, -10), (6, 0), (-6, 0)], fc="#e6c98f", hatch="////"); sv.text(7, -8, "M12", size=4.4)
    sv.poly([(-7, 0), (7, 0), (7, 8), (-7, 8)], fc="#e6c98f", hatch="////"); sv.rect(-2, -10, 4, 13, fc="white", lw="thin")
    sv.circ(0, 4.5, 3, fc="#999"); sv.line([(-2.5, 7.5), (2.5, 9.5), (-2.5, 11.5), (2.5, 13.5), (-2.5, 15.5), (2.5, 17.5)], lw="thin")
    sv.poly([(-11, 6), (11, 6), (11, 25), (-11, 25)], fc="none"); sv.rect(-9, 8, 18, 17, fc="none", lw="thin")
    sv.line([(11, 14), (16, 12), (18, -12)], lw=2.0, color="#999999")
    for (x, y, n, dx, dy) in [(-6, -5, 13, -14, -6), (0, 4.5, 14, -16, 6), (0, 13, 15, 14, 8), (-11, 20, 16, -12, 6)]:
        sv.balloon(x, y, n, dx, dy)
    sv.dim((-11, 25), (11, 25), 5, "d22 cup", "V/E")
    sh.note(250, 100, "NOTES - DETAILS", 7, weight="bold")
    sh.note(250, 94, "\n".join([
        "1. Steam valve: needle stem, fine thread (1.0 pitch [D]); packing stack =",
        "   brass washer + rubber packing + brass washer, compressed by packing nut",
        "   (AF14 [D]). Knob fixed by cross pin - drive it out before removal.",
        "2. Sight glass: borosilicate 3.3. Glass must float between the seals;",
        "   never let glass touch metal. Inner lock nuts are reached through the",
        "   boiler bottom (element removed). PTFE washers both sides of the shell.",
        "3. Boiler cap: v2 cap screws INSIDE the boiler neck [D]. Cap gasket",
        "   silicone. No anti-vacuum valve on this version.",
        "4. Safety valve: ball/spring, M12 thread [D], vent cup with drain tube",
        "   to the tray. Set-pressure unknown [E ~1.3-1.5 bar] - test before use.",
    ]), 5.3)
    sh.save(pdf)

# ================================================================== SHEET 5 : BASE, GRID, COVER, ELECTRICS
def sheet5(pdf):
    sh = Sheet(None, "BASE, DRIP GRID, RUBBER COVER & WIRING", "1:2")
    p = View(sh, 25, 205, 0.5, "BASE - PLAN (1:2)", lx=25 + 67, ly=150)
    p.poly(rounded_trap(BASE_RW, BASE_FW, BASE_L, BASE_R), fc="#d9efe6")
    p.poly(rounded_trap(BASE_RW - 16, BASE_FW - 16, BASE_L - 16, BASE_R - 8), fc="none", lw="hid")
    p.poly([(x + VD["TRAY_X0"], y) for x, y in rounded_trap(VD["TRAY_W"], VD["TRAY_W"] - 4, VD["TRAY_L"], 26)], fc="#ffffff")
    p.circ(BOIL_X, 0, 40.5, fc="white"); p.cl((BOIL_X - 50, 0), (BOIL_X + 50, 0)); p.cl((BOIL_X, -50), (BOIL_X, 50))
    p.dim((BOIL_X - 40.5, 0), (BOIL_X + 40.5, 0), 50, "Ø81 boiler hole", "E")
    p.dim((VD["TRAY_X0"], -58), (VD["TRAY_X0"] + VD["TRAY_L"], -58), -8, f"tray recess {VD['TRAY_L']} x {VD['TRAY_W']}", "V")
    p.dim((0, BASE_RW / 2), (BOIL_X, BASE_RW / 2), 8, f"{BOIL_X}", "V"); p.dim((BOIL_X, BASE_RW / 2), (VD["TRAY_X0"], BASE_RW / 2), 8, f"{VD['TRAY_X0'] - BOIL_X}", "V")
    p.dim((0, -BASE_RW / 2), (BASE_L, -BASE_RW / 2), -14, "270", "D"); p.dim((0, -BASE_RW / 2), (0, BASE_RW / 2), -10, "180", "D")
    p.text(5, 80, "61", size=6, weight="bold")
    s = View(sh, 25, 95, 0.5, "BASE - SIDE (switch side) (1:2)", lx=25 + 67, ly=78)
    s.poly([(4, 3), (BASE_L - 4, 3), (BASE_L - 10, BASE_H - 6), (BASE_L - 22, BASE_H), (22, BASE_H), (8, BASE_H - 8)], fc="#d9efe6")
    s.rect(0, 0, BASE_L, 3, fc="#222", lw="thin"); s.rect(0, 3, BASE_L, 7, fc="#333", lw="thin")
    s.rect(VD["SW_X"] - 15, 19, 30, 22, fc="white"); s.text(VD["SW_X"] - 14, 43, "65 cut-out 30 x 22 [V], centre X67 Z30", size=4.6)
    s.text(150, 40, "64 badge Ø38 is on the FRONT face (Y-30, Z33)\n66 cable gland M16 on the REAR face (Y+40, Z25)", size=4.6)
    s.dim((BASE_L, 0), (BASE_L, BASE_H), 8, "60", "V")
    s.text(140, -4, "Deep-drawn steel 1.0 [E]; flange/skirt rolled; powder RAL 6027 (restomod)", size=4.6, color=NOTE)
    # drip grid
    g = View(sh, 222, 215, 0.6, "62 DRIP GRID (1:1.67)", lx=222, ly=172)
    g.poly([(x - 70.5, y) for x, y in rounded_trap(112, 108, 141, 26)], fc="#eeeeee")
    for i in range(10):
        for j in range(8):
            x, y = -55 + i * 12.2, -45 + j * 12.8
            if abs(x - (-55 + 4.5 * 12.2)) < 7 and abs(y - (-45 + 3.5 * 12.8)) < 7: continue
            g.circ(x, y, 4, lw="thin", fc="white")
    g.circ(-55 + 4.5 * 12.2, -45 + 3.5 * 12.8, 2.5, lw="thin", fc="white")
    g.dim((-70.5, -60), (70.5, -60), -6, "141 x 112", "V"); g.text(-60, 62, "AISI 304, t 0.8 [E]; ~70 x d8 [V]", size=4.6)
    # rubber cover section
    r = View(sh, 190, 120, 0.6, "63 RUBBER COVER - SECTION (1:1.67)", lx=190 + 80, ly=105)
    r.poly([(0, 0), (BASE_L / 2, 0), (BASE_L / 2, 3), (8, 3), (8, 11), (0, 11)], fc="#333", hatch=None)
    r.dim((0, 0), (0, 11), -6, "11 lip", "V/E"); r.dim((BASE_L / 2 - 20, 0), (BASE_L / 2 - 20, 3), 6, "3", "E")
    r.text(30, 6, "SBR/NR 60 ShA, 4 holes; press-fit over skirt (no screws seen)", size=4.6)
    # wiring schematic
    wx, wy = 282, 255
    ax = sh.ax
    ax.text(wx, wy + 22, "WIRING - 1979 v2.2 (as rebuilt in video)", fontsize=7, weight="bold")
    def box(x, y, w, h, t, fc="white"):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=0.5)); ax.text(x + w / 2, y + h / 2, t, fontsize=5, ha="center", va="center")
    box(wx, wy - 4, 22, 14, "MAINS\n220 V\nL N PE")
    box(wx + 40, wy - 10, 26, 24, "2-gang\nrocker 65\nI (red, lamp)\nII (white)", fc="#fff3f3")
    box(wx + 85, wy + 2, 24, 10, "R1 200 W", fc="#fde9d0"); box(wx + 85, wy - 14, 24, 10, "R2 800 W", fc="#fde9d0")
    L_ = lambda pts, c="#a0522d": ax.plot(*zip(*pts), lw=0.8, color=c)
    L_([(wx + 22, wy + 6), (wx + 40, wy + 6)]); L_([(wx + 66, wy + 8), (wx + 85, wy + 7)]); L_([(wx + 66, wy - 4), (wx + 85, wy - 9)])
    L_([(wx + 109, wy + 7), (wx + 116, wy + 7), (wx + 116, wy - 22), (wx + 11, wy - 22), (wx + 11, wy - 4)], "#1f5fbf")
    L_([(wx + 109, wy - 9), (wx + 116, wy - 9)], "#1f5fbf")
    L_([(wx + 5, wy - 4), (wx + 5, wy - 30), (wx + 97, wy - 30), (wx + 97, wy - 14)], "#2e8b57")
    ax.text(wx + 40, wy - 34, "PE -> element flange (M6 ring tag)", fontsize=4.6, color="#2e8b57")
    ax.text(wx, wy - 42, "Lamp in rocker I. I = 200 W keep-warm, II = 800 W heat-up\n(I+II = 1000 W). Internal wires: 1.0 mm2 silicone/glass\nbraid, insulated 6.3 mm spades. Check: insulation\n> 2 MOhm at 500 V, PE continuity < 0.1 Ohm.", fontsize=4.8, va="top")
    sh.save(pdf)

# ================================================================== SHEET 6/7 : BOM
def bom_sheet(pdf, no, rows, title):
    sh = Sheet(no, title, "-")
    cols = [("ITEM", 12), ("QTY", 9), ("DESCRIPTION", 82), ("MATERIAL / FINISH", 112), ("KEY DIMENSIONS (mm)", 108), ("CONF.", 13), ("DRAWING", 14)]
    x0, y0, rh = 14, 283, 5.55
    x = x0
    for name, w in cols:
        sh.ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc="#dde6f3", ec=INK, lw=0.4)); sh.ax.text(x + 1, y0 - rh / 2, name, fontsize=5.2, va="center", weight="bold"); x += w
    for i, r in enumerate(rows):
        y = y0 - rh * (i + 2); x = x0
        vals = [r[0], str(r[1]), r[2], r[3], r[4], r[5], r[6]]
        for (name, w), val in zip(cols, vals):
            sh.ax.add_patch(Rectangle((x, y), w, rh, fc="white" if i % 2 else "#f7f7f7", ec="#888", lw=0.2))
            fs = 4.7 if len(val) < 70 else 4.1
            sh.ax.text(x + 1, y + rh / 2, val, fontsize=fs, va="center", clip_on=True); x += w
    sh.save(pdf)

def sheet8(pdf):
    sh = Sheet(None, "SEAL & FASTENER SCHEDULE, ASSEMBLY SEQUENCE, VERIFICATION LIST", "-")
    ax = sh.ax
    ax.text(14, 283, "SEAL SCHEDULE", fontsize=7.5, weight="bold", va="top")
    cols = [("ITEM", 12), ("SEAL", 40), ("SIZE (mm)", 40), ("RECOMMENDED COMPOUND", 80), ("ORIGINAL 1979", 40)]
    y0, rh = 276, 5.3; x = 14
    for n, w in cols:
        ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc="#dde6f3", ec=INK, lw=0.4)); ax.text(x + 1, y0 - rh / 2, n, fontsize=5, va="center", weight="bold"); x += w
    for i, r in enumerate(SEALS):
        x = 14; y = y0 - rh * (i + 2)
        for (n, w), val in zip(cols, r):
            ax.add_patch(Rectangle((x, y), w, rh, fc="white", ec="#888", lw=0.2)); ax.text(x + 1, y + rh / 2, val, fontsize=4.6, va="center"); x += w
    ax.text(14, 205, "FASTENER SCHEDULE", fontsize=7.5, weight="bold", va="top")
    fas = [("46", "2", "Hex bolt ISO 4017 M6x10 A2-70", "Group to boiler", "~6 Nm [E]"),
           ("8", "3", "Socket cap ISO 4762 M6x16 8.8 Zn (or M5x12)", "Element to ring nut", "~4 Nm, 3 passes [E]"),
           ("4", "1", "Ring nut M80x1.25 brass, 3 ears", "Boiler to base", "hand + 1/8 turn [E]"),
           ("47/48", "1+1", "Hex nut M8 + acorn nut DIN 1587 M8", "Group top stud", "snug + sealant"),
           ("50/51", "2+4", "Pin d6x32 + E-clip DIN 6799-5", "Lever fulcrum / rod", "-"),
           ("21", "2", "Hex nut M12x1 brass", "Sight-glass spigots (inside)", "firm, PTFE washer"),
           ("20", "2", "Gland nut M16x1, AF17", "Sight-glass glass retainers", "hand + 1/4 turn"),
           ("33", "1", "Union nut M14x1, AF17", "Steam wand to valve", "snug"),
           ("31", "1", "Spring pin ISO 8752 d2.5x16", "Steam knob", "-"),
           ("66", "1", "Cable gland M16x1.5 + lock nut", "Mains entry", "-")]
    cols = [("ITEM", 14), ("QTY", 10), ("FASTENER", 78), ("JOINT", 58), ("TIGHTENING", 44)]
    y0 = 198; x = 14
    for n, w in cols:
        ax.add_patch(Rectangle((x, y0 - rh), w, rh, fc="#dde6f3", ec=INK, lw=0.4)); ax.text(x + 1, y0 - rh / 2, n, fontsize=5, va="center", weight="bold"); x += w
    for i, r in enumerate(fas):
        x = 14; y = y0 - rh * (i + 2)
        for (n, w), val in zip(cols, r):
            ax.add_patch(Rectangle((x, y), w, rh, fc="white", ec="#888", lw=0.2)); ax.text(x + 1, y + rh / 2, val, fontsize=4.6, va="center"); x += w
    ax.text(14, 130, "ASSEMBLY SEQUENCE (as performed in the video, 22:01-30:25)", fontsize=7.5, weight="bold", va="top")
    seq = ["1  Sight-glass blocks into shell with PTFE washers + food-grade sealant; inner M12x1 nuts tightened from inside (22:08-22:33).",
           "2  Base over boiler neck: upper gasket - base - lower gasket - ring nut (3-lug tool, 23:05-23:39).",
           "3  Element gasket on flange, element in, 3 screws tightened cross-wise (23:40-23:59).",
           "4  Cable gland, mains cord, PE ring tag, switch snapped into cut-out, glass-braid leads to element (24:01-24:46).",
           "5  Badge pins through base, bent over; rubber cover pressed on (24:46-25:01).",
           "6  Sight glass: seals, washers, guard, glass, gland nuts; top plug (25:03-25:48).",
           "7  Group: rod seal + washer + circlip, piston with 2 greased seals, screen + gasket (25:48-26:51).",
           "8  Group-to-boiler seal + L-tube, 2 bolts; top lock + acorn nut; lever, pins, E-clips, handle (26:52-28:02).",
           "9  Safety valve ball, spring, cup; steam wand + tip; steam valve stem + packing; knob pin (28:03-29:12).",
           "10 Boiler cap; portafilter handle + spout; grid. Power-up test I and II (29:13-31:50)."]
    for i, s_ in enumerate(seq): ax.text(14, 123 - i * 4.9, s_, fontsize=5.1, va="top")
    ax.text(235, 283, "VERIFY BEFORE MANUFACTURE (calipers / thread gauge)", fontsize=7.5, weight="bold", va="top", color=NOTE)
    ver = ["Boiler shell OD and wall thickness (ultrasonic gauge).",
           "Neck thread major dia. (M80 assumed from 80 mm gasket ID).",
           "Neck internal thread (~M38x1.5 assumed).",
           "Sight-glass spigot / gland threads and glass OD & length.",
           "Safety-valve thread pitch and set pressure.",
           "Piston-seal ID (36 vs 33 mm between suppliers).",
           "Piston rod diameter, cross-hole, stroke.",
           "Element screw size (M6 vs M5) in YOUR ring nut.",
           "Lever pin dia., link length, lever length.",
           "Base sheet thickness, hole positions, switch cut-out.",
           "Steam valve seat geometry and wand bend radii.",
           "All [V] values: scaled from video at +/-5% at best."]
    for i, s_ in enumerate(ver): ax.text(235, 276 - i * 5.0, "[ ]  " + s_, fontsize=5.3, va="top")
    ax.text(235, 208, "MATERIAL NOTES", fontsize=7.5, weight="bold", va="top")
    mat = ["Brass parts: CW617N (CuZn40Pb2) forgings / CW614N bar; for new parts in",
           "potable-water contact prefer low-lead CW511L (DZR) or CW724R.",
           "Plating: Cu strike + bright Ni 15-20 um + Cr 0.3 um (decorative).",
           "Re-chroming in video: brush (tampon) chrome, 60 C, ~0.8 A.",
           "Seals: food grade (FDA 21 CFR 177.2600 / EC 1935/2004) silicone or EPDM.",
           "Fibre gaskets: AFM34 or equivalent asbestos-free, food safe.",
           "Lubricant: food-grade silicone grease (NSF H1), e.g. Molykote 111.",
           "Thread sealant: food-grade anaerobic (NSF/ANSI 61 listed).",
           "Wood (restomod): birdseye maple, hard-wax oil 3 coats, 1000-grit between."]
    for i, s_ in enumerate(mat): ax.text(235, 201 - i * 4.9, s_, fontsize=5.1, va="top")
    ax.text(235, 150, "WEIGHT BREAKDOWN (estimate, total 5.5 kg [D])", fontsize=7, weight="bold", va="top")
    wt = [("Boiler assembly incl. element, ring nut, sight glass", "2.15 kg"), ("Group + piston + lever", "1.05 kg"),
          ("Base + grid + rubber cover + switch + cord", "1.55 kg"), ("Portafilter + baskets + spout", "0.55 kg"),
          ("Cap, steam valve, wand, safety valve", "0.20 kg")]
    for i, (a, b) in enumerate(wt): ax.text(235, 143 - i * 4.9, a, fontsize=5.1, va="top"); ax.text(372, 143 - i * 4.9, b, fontsize=5.1, va="top", weight="bold")
    sh.save(pdf)

def main():
    import glob
    for f in glob.glob(os.path.join(OUT, "sheet*.png")) + glob.glob(os.path.join(OUT, "sheet*.svg")): os.remove(f)
    import view_sheets as VS, iso as ISO, pro_misc as PM, pro_build as PB, pro_option as PO
    Sheet.total = 33; Sheet.counter = 0
    PM.BOM[:] = [r for r in PM.BOM if r[0] not in [b[0] for b in PO.BOM]] + PO.BOM
    PM.FASTENERS[:] = [r for r in PM.FASTENERS if 'OPTION' not in r[6]] + PO.FASTENERS
    with PdfPages(os.path.join(OUT, "LaPavoni_Professional_CopperBrass_drawings.pdf")) as pdf:
        ISO.sheet_iso(pdf, Sheet); ISO.sheet_exploded(pdf, Sheet)
        VS.sheet_front_rear(pdf, Sheet); VS.sheet_sides(pdf, Sheet); VS.sheet_plan(pdf, Sheet)
        PM.sheet_boiler(pdf, Sheet); PM.sheet_group(pdf, Sheet); PM.sheet_joint(pdf, Sheet); PM.sheet_wiring(pdf, Sheet)
        PB.build(pdf, Sheet)
        PO.build(pdf, Sheet)
        PM.sheet_fasteners(pdf, Sheet)
        half = (len(PM.BOM) + 1) // 2
        bom_sheet(pdf, None, PM.BOM[:half], "BILL OF MATERIALS (1 of 2)")
        bom_sheet(pdf, None, PM.BOM[half:], "BILL OF MATERIALS (2 of 2)")
        PM.sheet_schedule(pdf, Sheet)
    print("sheets:", Sheet.counter)
    with open(os.path.join(OUT, "BOM.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Item", "Qty", "Description", "Material / finish", "Key dimensions (mm)", "Confidence", "Drawing"])
        w.writerows(PM.BOM)

if __name__ == "__main__":
    main()

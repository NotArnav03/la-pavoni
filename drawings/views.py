"""Simple 3D primitive model of the Europiccola v2.2 + orthographic projector (6 views).
Machine coordinates (mm): X = rear->front (user stands at +X), Y = -left/+right (switch side is LEFT = -Y),
Z = up from table. Origin: rear end of base, centre line, table level."""
import math
from matplotlib.patches import Polygon, Circle

INK = "#111111"; DIMC = "#0b3d91"; PT = 72 / 25.4
CHROME, BRASS, WOOD, BASEC, RUBBER, STEEL = "#ececec", "#e6c98f", "#d2ae7e", "#cfeee3", "#2b2b2b", "#d0d0d0"

# ----------------------------------------------------------------- key dimensions (single source of truth)
D = dict(
    L=270, W_REAR=180, W_FRONT=170, BASE_R=50, BASE_H=60, RUB_H=12,
    BX=70,                      # boiler axis from base rear
    FOOT_D=92, FOOT_Z=71,       # flared boiler foot ring
    SH_D=80, SH_Z1=240,         # shell OD, shell top (shoulder start)
    SHO_Z=263, NECK_D=44, NECK_Z=273, CAP_Z=300, TOP=320, KNOB_D=58,
    GX=155,                     # group axis from base rear (BX + 85)
    PORT_Z=218, BOLT_CC=38, ROD_PIN_X=155, ROD_PIN_Z=269.4, COL_X0=124, COL_X1=138,
    PF_Z0=160, BELL_Z0=176, BELL_Z1=196, BELL_D=72, BODY_Z1=260, YOKE_Z1=289, ACORN_Z=310,
    SPOUT_Z=132, PF_D=60, BODY_D=50,
    FX=130, FZ=281,             # lever fulcrum
    LEV_ANG=24.9, LEV_L=272, HANDLE_L=101, HANDLE_D=22,
    SG_X=44, SG_Y=-39, SG_Z0=113, SG_Z1=238,
    SV_X=100, SV_Y=11, PAD_X0=108, PAD_X1=118, FL_X1=123, PAD_W=26, PAD_H=52, SHELL_TOP=228,
    STK_X0=-26, STK_D=37, STK_Z=258,
    PF_ANG=242,                 # portafilter handle direction in plan (deg from +X, CCW seen from top)
    TRAY_X0=99, TRAY_L=141, TRAY_W=112,
    SW_X=67, SW_Z=30, SW_W=30, SW_H=22,
    BADGE_Y=-30, BADGE_Z=33, BADGE_D=38,
)

def rounded_trap(rw, fw, L, r, n=10, x0=0.0):
    pts = []
    for cx, cy, a0, a1 in [(L - r, fw / 2 - r, 0, 90), (r, rw / 2 - r, 90, 180), (r, -rw / 2 + r, 180, 270), (L - r, -fw / 2 + r, 270, 360)]:
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n); pts.append((x0 + cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

PROJ = {
    "FRONT": lambda x, y, z: (y, z, x), "REAR": lambda x, y, z: (-y, z, -x),
    "LEFT": lambda x, y, z: (x, z, -y), "RIGHT": lambda x, y, z: (-x, z, y),
    "TOP": lambda x, y, z: (x, y, z), "BOTTOM": lambda x, y, z: (x, -y, -z),
}
LOOK = {"FRONT": 0, "REAR": 0, "LEFT": 1, "RIGHT": 1, "TOP": 2, "BOTTOM": 2}

def lobed(cu, cv, r, n=6, k=0.15, m=72):
    return [(cu + r * (1 - k + k * math.cos(n * 2 * math.pi * i / m)) * math.cos(2 * math.pi * i / m),
             cv + r * (1 - k + k * math.cos(n * 2 * math.pi * i / m)) * math.sin(2 * math.pi * i / m)) for i in range(m)]

def hexagon(cu, cv, r):
    return [(cu + r * math.cos(math.radians(30 + 60 * i)), cv + r * math.sin(math.radians(30 + 60 * i))) for i in range(6)]

class Cyl:
    """Frustum between 3D points A and B (axis must be parallel to X, Y or Z)."""
    def __init__(self, A, B, r0, r1=None, fc=CHROME, shape="round", bias=0, name=""):
        self.A, self.B, self.r0, self.r1 = A, B, r0, (r0 if r1 is None else r1); self.fc, self.shape, self.bias, self.name = fc, shape, bias, name
        self.axis = [i for i in range(3) if abs(A[i] - B[i]) > 1e-9][0]
    def ops(self, view, pr):
        a, b = pr(*self.A), pr(*self.B)
        depth = (a[2] + b[2]) / 2 + self.bias
        if self.axis == LOOK[view]:
            near, far = (a, self.r0), (b, self.r1)
            if b[2] > a[2]: near, far = (b, self.r1), (a, self.r0)
            rmax = max(self.r0, self.r1); out = []
            out.append(("shape", near[0][0], near[0][1], rmax, self.shape, self.fc))
            if near[1] < rmax - 0.5: out.append(("shape", near[0][0], near[0][1], near[1], self.shape, "none"))
            return depth, out
        du, dv = b[0] - a[0], b[1] - a[1]; L = math.hypot(du, dv) or 1; nu, nv = -dv / L, du / L
        poly = [(a[0] + nu * self.r0, a[1] + nv * self.r0), (b[0] + nu * self.r1, b[1] + nv * self.r1),
                (b[0] - nu * self.r1, b[1] - nv * self.r1), (a[0] - nu * self.r0, a[1] - nv * self.r0)]
        return depth, [("poly", poly, self.fc)]

class Loft:
    """Prism between plan outline pts0 at z0 and pts1 at z1 (convex)."""
    def __init__(self, pts0, z0, pts1, z1, fc=BASEC, bias=0, name=""):
        self.p0, self.z0, self.p1, self.z1, self.fc, self.bias, self.name = pts0, z0, pts1, z1, fc, bias, name
    def ops(self, view, pr):
        c = [pr(x, y, self.z0) for x, y in self.p0]; d = [pr(x, y, self.z1) for x, y in self.p1]
        depth = (sum(p[2] for p in c + d) / len(c + d)) + self.bias
        if LOOK[view] == 2:
            near, far = (d, c) if view == "TOP" else (c, d)
            return depth, [("poly", [(p[0], p[1]) for p in far], self.fc), ("poly", [(p[0], p[1]) for p in near], self.fc)]
        u0 = [p[0] for p in c]; u1 = [p[0] for p in d]
        poly = [(min(u0), c[0][1]), (max(u0), c[0][1]), (max(u1), d[0][1]), (min(u1), d[0][1])]
        return depth, [("poly", poly, self.fc)]

def Box(x0, x1, y0, y1, z0, z1, fc=CHROME, bias=0, name=""):
    r = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return Loft(r, z0, r, z1, fc, bias, name)

class Holes:
    """Perforations, drawn only in the TOP view."""
    def __init__(self, pts, r, z): self.pts, self.r, self.z = pts, r, z
    def ops(self, view, pr):
        if view != "TOP": return -1e9, []
        out = []
        for x, y in self.pts:
            u, v, dp = pr(x, y, self.z); out.append(("shape", u, v, self.r, "round", "#7f7f7f"))
        return self.z + 1.1, out

class Tube:
    def __init__(self, pts, d, fc=CHROME, bias=0, cap="round", name=""):
        self.pts, self.d, self.fc, self.bias, self.cap, self.name = pts, d, fc, bias, cap, name
    def ops(self, view, pr):
        q = [pr(*p) for p in self.pts]
        return sum(p[2] for p in q) / len(q) + self.bias, [("tube", [(p[0], p[1]) for p in q], self.d, self.fc, self.cap)]

def model():
    d = D; M = []
    bx, gx = d["BX"], d["GX"]
    # base + rubber cover + grid
    M.append(Loft(rounded_trap(d["W_REAR"], d["W_FRONT"], d["L"], d["BASE_R"]), 8,
                  rounded_trap(d["W_REAR"] - 12, d["W_FRONT"] - 12, d["L"] - 12, d["BASE_R"] - 6, x0=6), d["BASE_H"], name="base"))
    M.append(Loft(rounded_trap(d["W_REAR"] + 4, d["W_FRONT"] + 4, d["L"] + 4, d["BASE_R"] + 2, x0=-2), 0,
                  rounded_trap(d["W_REAR"] + 4, d["W_FRONT"] + 4, d["L"] + 4, d["BASE_R"] + 2, x0=-2), d["RUB_H"], fc=RUBBER, bias=2, name="rubber"))
    M.append(Loft(rounded_trap(d["TRAY_W"], d["TRAY_W"] - 4, d["TRAY_L"], 26, x0=d["TRAY_X0"]), 59,
                  rounded_trap(d["TRAY_W"], d["TRAY_W"] - 4, d["TRAY_L"], 26, x0=d["TRAY_X0"]), 60.5, fc="#bdbdbd", bias=1, name="grid"))
    M.append(Holes([(d["TRAY_X0"] + 12 + i * 13, -44 + j * 12.6) for i in range(10) for j in range(8) if not (abs(i - 4.5) < 1 and abs(j - 3.5) < 1)], 4, 60.6))
    # switch, badge, cable gland
    sx, sz, sw, sh = d["SW_X"], d["SW_Z"], d["SW_W"], d["SW_H"]
    M.append(Box(sx - sw / 2 - 2, sx + sw / 2 + 2, -90.5, -87, sz - sh / 2 - 2, sz + sh / 2 + 2, fc="#222222", bias=3, name="switch"))
    M.append(Box(sx - sw / 2, sx + sw / 2, -91, -88, sz, sz + sh / 2, fc="#e03030", bias=4))
    M.append(Box(sx - sw / 2, sx + sw / 2, -91, -88, sz - sh / 2, sz, fc="#f3eedd", bias=4))
    M.append(Cyl((265, d["BADGE_Y"], d["BADGE_Z"]), (269, d["BADGE_Y"], d["BADGE_Z"]), d["BADGE_D"] / 2, fc="#d93030", bias=3, name="badge"))
    M.append(Cyl((-9, 40, 25), (3, 40, 25), 8, fc=STEEL, bias=3, name="gland")); M.append(Cyl((-3, 40, 25), (0, 40, 25), 11, fc=STEEL, shape="hex", bias=3))
    M.append(Tube([(-9, 40, 25), (-30, 44, 18), (-45, 48, 8)], 7, fc="#f4f4f4", cap="butt", name="cord"))
    # boiler
    M.append(Cyl((bx, 0, 60), (bx, 0, d["FOOT_Z"]), d["FOOT_D"] / 2, d["SH_D"] / 2 + 1, name="foot"))
    M.append(Cyl((bx, 0, d["FOOT_Z"]), (bx, 0, d["SH_Z1"]), d["SH_D"] / 2, name="shell"))
    M.append(Cyl((bx, 0, d["SH_Z1"]), (bx, 0, d["SHO_Z"]), d["SH_D"] / 2, d["NECK_D"] / 2, name="shoulder"))
    M.append(Cyl((bx, 0, d["SHO_Z"]), (bx, 0, d["NECK_Z"]), d["NECK_D"] / 2, name="neck"))
    M.append(Cyl((bx, 0, d["NECK_Z"]), (bx, 0, d["CAP_Z"]), 14, 19, fc=WOOD, name="capcone"))
    M.append(Cyl((bx, 0, d["CAP_Z"]), (bx, 0, d["TOP"]), d["KNOB_D"] / 2, fc=WOOD, shape="lobed", name="capknob"))
    # sight glass
    sgx, sgy = d["SG_X"], d["SG_Y"]
    for z in (d["SG_Z0"], d["SG_Z1"]):
        M.append(Box(sgx - 9, sgx + 9, sgy - 9, sgy + 9, z - 9, z + 9, bias=1))
    M.append(Cyl((sgx, sgy, d["SG_Z0"] + 9), (sgx, sgy, d["SG_Z1"] - 9), 8, bias=1, name="sg guard"))
    M.append(Cyl((sgx, sgy, d["SG_Z1"] + 9), (sgx, sgy, d["SG_Z1"] + 15), 4.5, bias=1))
    M.append(Cyl((sgx, sgy, d["SG_Z0"] - 15), (sgx, sgy, d["SG_Z0"] - 9), 8.5, shape="hex", bias=1))
    # steam valve (pointing to the rear), knob, wand
    z = d["STK_Z"]; y = 0
    M.append(Cyl((bx - 31, y, z), (bx - 37, y, z), 9.8, shape="hex"))
    M.append(Cyl((bx - 37, y, z), (6, y, z), 7.5, name="steam arm"))
    M.append(Cyl((6, y, z), (-2, y, z), 8, shape="hex"))
    M.append(Cyl((-2, y, z), (-6, y, z), 3))
    M.append(Cyl((-6, y, z), (d["STK_X0"], y, z), d["STK_D"] / 2, d["STK_D"] / 2 - 3, fc=WOOD, shape="lobed", name="steam knob"))
    M.append(Cyl((18, 0, z - 7), (18, 0, z - 15), 9.8, shape="hex"))
    M.append(Tube([(18, 0, z - 15), (18, 0, 212), (16, -22, 178), (14, -34, 136), (18, -38, 124)], 8, bias=0.5, name="wand"))
    # safety valve + drain
    M.append(Cyl((d["SV_X"], d["SV_Y"], 252), (d["SV_X"], d["SV_Y"], 258), 8.1, shape="hex"))
    M.append(Cyl((d["SV_X"], d["SV_Y"], 262), (d["SV_X"], d["SV_Y"], 286), 11, name="sv cup"))
    M.append(Tube([(d["SV_X"] + 8, 22, 272), (118, 26, 262), (124, 26, 236), (124, 26, 120), (128, 26, 62)], 5, name="drain"))
    # group: pad, flange, bolts, body
    pz = d["PORT_Z"]
    M.append(Box(bx + 36, d["PAD_X1"], -13, 13, pz - 26, pz + 26, name="pad"))
    M.append(Box(d["PAD_X1"], d["FL_X1"], -13, 13, pz - 26, pz + 26, name="flange"))
    for zz in (pz - d["BOLT_CC"] / 2, pz + d["BOLT_CC"] / 2):
        M.append(Cyl((d["FL_X1"], 0, zz), (d["FL_X1"] + 4, 0, zz), 5.77, fc=STEEL, shape="hex", bias=1))
    M.append(Cyl((d["FL_X1"], 0, pz), (131, 0, pz), 11))
    M.append(Cyl((gx, 0, d["PF_Z0"]), (gx, 0, d["BELL_Z0"]), d["PF_D"] / 2 - 2, d["PF_D"] / 2, name="pf"))
    M.append(Cyl((gx, 0, d["BELL_Z0"]), (gx, 0, d["BELL_Z1"]), d["BELL_D"] / 2, name="bell"))
    M.append(Cyl((gx, 0, d["BELL_Z1"]), (gx, 0, 206), d["BELL_D"] / 2, d["BODY_D"] / 2))
    M.append(Cyl((gx, 0, 206), (gx, 0, d["BODY_Z1"]), d["BODY_D"] / 2, name="cyl"))
    M.append(Box(d["COL_X0"], d["COL_X1"], -8, 8, d["BODY_Z1"] - 4, d["YOKE_Z1"], name="column"))
    M.append(Cyl((gx, 0, d["BODY_Z1"]), (gx, 0, 297), 5, fc=STEEL, name="rod"))
    M.append(Box(gx - 6, gx + 6, -5, 5, 262, 277, fc=STEEL, name="rod eye"))
    M.append(Cyl((gx, 0, 293), (gx, 0, 299), 7.5, shape="hex"))
    M.append(Cyl((gx, 0, 299), (gx, 0, d["ACORN_Z"]), 7.5, 5, shape="hex", name="acorn"))
    M.append(Cyl((gx, 0, 146), (gx, 0, d["PF_Z0"]), 6, 7, name="spout"))
    M.append(Tube([(gx, -5, 147), (gx, -15, d["SPOUT_Z"] + 3)], 6)); M.append(Tube([(gx, 5, 147), (gx, 15, d["SPOUT_Z"] + 3)], 6))
    # portafilter handle
    a = math.radians(d["PF_ANG"]); ux, uy = math.cos(a), math.sin(a)
    p = lambda r, zz: (gx + r * ux, r * uy, zz)
    M.append(Tube([p(28, 172), p(52, 170)], 15, name="pf arm")); M.append(Tube([p(52, 170), p(152, 165)], 24, fc=WOOD, name="pf handle"))
    # lever
    la = math.radians(d["LEV_ANG"]); lx, lz = math.cos(la), -math.sin(la)
    q = lambda r: (d["FX"] + r * lx, 0, d["FZ"] + r * lz)
    M.append(Tube([q(-14), q(60)], 22, fc="#3a3a3a", name="fork"))
    M.append(Tube([q(55), q(d["LEV_L"] - d["HANDLE_L"] + 4)], 11, name="lever rod"))
    M.append(Tube([q(d["LEV_L"] - d["HANDLE_L"]), q(d["LEV_L"])], d["HANDLE_D"], fc=WOOD, name="lever handle"))
    M.append(Cyl((d["FX"], -13, d["FZ"]), (d["FX"], 13, d["FZ"]), 3.5, fc=STEEL, bias=2, name="fulcrum pin"))
    M.append(Cyl((d["ROD_PIN_X"], -13, d["ROD_PIN_Z"]), (d["ROD_PIN_X"], 13, d["ROD_PIN_Z"]), 3.5, fc=STEEL, bias=2, name="rod pin"))
    return M

class ViewPort:
    def __init__(self, ax, view, ox, oy, s):
        self.ax, self.view, self.ox, self.oy, self.s, self.pr = ax, view, ox, oy, s, PROJ[view]
    def S(self, u, v): return (self.ox + u * self.s, self.oy + v * self.s)
    def P(self, x, y, z):
        u, v, _ = self.pr(x, y, z); return self.S(u, v)
    def draw(self, M, extra=None):
        items = []
        for prim in M:
            dp, ops = prim.ops(self.view, self.pr); items.append((dp, ops))
        items.sort(key=lambda t: t[0])
        z = 2
        for dp, ops in items:
            for op in ops:
                z += 0.001; self._op(op, z)
        if extra: extra(self)
    def _op(self, op, z):
        ax, s = self.ax, self.s
        if op[0] == "poly":
            ax.add_patch(Polygon([self.S(u, v) for u, v in op[1]], closed=True, fc=op[2], ec=INK, lw=0.45, zorder=z))
        elif op[0] == "shape":
            _, u, v, r, shape, fc = op
            if shape == "round": ax.add_patch(Circle(self.S(u, v), r * s, fc=fc, ec=INK, lw=0.45, zorder=z))
            else:
                pts = lobed(u, v, r) if shape == "lobed" else hexagon(u, v, r)
                ax.add_patch(Polygon([self.S(a, b) for a, b in pts], closed=True, fc=fc, ec=INK, lw=0.45, zorder=z))
        elif op[0] == "tube":
            _, pts, dmm, fc, cap = op
            xs, ys = zip(*[self.S(u, v) for u, v in pts]); w = dmm * s * PT
            ax.plot(xs, ys, lw=w + 0.9, color=INK, solid_capstyle=cap, solid_joinstyle="round", zorder=z)
            ax.plot(xs, ys, lw=max(w - 0.9, 0.3), color=fc, solid_capstyle=cap, solid_joinstyle="round", zorder=z + 0.0005)
    # --------------------------------------------------------------- annotation helpers (args in model mm)
    def hdim(self, pa, pb, ysheet, txt, tag="", size=5.0):
        A, B = self.P(*pa), self.P(*pb); self._dim(A, B, (A[0], ysheet), (B[0], ysheet), txt, tag, size, 0)
    def vdim(self, pa, pb, xsheet, txt, tag="", size=5.0):
        A, B = self.P(*pa), self.P(*pb); self._dim(A, B, (xsheet, A[1]), (xsheet, B[1]), txt, tag, size, 90)
    def _dim(self, A, B, A2, B2, txt, tag, size, rot):
        ax = self.ax
        for p, q in ((A, A2), (B, B2)):
            dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy)
            if L > 0.5:
                ex, ey = dx / L * 1.2, dy / L * 1.2
                ax.plot([p[0] + dx / L * 0.8, q[0] + ex], [p[1] + dy / L * 0.8, q[1] + ey], lw=0.2, color=DIMC, zorder=20)
        ax.annotate("", xy=A2, xytext=B2, arrowprops=dict(arrowstyle="<|-|>", lw=0.35, color=DIMC, mutation_scale=4.5, shrinkA=0, shrinkB=0), zorder=21)
        lab = txt + (f" [{tag}]" if tag else "")
        mx, my = (A2[0] + B2[0]) / 2, (A2[1] + B2[1]) / 2
        span = math.hypot(B2[0] - A2[0], B2[1] - A2[1])
        if rot == 0:
            ax.text(mx, my + 1.3, lab, fontsize=size, color=DIMC, ha="center", va="bottom", zorder=22, bbox=dict(fc="white", ec="none", pad=0.15))
        else:
            ax.text(mx - 1.3, my, lab, fontsize=size, color=DIMC, ha="right" if span < 4 else "center", va="center",
                    rotation=0 if span < 4 else 90, zorder=22, bbox=dict(fc="white", ec="none", pad=0.15))
    def dia(self, p, r, txt, tag="", ang=45, ext=9, size=5.0):
        c = self.P(*p); a = math.radians(ang); R = r * self.s
        e = (c[0] + R * math.cos(a), c[1] + R * math.sin(a)); q = (e[0] + ext * math.cos(a), e[1] + ext * math.sin(a))
        self.ax.annotate("", xy=e, xytext=q, arrowprops=dict(arrowstyle="-|>", lw=0.35, color=DIMC, mutation_scale=4.5, shrinkA=0, shrinkB=0), zorder=21)
        self.ax.plot([q[0], q[0] + (8 if math.cos(a) >= 0 else -8)], [q[1], q[1]], lw=0.35, color=DIMC, zorder=21)
        self.ax.text(q[0] + (8.5 if math.cos(a) >= 0 else -8.5), q[1], f"Ø{txt}" + (f" [{tag}]" if tag else ""), fontsize=size, color=DIMC,
                     ha="left" if math.cos(a) >= 0 else "right", va="center", zorder=22, bbox=dict(fc="white", ec="none", pad=0.15))
    def leader(self, p, txt, dx, dy, size=4.8, color=INK):
        a = self.P(*p); q = (a[0] + dx, a[1] + dy)
        self.ax.plot([a[0], q[0]], [a[1], q[1]], lw=0.3, color=color, zorder=21); self.ax.add_patch(Circle(a, 0.45, color=color, zorder=21))
        self.ax.text(q[0] + (0.8 if dx >= 0 else -0.8), q[1], txt, fontsize=size, color=color, ha="left" if dx >= 0 else "right", va="center", zorder=22,
                     bbox=dict(fc="white", ec="none", pad=0.15))
    def angle(self, p, r, a0, a1, txt, size=5.0):
        from matplotlib.patches import Arc
        c = self.P(*p); self.ax.add_patch(Arc(c, 2 * r, 2 * r, theta1=min(a0, a1), theta2=max(a0, a1), ec=DIMC, lw=0.35, zorder=21))
        am = math.radians((a0 + a1) / 2)
        self.ax.text(c[0] + (r + 2) * math.cos(am), c[1] + (r + 2) * math.sin(am), txt, fontsize=size, color=DIMC, ha="left", va="center", zorder=22,
                     bbox=dict(fc="white", ec="none", pad=0.15))
    def cl(self, p0, p1):
        a, b = self.P(*p0), self.P(*p1)
        self.ax.plot([a[0], b[0]], [a[1], b[1]], lw=0.22, ls=(0, (8, 2, 1.5, 2)), color="#555555", zorder=19)
    def hidden_circle(self, p, r, ec="#333333"):
        self.ax.add_patch(Circle(self.P(*p), r * self.s, fc="none", ec=ec, lw=0.3, ls=(0, (3, 1.5)), zorder=19))
    def label(self, text, x, y, scale_txt):
        self.ax.text(x, y, text, fontsize=7.5, weight="bold", ha="center", va="top")
        self.ax.text(x, y - 3.6, scale_txt, fontsize=5.5, ha="center", va="top")

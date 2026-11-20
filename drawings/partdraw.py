"""Generic detail-drawing engine: every diameter, step, depth, hole, thread, groove and bend is dimensioned.
Cells are laid out on A3 sheets; each cell = one part with its own scale."""
import math
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle, Arc

INK, DIMC, NOTE, HATCH_FC = "#111111", "#0b3d91", "#7a1f1f", "#f4e3b5"
SCALES = [5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.8, 2 / 3, 0.5, 0.4, 1 / 3, 0.25, 0.2]

def scale_label(s):
    if s >= 1: return f"{s:g}:1"
    return f"1:{1 / s:.3g}"

def pick_scale(w_mm, h_mm, cw, ch):
    for s in SCALES:
        if w_mm * s <= cw and h_mm * s <= ch: return s
    return SCALES[-1]

class Cell:
    """A drawing area on a sheet with a header strip."""
    def __init__(self, ax, x, y, w, h, item, name, material, qty, conf, note=""):
        self.ax, self.x, self.y, self.w, self.h = ax, x, y, w, h
        ax.add_patch(Rectangle((x, y), w, h, fill=False, lw=0.45, ec=INK, zorder=1))
        ax.add_patch(Rectangle((x, y + h - 7), w, 7, fc="#eef2f8", lw=0.45, ec=INK, zorder=1))
        ax.add_patch(Circle((x + 4.5, y + h - 3.5), 2.6, fc="white", ec=INK, lw=0.5, zorder=2))
        ax.text(x + 4.5, y + h - 3.5, str(item), fontsize=4.6, ha="center", va="center", weight="bold", zorder=3)
        ax.text(x + 9, y + h - 2.3, f"{name}   QTY {qty}   [{conf}]", fontsize=5.4, va="center", weight="bold", zorder=3)
        ax.text(x + 9, y + h - 5.3, material, fontsize=4.4, va="center", zorder=3)
        self.scale_txt_pos = (x + w - 1.5, y + h - 2.3)
        if note: ax.text(x + 1.5, y + 1.5, note, fontsize=4.1, va="bottom", color=NOTE, zorder=3, linespacing=1.25)
    def set_scale(self, s):
        self.ax.text(*self.scale_txt_pos, f"SCALE {scale_label(s)}", fontsize=4.6, ha="right", va="center", zorder=3)

# ------------------------------------------------------------------ low-level dimension helpers (sheet coords)
def _txt(ax, x, y, s, rot=0, size=4.6, ha="center", va="center", color=DIMC):
    ax.text(x, y, s, fontsize=size, color=color, rotation=rot, ha=ha, va=va, zorder=22, bbox=dict(fc="white", ec="none", pad=0.08))

def hdim(ax, x0, x1, yref0, yref1, y, txt, size=4.4):
    for xr, yr in ((x0, yref0), (x1, yref1)):
        ax.plot([xr, xr], [yr, y + (1 if y > yr else -1)], lw=0.18, color=DIMC, zorder=20)
    ax.annotate("", xy=(x0, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<|-|>", lw=0.3, color=DIMC, mutation_scale=3.6, shrinkA=0, shrinkB=0), zorder=21)
    if abs(x1 - x0) < 4.5:
        _txt(ax, max(x0, x1) + 0.8, y, txt, size=size, ha="left")
    else:
        _txt(ax, (x0 + x1) / 2, y + 1.0, txt, size=size, va="bottom")

def vdim(ax, y0, y1, xref0, xref1, x, txt, size=4.4, side="left"):
    for yr, xr in ((y0, xref0), (y1, xref1)):
        ax.plot([xr, x + (1 if x > xr else -1)], [yr, yr], lw=0.18, color=DIMC, zorder=20)
    ax.annotate("", xy=(x, y0), xytext=(x, y1), arrowprops=dict(arrowstyle="<|-|>", lw=0.3, color=DIMC, mutation_scale=3.6, shrinkA=0, shrinkB=0), zorder=21)
    if abs(y1 - y0) < 6:
        _txt(ax, x + (0.8 if side == "right" else -0.8), (y0 + y1) / 2, txt, size=size, ha="left" if side == "right" else "right")
    else:
        _txt(ax, x - 1.0, (y0 + y1) / 2, txt, rot=90, size=size)

def leader(ax, p, q, txt, size=4.4, color=DIMC):
    ax.plot([p[0], q[0]], [p[1], q[1]], lw=0.25, color=color, zorder=21)
    ax.add_patch(Circle(p, 0.35, color=color, zorder=21))
    ha = "left" if q[0] >= p[0] else "right"
    ax.plot([q[0], q[0] + (3 if ha == "left" else -3)], [q[1], q[1]], lw=0.25, color=color, zorder=21)
    _txt(ax, q[0] + (3.4 if ha == "left" else -3.4), q[1], txt, size=size, ha=ha, color=color)

def cl(ax, p0, p1):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], lw=0.2, ls=(0, (8, 2, 1.5, 2)), color="#555555", zorder=19)

# ================================================================== TURNED / AXISYMMETRIC PARTS
def turned(cell, spec):
    """spec: segs=[{L, D, D2?, t?(thread), hex?(AF), knurl?, lobes?}], bl=[(depth, D, thread?)], br=[...],
    grooves=[(x, w, Dg)], xholes=[(x, D, note)], flats, notes"""
    ax = cell.ax; segs = spec["segs"]
    for sg in segs:
        if "D" not in sg: sg["D"] = sg["hex"] * 1.1547
    Ltot = sum(s["L"] for s in segs); Dmax = max(max(s["D"], s.get("D2", 0), s.get("hex", 0) * 1.1547) for s in segs)
    s = spec.get("scale") or pick_scale(Ltot + 26, Dmax + 22, cell.w - 34, cell.h - 46)
    cell.set_scale(s)
    ox = cell.x + (cell.w - Ltot * s) / 2 - 4; oy = cell.y + cell.h / 2 + 1
    X = lambda x: ox + x * s; Y = lambda r: oy + r * s
    # outer profile points (upper half)
    xs = [0]; prof = []
    for sg in segs:
        x0 = xs[-1]; x1 = x0 + sg["L"]; xs.append(x1)
        r0 = sg["D"] / 2; r1 = sg.get("D2", sg["D"]) / 2
        if sg.get("hex"): r0 = r1 = sg["hex"] / 2 * 1.1547
        prof.append((x0, x1, r0, r1, sg))
    # bore profile from both ends -> function rb(x)
    def bore_r(x):
        r = 0.0; acc = 0
        for dpt, D, *_ in spec.get("bl", []):
            if acc <= x < acc + dpt: r = max(r, D / 2)
            acc += dpt
        acc = Ltot
        for dpt, D, *_ in spec.get("br", []):
            if acc - dpt <= x < acc: r = max(r, D / 2)
            acc -= dpt
        for x0, w, Dg in spec.get("grooves", []): pass
        return r
    # breakpoints
    bp = sorted(set(xs + [round(v, 4) for v in _bore_breaks(spec, Ltot)]))
    # section (upper) polygon, hatched; external view (lower) outline
    for (x0, x1, r0, r1, sg) in prof:
        sub = [b for b in bp if x0 <= b <= x1]
        for a, b in zip(sub[:-1], sub[1:]):
            ra = r0 + (r1 - r0) * (a - x0) / (x1 - x0); rb_ = r0 + (r1 - r0) * (b - x0) / (x1 - x0)
            ri = bore_r((a + b) / 2)
            if ra > ri + 1e-6:
                ax.add_patch(Polygon([(X(a), Y(ri)), (X(b), Y(ri)), (X(b), Y(rb_)), (X(a), Y(ra))], closed=True,
                                     fc=spec.get("fc", HATCH_FC), ec="none", hatch=spec.get("hatch", "////"), lw=0, zorder=3))
        # outline upper & lower
        ax.plot([X(x0), X(x1)], [Y(r0), Y(r1)], lw=0.7, color=INK, zorder=5)
        ax.plot([X(x0), X(x1)], [Y(-r0), Y(-r1)], lw=0.7, color=INK, zorder=5)
        ax.add_patch(Polygon([(X(x0), Y(-r0)), (X(x1), Y(-r1)), (X(x1), Y(0)), (X(x0), Y(0))], closed=True, fc=spec.get("ext_fc", "#f3f3f3"), ec="none", zorder=2))
        if sg.get("t"):     # thread: minor diameter thin line on both halves
            pitch = _pitch(sg["t"]); rm = r0 - 0.6134 * pitch
            for sgn in (1, -1): ax.plot([X(x0), X(x1)], [Y(sgn * rm), Y(sgn * rm)], lw=0.3, color=INK, zorder=6)
        if sg.get("hex"):
            af = sg["hex"] / 2
            for sgn in (1, -1): ax.plot([X(x0), X(x1)], [Y(sgn * af * 0.5), Y(sgn * af * 0.5)], lw=0.3, color=INK, zorder=6)
        if sg.get("knurl"):
            for k in np.arange(x0 + 1, x1, 1.6): ax.plot([X(k), X(k + 1.2)], [Y(-r0), Y(-r0 * 0.15)], lw=0.15, color="#444", zorder=6)
    # vertical step lines
    rs = []
    for (x0, x1, r0, r1, sg) in prof: rs.append((x0, r0)); rs.append((x1, r1))
    for x in xs:
        rr = [r for (xx, r) in rs if abs(xx - x) < 1e-6]
        hi = max(rr); ax.plot([X(x), X(x)], [Y(-hi), Y(hi)], lw=0.7 if x in (0, Ltot) else 0.5, color=INK, zorder=5)
    # bores: outline in section
    for xa, xb, r in _bore_segments(spec, Ltot):
        ax.plot([X(xa), X(xb)], [Y(r), Y(r)], lw=0.6, color=INK, zorder=5)
        ax.plot([X(xa), X(xb)], [Y(-r), Y(-r)], lw=0.3, ls=(0, (3, 1.5)), color=INK, zorder=5)
        for xx in (xa, xb):
            if 0 < xx < Ltot: ax.plot([X(xx), X(xx)], [Y(0), Y(r)], lw=0.5, color=INK, zorder=5)
    # grooves (external)
    for gx0, w, Dg in spec.get("grooves", []):
        rg = Dg / 2; rr = _r_at(prof, gx0 + w / 2)
        for sgn in (1, -1):
            ax.add_patch(Rectangle((X(gx0), Y(sgn * rg) if sgn > 0 else Y(-rr)), w * s, (rr - rg) * s, fc="white", ec=INK, lw=0.5, zorder=7))
    # internal threads label marker
    # cross holes
    for hx, hD, hnote in spec.get("xholes", []):
        r = _r_at(prof, hx)
        ax.add_patch(Circle((X(hx), Y(-r * 0.45)), hD / 2 * s, fc="white", ec=INK, lw=0.5, zorder=8))
        ax.plot([X(hx - hD / 2), X(hx - hD / 2)], [Y(0), Y(r)], lw=0.3, ls=(0, (3, 1.5)), color=INK, zorder=8)
        ax.plot([X(hx + hD / 2), X(hx + hD / 2)], [Y(0), Y(r)], lw=0.3, ls=(0, (3, 1.5)), color=INK, zorder=8)
    cl(ax, (X(-4), Y(0)), (X(Ltot + 4), Y(0)))
    # ---------------- dimensions
    rmax = max(max(r0, r1) for (_, _, r0, r1, _) in prof)
    yb = Y(-rmax) - 5
    for (x0, x1, r0, r1, sg) in prof:
        hdim(ax, X(x0), X(x1), Y(-r0), Y(-r1), yb, f"{sg['L']:g}")
    hdim(ax, X(0), X(Ltot), Y(-prof[0][2]), Y(-prof[-1][3]), yb - 6.5, f"{Ltot:g} overall")
    # diameters: vertical dims spanning each segment (upper side labels)
    used = []
    for i, (x0, x1, r0, r1, sg) in enumerate(prof):
        xm = (x0 + x1) / 2
        if sg.get("hex"):
            lab = f"AF{sg['hex']:g} hex"
        elif sg.get("t"):
            lab = f"{sg['t']}"
        elif sg.get("lobes"):
            lab = f"Ø{sg['D']:g} over {sg['lobes']} lobes"
        else:
            lab = f"Ø{sg['D']:g}" + (f"→Ø{sg['D2']:g}" if sg.get("D2") else "")
        if sg.get("tol"): lab += f" {sg['tol']}"
        if sg.get("knurl"): lab += " knurl"
        r = max(r0, r1)
        ax.annotate("", xy=(X(xm), Y(r)), xytext=(X(xm), Y(-r)), arrowprops=dict(arrowstyle="<|-|>", lw=0.3, color=DIMC, mutation_scale=3.6, shrinkA=0, shrinkB=0), zorder=21)
        ty = Y(r) + 2.5 + (3.4 if any(abs(X(xm) - u) < 11 for u in used) else 0)
        used.append(X(xm))
        ax.plot([X(xm), X(xm)], [Y(r), ty - 1], lw=0.18, color=DIMC, zorder=20)
        _txt(ax, X(xm), ty, lab, size=4.3, va="bottom")
    # bore labels + depths (from left/right)
    k = 0
    for side, lst in (("L", spec.get("bl", [])), ("R", spec.get("br", []))):
        acc = 0
        for dpt, D, *rest in lst:
            th = rest[0] if rest else None
            xa = acc if side == "L" else Ltot - acc - dpt; xb = xa + dpt; acc += dpt
            lab = (f"{th}" if th else f"Ø{D:g}") + (" THRU" if dpt >= Ltot - 1e-6 else f" ↧{dpt:g}")
            p = (X((xa + xb) / 2), Y(D / 4))
            q = (X(xa + (xb - xa) * (0.3 if side == "L" else 0.7)) + (-14 if side == "L" else 14), Y(rmax) + 13 + 3.6 * (k % 3))
            leader(ax, p, q, lab, size=4.3); k += 1
    for gx0, w, Dg in spec.get("grooves", []):
        r = _r_at(prof, gx0 + w / 2)
        leader(ax, (X(gx0 + w / 2), Y(-Dg / 2)), (X(gx0 + w / 2) + 10, Y(-r) - 3), f"groove Ø{Dg:g} x {w:g} @ {gx0:g}", size=4.3)
    for hx, hD, hnote in spec.get("xholes", []):
        r = _r_at(prof, hx)
        leader(ax, (X(hx), Y(-r * 0.45)), (X(hx) + 12, Y(-r) - 1.5), f"Ø{hD:g} {hnote} @ {hx:g}", size=4.3)
    if spec.get("extra"): spec["extra"](ax, X, Y, s)
    if spec.get("notes"):
        ax.text(cell.x + cell.w - 1.5, cell.y + 1.5, "\n".join(spec["notes"]), fontsize=4.1, ha="right", va="bottom", color=NOTE, zorder=3, linespacing=1.25)

def _pitch(t):
    t = t.replace("x", "x").split("x")
    try: return float(t[1].split()[0])
    except Exception:
        coarse = {3: 0.5, 4: 0.7, 5: 0.8, 6: 1.0, 8: 1.25, 10: 1.5, 12: 1.75, 16: 2.0}
        try: return coarse.get(int(float(t[0].strip("M~"))), 1.0)
        except Exception: return 1.0

def _r_at(prof, x):
    for (x0, x1, r0, r1, sg) in prof:
        if x0 <= x <= x1: return r0 + (r1 - r0) * (x - x0) / max(x1 - x0, 1e-9)
    return prof[-1][3]

def _bore_breaks(spec, Ltot):
    out = []; acc = 0
    for dpt, *_ in spec.get("bl", []): out += [acc, acc + dpt]; acc += dpt
    acc = Ltot
    for dpt, *_ in spec.get("br", []): out += [acc - dpt, acc]; acc -= dpt
    for g0, w, _ in spec.get("grooves", []): out += [g0, g0 + w]
    return [min(max(o, 0), Ltot) for o in out]

def _bore_segments(spec, Ltot):
    segs = []; acc = 0
    for dpt, D, *_ in spec.get("bl", []): segs.append((acc, acc + dpt, D / 2)); acc += dpt
    acc = Ltot
    for dpt, D, *_ in spec.get("br", []): segs.append((acc - dpt, acc, D / 2)); acc -= dpt
    return segs

# ================================================================== FLAT RINGS / SEALS / WASHERS
def ring(cell, OD, ID, T, kind="flat", extra=None):
    ax = cell.ax
    s = pick_scale(OD + 30, OD + 22, cell.w - 30, cell.h - 22); cell.set_scale(s)
    cx = cell.x + cell.w * 0.36; cy = cell.y + cell.h / 2 - 1
    ax.add_patch(Circle((cx, cy), OD / 2 * s, fc="#dcdcdc", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Circle((cx, cy), ID / 2 * s, fc="white", ec=INK, lw=0.6, zorder=4))
    cl(ax, (cx - OD / 2 * s - 3, cy), (cx + OD / 2 * s + 3, cy)); cl(ax, (cx, cy - OD / 2 * s - 3), (cx, cy + OD / 2 * s + 3))
    a = math.radians(40)
    leader(ax, (cx + OD / 2 * s * math.cos(a), cy + OD / 2 * s * math.sin(a)), (cx + OD / 2 * s + 4, cy + OD / 2 * s + 1), f"Ø{OD:g} OD")
    leader(ax, (cx - ID / 2 * s * math.cos(a), cy - ID / 2 * s * math.sin(a)), (cx - OD / 2 * s - 4, cy - OD / 2 * s + 1), f"Ø{ID:g} ID")
    # section of one wall, own enlarged scale (ID at bottom, OD at top)
    s2 = min(6, (cell.h * 0.34) / max((OD - ID) / 2, 0.5), (cell.w * 0.17) / max(T, 0.5))
    sx = cell.x + cell.w * 0.80; w = (OD - ID) / 2 * s2; t = T * s2; y0 = cy - w / 2
    if kind == "lip":
        pts = [(sx - t / 2, y0), (sx + t / 2, y0), (sx + t / 2, y0 + w), (sx + t * 0.1, y0 + w), (sx - t * 0.05, y0 + w * 0.45), (sx - t / 2, y0 + w)]
        ax.add_patch(Polygon(pts, closed=True, fc="#9a9a9a", ec=INK, lw=0.5, hatch="xxxx", zorder=4))
    elif kind == "oring":
        ax.add_patch(Circle((sx, cy), w / 2, fc="#333", ec=INK, lw=0.5, zorder=4))
    else:
        ax.add_patch(Polygon([(sx - t / 2, y0), (sx + t / 2, y0), (sx + t / 2, y0 + w), (sx - t / 2, y0 + w)], closed=True, fc="#9a9a9a", ec=INK, lw=0.5, hatch="xxxx", zorder=4))
    ax.plot([sx - t / 2 - 4, sx + t / 2 + 4], [y0 - 2, y0 - 2], lw=0.2, ls=(0, (8, 2, 1.5, 2)), color="#555", zorder=3)
    ax.text(sx, y0 - 3, "toward axis", fontsize=3.8, ha="center", va="top", color="#555")
    hdim(ax, sx - t / 2, sx + t / 2, y0 + w, y0 + w, y0 + w + 4, f"{T:g}")
    vdim(ax, y0, y0 + w, sx + t / 2, sx + t / 2, sx + t / 2 + 4, f"{(OD - ID) / 2:g}", side="right")
    ax.text(sx, y0 + w + 9, f"SECTION  {scale_label(s2)}", fontsize=4.4, ha="center")
    if extra: ax.text(cell.x + 2, cell.y + cell.h - 10, extra, fontsize=4.3, va="top", color=NOTE)

# ================================================================== PLATES / OUTLINES WITH HOLE TABLE
def plate(cell, outline, holes, T, edge_note="", table_x=None, origin_note="datum X0/Y0 as shown", hatch_edge=True, slots=None):
    """outline: list of (x,y) mm (closed). holes: [(id, x, y, D, note)]."""
    ax = cell.ax; xs = [p[0] for p in outline]; ys = [p[1] for p in outline]
    W, Hh = max(xs) - min(xs), max(ys) - min(ys)
    tw = 66 if holes else 0
    s = pick_scale(W + 24, Hh + 30, cell.w - tw - 22, cell.h - 32); cell.set_scale(s)
    ox = cell.x + 12 - min(xs) * s; oy = cell.y + 18 - min(ys) * s + (cell.h - 32 - Hh * s) / 2
    P = lambda x, y: (ox + x * s, oy + y * s)
    ax.add_patch(Polygon([P(*p) for p in outline], closed=True, fc="#eeeeee", ec=INK, lw=0.7, zorder=3))
    for hid, x, y, D, note in holes:
        ax.add_patch(Circle(P(x, y), D / 2 * s, fc="white", ec=INK, lw=0.5, zorder=4))
        ax.text(*P(x + D / 2 + 0.6 / s, y + D / 2 + 0.6 / s), hid, fontsize=3.8, color=DIMC, zorder=6)
        c = P(x, y); ax.plot([c[0] - 1.2, c[0] + 1.2], [c[1], c[1]], lw=0.2, color="#555", zorder=5); ax.plot([c[0], c[0]], [c[1] - 1.2, c[1] + 1.2], lw=0.2, color="#555", zorder=5)
    for sl in (slots or []):
        (x0, y0, x1, y1, w, sid) = sl
        ang = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
        ax.add_patch(Polygon([P(x0 + nx, y0 + ny), P(x1 + nx, y1 + ny), P(x1 - nx, y1 - ny), P(x0 - nx, y0 - ny)], closed=True, fc="white", ec=INK, lw=0.5, zorder=4))
    # overall dims + datum
    hdim(ax, P(min(xs), 0)[0], P(max(xs), 0)[0], P(0, min(ys))[1], P(0, min(ys))[1], P(0, min(ys))[1] - 5, f"{W:.1f}".rstrip("0").rstrip("."))
    vdim(ax, P(0, min(ys))[1], P(0, max(ys))[1], P(min(xs), 0)[0], P(min(xs), 0)[0], P(min(xs), 0)[0] - 5, f"{Hh:.1f}".rstrip("0").rstrip("."))
    o = P(0, 0); ax.plot([o[0], o[0] + 5], [o[1], o[1]], lw=0.6, color="#c00000", zorder=9); ax.plot([o[0], o[0]], [o[1], o[1] + 5], lw=0.6, color="#c00000", zorder=9)
    ax.text(o[0] + 0.5, o[1] - 2.2, "X0 Y0", fontsize=3.8, color="#c00000", zorder=9)
    ax.text(cell.x + 2, cell.y + 3, f"t = {T:g}   {edge_note}", fontsize=4.4, va="bottom", zorder=6)
    if holes:
        tx = table_x or cell.x + cell.w - tw - 1; ty = cell.y + cell.h - 10
        hdr = ("ID", "X", "Y", "Ø / thread / depth")
        cw = (7, 9, 9, 40)
        xx = tx
        for h_, w_ in zip(hdr, cw):
            ax.add_patch(Rectangle((xx, ty - 3.6), w_, 3.6, fc="#dde6f3", ec=INK, lw=0.3, zorder=6)); ax.text(xx + 0.6, ty - 1.8, h_, fontsize=3.9, va="center", weight="bold", zorder=7); xx += w_
        for i, (hid, x, y, D, note) in enumerate(holes):
            yy = ty - 3.6 * (i + 2); xx = tx
            for v, w_ in zip((hid, f"{x:g}", f"{y:g}", note or f"Ø{D:g} THRU"), cw):
                ax.add_patch(Rectangle((xx, yy), w_, 3.6, fc="white", ec="#999", lw=0.2, zorder=6)); ax.text(xx + 0.6, yy + 1.8, v, fontsize=3.8, va="center", zorder=7); xx += w_
    return P, s

# ================================================================== PIPES / BENT TUBES (bend table)
def pipe(cell, pts, OD, wall, R, ends=("", "")):
    """pts: list of 3D points (mm) of the centre-line polyline (intersection points). Bend radius R."""
    ax = cell.ax; P = np.array(pts, float)
    # two projections: side (X-Z) and plan (X-Y) -> choose the two axes with the largest spread
    spans = P.max(axis=0) - P.min(axis=0); ax_pairs = [(0, 2, "X", "Z"), (1, 2, "Y", "Z"), (0, 1, "X", "Y")]
    ax_pairs.sort(key=lambda t: -(spans[t[0]] + spans[t[1]]))
    (a1, b1, la1, lb1), (a2, b2, la2, lb2) = ax_pairs[0], ax_pairs[1]
    tbl_w = 78
    vw = (cell.w - tbl_w - 10) / 2
    for k, (a, b, la, lb) in enumerate(((a1, b1, la1, lb1), (a2, b2, la2, lb2))):
        W_ = max(spans[a], 1) + OD; H_ = max(spans[b], 1) + OD
        s = pick_scale(W_ + 18, H_ + 18, vw - 6, cell.h - 22)
        ox = cell.x + 4 + k * vw + (vw - W_ * s) / 2 - (P[:, a].min() - OD / 2) * s
        oy = cell.y + 12 + (cell.h - 22 - H_ * s) / 2 - (P[:, b].min() - OD / 2) * s
        Q = [(ox + p[a] * s, oy + p[b] * s) for p in P]
        ax.plot(*zip(*Q), lw=max(OD * s * 2.835, 0.8) + 0.8, color=INK, solid_joinstyle="round", solid_capstyle="butt", zorder=4)
        ax.plot(*zip(*Q), lw=max(OD * s * 2.835 - 0.8, 0.3), color="#e6e6e6", solid_joinstyle="round", solid_capstyle="butt", zorder=5)
        ax.plot(*zip(*Q), lw=0.2, ls=(0, (8, 2, 1.5, 2)), color="#555", zorder=6)
        for i, q in enumerate(Q):
            ax.add_patch(Circle(q, 1.6, fc="white", ec=DIMC, lw=0.3, zorder=7)); ax.text(q[0], q[1], f"P{i}", fontsize=3.3, ha="center", va="center", color=DIMC, zorder=8)
        ax.text(cell.x + 4 + k * vw + vw / 2, cell.y + 8, f"VIEW {la}-{lb}  scale {scale_label(s)}", fontsize=4.4, ha="center")
        if k == 0: cell.set_scale(s)
    # bend table
    rows = []; total = 0.0
    segL = [np.linalg.norm(P[i + 1] - P[i]) for i in range(len(P) - 1)]
    angs = []
    for i in range(1, len(P) - 1):
        u = (P[i] - P[i - 1]); v = (P[i + 1] - P[i]); u /= np.linalg.norm(u); v /= np.linalg.norm(v)
        angs.append(math.degrees(math.acos(max(-1, min(1, u @ v)))))
    # straight lengths between tangent points
    tl = [R * math.tan(math.radians(a) / 2) for a in angs]
    for i, L in enumerate(segL):
        cut = (tl[i - 1] if i - 1 >= 0 else 0) + (tl[i] if i < len(tl) else 0)
        st = L - cut
        arc = (math.radians(angs[i]) * R) if i < len(angs) else 0
        total += st + arc
        rows.append((f"P{i}->P{i + 1}", f"{L:.1f}", f"{st:.1f}", f"{angs[i]:.1f}" if i < len(angs) else "-", f"{arc:.1f}" if i < len(angs) else "-"))
    tx, ty = cell.x + cell.w - tbl_w - 2, cell.y + cell.h - 10
    hdr = ("SEG", "C/L", "STRAIGHT", "BEND°", "ARC"); cw = (16, 14, 18, 14, 14); xx = tx
    for h_, w_ in zip(hdr, cw):
        ax.add_patch(Rectangle((xx, ty - 3.6), w_, 3.6, fc="#dde6f3", ec=INK, lw=0.3, zorder=6)); ax.text(xx + 0.6, ty - 1.8, h_, fontsize=3.9, va="center", weight="bold", zorder=7); xx += w_
    for i, r in enumerate(rows):
        yy = ty - 3.6 * (i + 2); xx = tx
        for v, w_ in zip(r, cw):
            ax.add_patch(Rectangle((xx, yy), w_, 3.6, fc="white", ec="#999", lw=0.2, zorder=6)); ax.text(xx + 0.6, yy + 1.8, v, fontsize=3.8, va="center", zorder=7); xx += w_
    yy = ty - 3.6 * (len(rows) + 2) - 1
    ax.text(tx, yy, f"Tube Ø{OD:g} x {wall:g} wall, bend R{R:g} (C/L)\nDeveloped length {total:.1f} mm (cut length + end allowances)", fontsize=4.2, va="top", zorder=7)
    yy -= 8
    ax.text(tx, yy, "Point coordinates (machine datums):", fontsize=4.0, va="top", weight="bold", zorder=7)
    for i, p in enumerate(P):
        ax.text(tx, yy - 3.4 * (i + 1), f"P{i}: X{p[0]:.1f}  Y{p[1]:.1f}  Z{p[2]:.1f}", fontsize=3.9, va="top", zorder=7)
    if ends[0] or ends[1]:
        ax.text(tx, yy - 3.4 * (len(P) + 1) - 1, f"P0 end: {ends[0]}\nP{len(P) - 1} end: {ends[1]}", fontsize=3.9, va="top", color=NOTE, zorder=7)
    return total

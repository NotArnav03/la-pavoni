"""Simplified, easier-to-read part cells:
  left-top    : shaded isometric view of the part
  left-bottom : KEY DIMENSIONS table in plain words (all mm, SI units), feature letters A, B, C ...
  right       : the drawing, with letter tags and length chain only (no arrow clutter)."""
import math
import numpy as np
from matplotlib.patches import Polygon, Circle, Rectangle
from matplotlib.collections import PolyCollection
from partdraw import Cell, hdim, vdim, cl, pick_scale, scale_label, INK, DIMC, NOTE, HATCH_FC, _pitch
import iso as ISO

LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"

# ------------------------------------------------------------------ sub-areas of a cell
class Sub:
    def __init__(self, parent, x, y, w, h):
        self.ax, self.x, self.y, self.w, self.h, self.parent = parent.ax, x, y, w, h, parent
    def set_scale(self, s): self.parent.set_scale(s)

def split(cell, left_frac=0.36):
    lw = cell.w * left_frac; top = cell.y + cell.h - 7.5
    isob = (cell.x + 1.5, cell.y + cell.h * 0.48, lw - 3, top - cell.y - cell.h * 0.48 - 1)
    tab = (cell.x + 1.5, cell.y + 1.5, lw - 3, cell.h * 0.48 - 3)
    draw = Sub(cell, cell.x + lw, cell.y, cell.w - lw, cell.h - 7)
    cell.ax.plot([cell.x + lw, cell.x + lw], [cell.y + 1, top], lw=0.25, color="#999", zorder=1)
    return isob, tab, draw

# ------------------------------------------------------------------ isometric thumbnail
def iso_thumb(ax, faces, box, label="ISOMETRIC"):
    if not faces: return
    x0, y0, w, h = box
    faces = [(np.asarray(P, float), c) for P, c in faces]
    pts = np.array([ISO.project(p)[:2] for P, _ in faces for p in P])
    mn, mx = pts.min(axis=0), pts.max(axis=0); span = np.maximum(mx - mn, 1e-6)
    s = min((w - 4) / span[0], (h - 7) / span[1])
    ox = x0 + (w - span[0] * s) / 2 - mn[0] * s; oy = y0 + 2 + (h - 7 - span[1] * s) / 2 - mn[1] * s
    polys, cols, dep = [], [], []
    for P, col in faces:
        P = np.asarray(P, float); n = np.cross(P[1] - P[0], P[2] - P[0]).astype(float); nn = np.linalg.norm(n)
        if nn < 1e-9 and len(P) > 3: n = np.cross(P[2] - P[0], P[3] - P[0]); nn = np.linalg.norm(n)
        if nn < 1e-9: continue
        n /= nn
        if n @ ISO.VIEW < -0.02: continue
        Q = np.array([ISO.project(p) for p in P])
        shade = 0.42 + 0.58 * max(0.0, n @ ISO.LIGHT) + 0.18 * max(0.0, n @ ISO.VIEW) ** 8
        polys.append([(ox + q[0] * s, oy + q[1] * s) for q in Q]); cols.append(np.clip(ISO._rgb(col) * shade, 0, 1)); dep.append(Q[:, 2].mean())
    o = np.argsort(dep)
    ax.add_collection(PolyCollection([polys[i] for i in o], facecolors=[cols[i] for i in o],
                                     edgecolors=[tuple(np.clip(cols[i] * 0.6, 0, 1)) for i in o], linewidths=0.06, zorder=3))
    ax.text(x0 + w / 2, y0 + h - 1, label, fontsize=4.4, ha="center", va="top", color="#555", weight="bold")

def faces_turned(spec, col):
    """Revolve the turned-part spec about X into mesh faces."""
    F = []; x = 0.0; Ltot = sum(s["L"] for s in spec["segs"])
    def bore(xm):
        r = 0.0; acc = 0
        for dpt, Dd, *_ in spec.get("bl", []):
            if acc <= xm < acc + dpt: r = max(r, Dd / 2)
            acc += dpt
        acc = Ltot
        for dpt, Dd, *_ in spec.get("br", []):
            if acc - dpt <= xm < acc: r = max(r, Dd / 2)
            acc -= dpt
        return r
    for sg in spec["segs"]:
        L = sg["L"]; r0 = sg.get("D", 1) / 2; r1 = sg.get("D2", sg.get("D", 1)) / 2
        shape = "round"
        if sg.get("hex"): r0 = r1 = sg["hex"] / 2 * 1.1547; shape = "hex"
        if sg.get("lobes"): shape = "lobed"
        ri = bore(x + L / 2)
        F += ISO.cyl((x, 0, 0), (x + L, 0, 0), r0, r1, col=col, shape=shape, n=32, ri=min(ri, min(r0, r1) - 0.3) if ri > 0 else 0)
        x += L
    return F

def faces_ring(OD, ID, T, col="#3a3a3a"):
    return ISO.cyl((0, 0, 0), (0, 0, T), OD / 2, col=col, n=48, ri=ID / 2)

def faces_item(item):
    out = []
    for it, lab, F, ex in ISO.items():
        if it == item: out += F
    return out

# ------------------------------------------------------------------ key-dimension table
def key_table(ax, box, rows, title="KEY DIMENSIONS  (all in mm)"):
    x0, y0, w, h = box
    ax.text(x0, y0 + h, title, fontsize=4.8, weight="bold", va="top")
    rh = min(3.7, (h - 5) / max(len(rows), 1)); fs = 4.4 if rh >= 3.4 else 3.9
    for i, (k, txt) in enumerate(rows):
        y = y0 + h - 5 - i * rh
        if k:
            ax.add_patch(Circle((x0 + 1.8, y - rh / 2 + 0.2), 1.45, fc="white", ec=DIMC, lw=0.35, zorder=5))
            ax.text(x0 + 1.8, y - rh / 2 + 0.2, k, fontsize=3.7, ha="center", va="center", color=DIMC, weight="bold", zorder=6)
        ax.text(x0 + 4.2, y - rh / 2 + 0.2, txt, fontsize=fs, va="center", zorder=6, clip_on=False)

def tag(ax, x, y, k):
    ax.add_patch(Circle((x, y), 1.6, fc="white", ec=DIMC, lw=0.4, zorder=25))
    ax.text(x, y, k, fontsize=3.9, ha="center", va="center", color=DIMC, weight="bold", zorder=26)

# ------------------------------------------------------------------ simplified turned part
def _seg_text(sg):
    L = sg["L"]
    if sg.get("hex"): return f"Hexagon {sg['hex']:g} across flats, {L:g} long"
    if sg.get("t"):
        t = sg["t"]; return f"External thread {t}" + ("" if "x" in t else f" x {_pitch(t):g}") + f", {L:g} long"
    if sg.get("lobes"): return f"{sg['lobes']}-lobe grip, Ø{sg['D']:g} over lobes" + (f" -> Ø{sg['D2']:g}" if sg.get("D2") else "") + f", {L:g} long"
    if sg.get("D2"): return f"Taper Ø{sg['D']:g} -> Ø{sg['D2']:g}, {L:g} long"
    return f"Diameter Ø{sg['D']:g}" + (f" (tol. {sg['tol']})" if sg.get("tol") else "") + (" knurled" if sg.get("knurl") else "") + f", {L:g} long"

def turned_simple(sub, spec):
    ax = sub.ax; segs = spec["segs"]
    for sg in segs:
        if "D" not in sg: sg["D"] = sg["hex"] * 1.1547
    Ltot = sum(s["L"] for s in segs); Dmax = max(max(s["D"], s.get("D2", 0)) for s in segs)
    s = pick_scale(Ltot + 20, Dmax + 24, sub.w - 14, sub.h - 30); sub.set_scale(s)
    ox = sub.x + (sub.w - Ltot * s) / 2; oy = sub.y + sub.h / 2 + 3
    X = lambda x: ox + x * s; Y = lambda r: oy + r * s
    rows = []; k = 0; x = 0
    prof = []
    for sg in segs:
        x0, x1 = x, x + sg["L"]; x = x1
        r0 = sg["D"] / 2; r1 = sg.get("D2", sg["D"]) / 2
        if sg.get("hex"): r0 = r1 = sg["hex"] / 2 * 1.1547
        prof.append((x0, x1, r0, r1, sg))
    bsegs = []; acc = 0
    for dpt, Dd, *rest in spec.get("bl", []): bsegs.append((acc, acc + dpt, Dd / 2, rest[0] if rest else None, "left", dpt)); acc += dpt
    acc = Ltot
    for dpt, Dd, *rest in spec.get("br", []): bsegs.append((acc - dpt, acc, Dd / 2, rest[0] if rest else None, "right", dpt)); acc -= dpt
    def br_at(xm):
        r = 0
        for a, b, rr, *_ in bsegs:
            if a <= xm < b: r = max(r, rr)
        return r
    # outline: upper half sectioned (hatched), lower half plain outside view
    for (x0, x1, r0, r1, sg) in prof:
        brs = sorted(set([x0, x1] + [v for a, b, *_ in bsegs for v in (a, b) if x0 < v < x1]))
        for a, b in zip(brs[:-1], brs[1:]):
            ra = r0 + (r1 - r0) * (a - x0) / (x1 - x0); rb = r0 + (r1 - r0) * (b - x0) / (x1 - x0); ri = br_at((a + b) / 2)
            if min(ra, rb) > ri:
                ax.add_patch(Polygon([(X(a), Y(ri)), (X(b), Y(ri)), (X(b), Y(rb)), (X(a), Y(ra))], closed=True, fc=spec.get("fc", HATCH_FC), hatch=spec.get("hatch", "////"), ec="none", zorder=3))
        ax.add_patch(Polygon([(X(x0), Y(-r0)), (X(x1), Y(-r1)), (X(x1), Y(0)), (X(x0), Y(0))], closed=True, fc="#f1f1f1", ec="none", zorder=2))
        for sgn in (1, -1): ax.plot([X(x0), X(x1)], [Y(sgn * r0), Y(sgn * r1)], lw=0.7, color=INK, zorder=5)
        if sg.get("t"):
            rm = r0 - 0.6134 * _pitch(sg["t"])
            for sgn in (1, -1): ax.plot([X(x0), X(x1)], [Y(sgn * rm), Y(sgn * rm)], lw=0.3, color=INK, zorder=6)
    for i, (x0, x1, r0, r1, sg) in enumerate(prof):
        hi = max(r0, r1, prof[i - 1][3] if i else 0)
        ax.plot([X(x0), X(x0)], [Y(-hi), Y(hi)], lw=0.5, color=INK, zorder=5)
    ax.plot([X(Ltot), X(Ltot)], [Y(-prof[-1][3]), Y(prof[-1][3])], lw=0.7, color=INK, zorder=5)
    for a, b, r, *_ in bsegs:
        ax.plot([X(a), X(b)], [Y(r), Y(r)], lw=0.55, color=INK, zorder=5)
        ax.plot([X(a), X(b)], [Y(-r), Y(-r)], lw=0.3, ls=(0, (3, 1.5)), color=INK, zorder=5)
        for xx in (a, b):
            if 0 < xx < Ltot: ax.plot([X(xx), X(xx)], [Y(0), Y(r)], lw=0.5, color=INK, zorder=5)
    cl(ax, (X(-3), Y(0)), (X(Ltot + 3), Y(0)))
    # letters: outer segments
    rmax = max(max(p[2], p[3]) for p in prof)
    for (x0, x1, r0, r1, sg) in prof:
        L_ = LETTERS[k]; k += 1
        tag(ax, X((x0 + x1) / 2), Y(max(r0, r1)) + 3.2, L_)
        rows.append((L_, _seg_text(sg) + f"  (from {x0:g} to {x1:g})"))
    for a, b, r, th, side, dpt in bsegs:
        L_ = LETTERS[k]; k += 1
        tag(ax, X((a + b) / 2), Y(r * 0.5), L_)
        what = f"Internal thread {th}" if th and th.startswith(("M", "G", "1/")) else (th if th else f"Bore Ø{2 * r:g}")
        if th and not th.startswith(("M", "G", "1/")): what = th
        depth = "right through" if abs(dpt - Ltot) < 1e-6 else f"{dpt:g} deep from the {side} end"
        rows.append((L_, f"{what}, {depth}"))
    for gx0, w, Dg in spec.get("grooves", []):
        L_ = LETTERS[k]; k += 1; tag(ax, X(gx0 + w / 2), Y(-rmax) - 3, L_)
        rows.append((L_, f"Groove Ø{Dg:g}, {w:g} wide, starts {gx0:g} from left"))
    for hx, hD, note in spec.get("xholes", []):
        r = max(p[2] for p in prof if p[0] <= hx <= p[1])
        ax.add_patch(Circle((X(hx), Y(-r * 0.45)), hD / 2 * s, fc="white", ec=INK, lw=0.5, zorder=8))
        L_ = LETTERS[k]; k += 1; tag(ax, X(hx) + hD / 2 * s + 2.5, Y(-r * 0.45), L_)
        rows.append((L_, f"Cross hole Ø{hD:g} ({note}), centre {hx:g} from left"))
    # length chain + overall (the only arrows on the drawing)
    yb = Y(-rmax) - 6
    for (x0, x1, r0, r1, sg) in prof: hdim(ax, X(x0), X(x1), Y(-r0), Y(-r1), yb, f"{sg['L']:g}", size=4.4)
    hdim(ax, X(0), X(Ltot), Y(-prof[0][2]), Y(-prof[-1][3]), yb - 6.5, f"{Ltot:g} overall", size=4.6)
    ax.text(sub.x + sub.w / 2, sub.y + sub.h - 2, "upper half = section, lower half = outside view", fontsize=3.8, ha="center", va="top", color="#666")
    if spec.get("extra"): spec["extra"](ax, X, Y, s)
    rows.append(("", f"Overall length {Ltot:g}, largest diameter Ø{Dmax:g}"))
    for n in spec.get("notes", []): rows.append(("", n))
    return rows

def ring_simple(sub, OD, ID, T, kind):
    ax = sub.ax
    s = pick_scale(OD + 20, OD + 20, sub.w * 0.55, sub.h - 14); sub.set_scale(s)
    cx, cy = sub.x + sub.w * 0.32, sub.y + sub.h / 2
    ax.add_patch(Circle((cx, cy), OD / 2 * s, fc="#cfcfcf", ec=INK, lw=0.6, zorder=3)); ax.add_patch(Circle((cx, cy), ID / 2 * s, fc="white", ec=INK, lw=0.6, zorder=4))
    tag(ax, cx + OD / 2 * s * 0.72, cy + OD / 2 * s * 0.72 + 2.5, "A"); tag(ax, cx, cy, "B")
    cl(ax, (cx - OD / 2 * s - 2, cy), (cx + OD / 2 * s + 2, cy))
    s2 = min(6, (sub.h * 0.4) / max((OD - ID) / 2, 0.5), (sub.w * 0.2) / max(T, 0.5))
    s2 = max([v for v in (6, 5, 4, 3, 2.5, 2, 1.5, 1.25, 1, 0.8, 0.5) if v <= s2] or [0.5])
    sx = sub.x + sub.w * 0.8; w = (OD - ID) / 2 * s2; t = T * s2; y0 = cy - w / 2
    if kind == "oring": ax.add_patch(Circle((sx, cy), w / 2, fc="#333", ec=INK, lw=0.5, zorder=4))
    elif kind == "lip": ax.add_patch(Polygon([(sx - t / 2, y0), (sx + t / 2, y0), (sx + t / 2, y0 + w), (sx + t * 0.1, y0 + w), (sx - t * 0.05, y0 + w * 0.45), (sx - t / 2, y0 + w)], closed=True, fc="#9a9a9a", ec=INK, lw=0.5, hatch="xxxx", zorder=4))
    else: ax.add_patch(Polygon([(sx - t / 2, y0), (sx + t / 2, y0), (sx + t / 2, y0 + w), (sx - t / 2, y0 + w)], closed=True, fc="#9a9a9a", ec=INK, lw=0.5, hatch="xxxx", zorder=4))
    tag(ax, sx + t / 2 + 3, cy, "C")
    ax.text(sx, y0 - 2.5, f"cross-section {scale_label(s2)}", fontsize=3.8, ha="center", va="top", color="#666")
    rows = [("A", f"Outside diameter Ø{OD:g}"), ("B", f"Inside diameter Ø{ID:g}"),
            ("C", (f"Cord thickness {T:g} (round section)" if kind == "oring" else f"Thickness {T:g}, radial width {(OD - ID) / 2:g}" + (" (V-lip profile, lip faces pressure)" if kind == "lip" else "")))]
    return rows

# ------------------------------------------------------------------ wrappers used by the sheet builder
def cell_turned(ax, x, y, w, h, it, name, mat, qty, conf, spec, col="#e6c98f"):
    c = Cell(ax, x, y, w, h, it, name, mat, qty, conf); isob, tab, sub = split(c)
    rows = turned_simple(sub, spec); key_table(ax, tab, rows)
    iso_thumb(ax, faces_turned(spec, "#c9956a" if spec.get("hatch") == "----" else col), isob)

def cell_ring(ax, x, y, w, h, it, name, mat, qty, conf, dims, note):
    OD, ID, T, kind = dims
    c = Cell(ax, x, y, w, h, it, name, mat, qty, conf); isob, tab, sub = split(c)
    rows = ring_simple(sub, OD, ID, T, kind)
    if note: rows.append(("", note))
    key_table(ax, tab, rows)
    iso_thumb(ax, faces_ring(OD, ID, T, "#3a3a3a" if kind != "flat" or "Fibre" not in mat else "#8a8a8a"), isob)

def cell_custom(ax, x, y, w, h, it, name, mat, qty, conf, fn, keys, left_frac=0.30):
    c = Cell(ax, x, y, w, h, it, name, mat, qty, conf); isob, tab, sub = split(c, left_frac)
    fn(sub); key_table(ax, tab, keys); iso_thumb(ax, faces_item(it), isob)

def cell_pipe(ax, x, y, w, h, it, name, mat, qty, conf, args, pipefn):
    c = Cell(ax, x, y, w, h, it, name, mat, qty, conf); isob, tab, sub = split(c, 0.24)
    pts, OD, wall, R, ends = args
    total = pipefn(sub, pts, OD, wall, R, ends)
    key_table(ax, tab, [("", f"Tube Ø{OD:g} x {wall:g} wall"), ("", f"Bend radius {R:g} (centre line)"), ("", f"Cut length {total:.0f}"),
                        ("", "Bend table on the right; P0, P1 ... are"), ("", "centre-line corner points.")])
    iso_thumb(ax, ISO.tube([tuple(p) for p in pts], OD, "#e9c35a" if "Brass" in mat else "#c87f4a"), isob)

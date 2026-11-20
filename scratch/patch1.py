import os
os.chdir(r"C:\coffee\drawings")

def edit(p, rep):
    s = open(p, encoding='utf-8').read()
    for a, b in rep:
        assert s.count(a) == 1, (p, a[:80]); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)

s = open('partdraw.py', encoding='utf-8').read()
i = s.index('    # section (own enlarged scale)'); j = s.index('    if extra: ax.text(cell.x + 2, cell.y + cell.h - 10', i)
new = '''    # section of one wall, own enlarged scale (ID at bottom, OD at top)
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
'''
s = s[:i] + new + s[j:]
open('partdraw.py', 'w', encoding='utf-8').write(s)

ear = '''def _eared(rc, pcd_r, er, n=3, start=90, res=720):
    pts = []
    for k in range(res):
        a = 2 * math.pi * k / res; r = rc
        for e in range(n):
            ea = math.radians(start + 360 / n * e); d = (a - ea + math.pi) % (2 * math.pi) - math.pi
            h = pcd_r * math.sin(d)
            if abs(h) <= er and abs(d) < math.pi / 2: r = max(r, pcd_r * math.cos(d) + math.sqrt(er * er - h * h))
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts

def ringnut_drawing(cell):'''
edit('parts_sheets.py', [
    ('def ringnut_drawing(cell):', ear),
    ('''    pts = []
    for k in range(360):
        a = math.radians(k); r = 49
        for e in range(3):
            ea = math.radians(90 + 120 * e); dd = abs((a - ea + math.pi) % (2 * math.pi) - math.pi)
            if dd < math.radians(12): r = max(r, 52 + math.sqrt(max(0, 49 - (52 * math.sin(dd)) ** 2)) * 0 + 7 * math.cos(dd * 6))
        pts.append((r * math.cos(a), r * math.sin(a)))''', '    pts = _eared(49, 52, 8)'),
    ('''    pts = []
    for k in range(360):
        a = math.radians(k); r = 42
        for e in range(3):
            ea = math.radians(90 + 120 * e); dd = abs((a - ea + math.pi) % (2 * math.pi) - math.pi)
            if dd < math.radians(11): r = max(r, 52 + 6.5 * math.cos(dd * 7))
        pts.append((r * math.cos(a), r * math.sin(a)))''', '    pts = _eared(42, 52, 7.5)'),
    ('3 ears on PCD 104 @ 90/210/330°. Chamfer', '3 ears R8 on PCD 104 @ 90/210/330°. Chamfer'),
    ('''    s = pick_scale(L + 40, OD + 30, cell.w * 0.42, cell.h - 30); cell.set_scale(s)
    ox, oy = cell.x + 14, cell.y + cell.h / 2 - 2''', '''    s = pick_scale(L + 30, OD + 26, cell.w - 20, cell.h * 0.42); cell.set_scale(s)
    ox, oy = cell.x + 16, cell.y + cell.h - 18 - OD / 2 * s - 6'''),
    ('''    s2 = pick_scale(circ + 20, L + 25, cell.w * 0.50, cell.h - 26)
    dx, dy = cell.x + cell.w * 0.47, cell.y + 12
    Q = lambda a, z: (dx + a / 360 * circ * s2, dy + z * s2)''', '''    s2 = pick_scale(circ + 20, L + 25, cell.w - 24, cell.h * 0.48)
    dx, dy = cell.x + 14, cell.y + 14
    Q = lambda a, z: (dx + ((a + 90) % 360) / 360 * circ * s2, dy + z * s2)'''),
    ('    ax.add_patch(Polygon([Q(0, 0), Q(360, 0), Q(360, L), Q(0, L)], closed=True, fc="#f2f2f2", ec=INK, lw=0.6, zorder=3))',
     '    ax.add_patch(Polygon([(dx, dy), (dx + circ * s2, dy), (dx + circ * s2, dy + L * s2), (dx, dy + L * s2)], closed=True, fc="#f2f2f2", ec=INK, lw=0.6, zorder=3))\n'
     '    for a_ in (0, 90, 180, 270): ax.text(*Q(a_, -4), f"{a_}°", fontsize=3.8, ha="center", color="#555")'),
    ('    ax.text(*Q(0, L + 3), f"DEVELOPED SHELL  (0° = +X towards group, CCW from above)   scale {scale_label(s2)}", fontsize=4.2, zorder=5)\n'
     '    hdim(ax, Q(0, 0)[0], Q(360, 0)[0], Q(0, 0)[1], Q(0, 0)[1], Q(0, 0)[1] - 4, f"{circ:.1f} = π x {OD}")',
     '    ax.text(dx, dy + L * s2 + 2, f"DEVELOPED SHELL (seam at -90°; 0° = +X towards group, CCW seen from above)   scale {scale_label(s2)}", fontsize=4.2, zorder=5)\n'
     '    hdim(ax, dx, dx + circ * s2, dy, dy, dy - 7, f"{circ:.1f} = π x {OD}")\n'
     '    for hid, a, z, d_, note in holes:\n'
     '        vdim(ax, dy, Q(a, z)[1], Q(a, z)[0], Q(a, z)[0], Q(a, z)[0] + 7, f"{z:g}", side="right", size=4)\n'
     '        hdim(ax, dx, Q(a, z)[0], dy + L * s2, Q(a, z)[1], dy + L * s2 + 6 + 4 * holes.index((hid, a, z, d_, note)), f"{((a + 90) % 360) / 360 * circ:.1f}", size=4)'),
    ('    ax.add_patch(Polygon([P(fl0, pz - 26), P(fl1, pz - 26), P(fl1, pz - 11), P(-rb, pz - 11), P(-rb, pz + 11), P(fl1, pz + 11), P(fl1, pz + 26), P(fl0, pz + 26)],',
     '    ax.add_patch(Polygon([P(fl0, pz - 24), P(fl1, pz - 24), P(fl1, pz - 11), P(-rb, pz - 11), P(-rb, pz + 11), P(fl1, pz + 11), P(fl1, pz + 24), P(fl0, pz + 24)],'),
    ('P(fl0, pz - 26)[1], P(0, 0)[1], P(0, pz - 32)[1]', 'P(fl0, pz - 24)[1], P(0, 0)[1], P(0, pz - 32)[1]'),
    ('P(fl0, pz + 26)[1], P(fl1, pz + 26)[1], P(0, pz + 30)[1]', 'P(fl0, pz + 24)[1], P(fl1, pz + 24)[1], P(0, pz + 30)[1]'),
    ('vdim(ax, P(0, pz - 26)[1], P(0, pz + 26)[1], P(fl0, 0)[0], P(fl0, 0)[0], P(fl0, 0)[0] - 12, "52 flange")',
     'vdim(ax, P(0, pz - 24)[1], P(0, pz + 24)[1], P(fl0, 0)[0], P(fl0, 0)[0], P(fl0, 0)[0] - 12, "48 flange")'),
    ('    holes = [("A", 13, 7, 5, "M6 ↧10, thd ↧8"), ("B", 13, 45, 5, "M6 ↧10, thd ↧8"), ("C", 13, 26, 6, "Ø6 THRU; Ø8 H7 ↧6 from back"),\n'
     '             ("D", 13, 26, 16, "seal recess Ø16 x 1.2 deep")]\n'
     '    P, s = plate(cell, [(0, 0), (26, 0), (26, 52), (0, 52)], holes, 10,',
     '    holes = [("A", 13, 5, 5, "M6 ↧10, thd ↧8"), ("B", 13, 43, 5, "M6 ↧10, thd ↧8"), ("C", 13, 24, 6, "Ø6 THRU; Ø8 H7 ↧6 from back"),\n'
     '             ("D", 13, 24, 16, "seal recess Ø16 x 1.2 deep")]\n'
     '    P, s = plate(cell, [(0, 0), (26, 0), (26, 48), (0, 48)], holes, 10,'),
    ('    hdim(ax, P(0, 0)[0], P(13, 0)[0], P(0, 52)[1], P(13, 52)[1], P(0, 52)[1] + 4, "13", size=4)\n'
     '    vdim(ax, P(0, 0)[1], P(0, 7)[1], P(26, 0)[0], P(26, 7)[0], P(26, 0)[0] + 4, "7", side="right", size=4)\n'
     '    vdim(ax, P(0, 7)[1], P(0, 45)[1], P(26, 7)[0], P(26, 45)[0], P(26, 0)[0] + 10, "38 c/c", side="right", size=4)',
     '    hdim(ax, P(0, 0)[0], P(13, 0)[0], P(0, 48)[1], P(13, 48)[1], P(0, 48)[1] + 4, "13", size=4)\n'
     '    vdim(ax, P(0, 0)[1], P(0, 5)[1], P(26, 0)[0], P(26, 5)[0], P(26, 0)[0] + 4, "5", side="right", size=4)\n'
     '    vdim(ax, P(0, 5)[1], P(0, 43)[1], P(26, 5)[0], P(26, 43)[0], P(26, 0)[0] + 10, "38 c/c", side="right", size=4)\n'
     '    vdim(ax, P(0, 0)[1], P(0, 24)[1], P(0, 0)[0], P(13, 24)[0], P(0, 0)[0] - 12, "24 port", size=4)'),
    ('[(18, 0, D["STK_Z"] - 23), (18, 0, 236), (16, -16, 210), (14, -32, 140), (18, -36, 126)], 8, 1, 12,',
     '[(18, 0, D["STK_Z"] - 23), (18, 0, 212), (16, -22, 178), (14, -34, 136), (18, -38, 124)], 8, 1, 12,'),
    ('''xholes=[(28, 3, "outlet to wand branch")], fc=HATCH_FC,''', '''xholes=[(28, 3, "outlet to wand branch")], fc=HATCH_FC, extra=_branch,'''),
    ('def valvebody_drawing(cell):', '''def _branch(ax, X, Y, s):
    ax.add_patch(Polygon([(X(21), Y(-7.5)), (X(35), Y(-7.5)), (X(35), Y(-14.5)), (X(21), Y(-14.5))], closed=True, fc="#f3f3f3", ec=INK, lw=0.6, zorder=6))
    ax.add_patch(Polygon([(X(23), Y(-14.5)), (X(33), Y(-14.5)), (X(33), Y(-22.5)), (X(23), Y(-22.5))], closed=True, fc="#f3f3f3", ec=INK, lw=0.6, zorder=6))
    for xx in (23.6, 32.4): ax.plot([X(xx), X(xx)], [Y(-14.5), Y(-22.5)], lw=0.3, color=INK, zorder=7)
    for xx in (26.5, 29.5): ax.plot([X(xx), X(xx)], [Y(-3), Y(-22.5)], lw=0.3, ls=(0, (3, 1.5)), color=INK, zorder=7)
    vdim(ax, Y(-7.5), Y(-14.5), X(35), X(35), X(35) + 4, "7", side="right", size=4)
    vdim(ax, Y(-14.5), Y(-22.5), X(33), X(33), X(35) + 4, "8 M10x1", side="right", size=4)
    hdim(ax, X(21), X(35), Y(-14.5), Y(-14.5), Y(-22.5) - 4, "Ø14 boss", size=4)

def valvebody_drawing(cell):'''),
])
edit('iso.py', [('tube([(18, 0, z - 23), (18, 0, 238), (16, -16, 210), (14, -32, 140), (18, -36, 126)], 8, CHR)',
                 'tube([(18, 0, z - 23), (18, 0, 212), (16, -22, 178), (14, -34, 136), (18, -38, 124)], 8, CHR)'),
                ('sphere((18, -36, 126), 4.5, CHR)', 'sphere((18, -38, 124), 4.5, CHR)')])
edit('views.py', [('M.append(Tube([(18, 0, z - 15), (18, 0, 236), (16, -16, 210), (14, -32, 140), (18, -36, 126)], 8, bias=0.5, name="wand"))',
                   'M.append(Tube([(18, 0, z - 15), (18, 0, 212), (16, -22, 178), (14, -34, 136), (18, -38, 124)], 8, bias=0.5, name="wand"))')])
print("patched")

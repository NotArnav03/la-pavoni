import os
os.chdir(r"C:\coffee\drawings")
def edit(p, rep):
    s = open(p, encoding='utf-8').read()
    for a, b in rep:
        assert s.count(a) == 1, (p, a[:90]); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
edit('joint.py', [
    ('"BREW GROUP ASSEMBLY - SECTION B-B (X-Z plane through group axis), lever at rest"', '"BREW GROUP ASSEMBLY - SECTION B-B, lever at rest"'),
    ('"GROUP-TO-BOILER JOINT - boss, flange, bolts, port seal, L-tube (all dimensions)"', '"GROUP-TO-BOILER JOINT - boss, flange, bolts, seal"'),
    ('''    _poly(ax, [P(fl0 - 10, pz - 24), P(fl0, pz - 24), P(fl0, pz + 24), P(fl0 - 10, pz + 24)], BR2, "\\\\\\\\\\\\\\\\")
    ax.add_patch(Rectangle(P(fl0 - 10, pz - 3), 10, 6, fc="#cfe8f5", ec=INK, lw=0.4, zorder=4))
    _poly(ax, [P(fl0 - 10, pz - 60), P(fl0 - 8.5, pz - 60), P(fl0 - 8.5, pz + 40), P(fl0 - 10, pz + 40)], BR, "////")''',
     '''    shx = D["BX"] + D["SH_D"] / 2 - gx
    _poly(ax, [P(shx, pz - 24), P(fl0, pz - 24), P(fl0, pz + 24), P(shx, pz + 24)], BR2, "\\\\\\\\\\\\\\\\")
    ax.add_patch(Rectangle(P(shx, pz - 3), fl0 - shx, 6, fc="#cfe8f5", ec=INK, lw=0.4, zorder=4))
    _poly(ax, [P(shx - 1.5, pz - 60), P(shx, pz - 60), P(shx, pz - 7), P(shx - 1.5, pz - 7)], BR, "////")
    _poly(ax, [P(shx - 1.5, pz + 7), P(shx, pz + 7), P(shx, pz + 40), P(shx - 1.5, pz + 40)], BR, "////")'''),
    ('        ax.add_patch(Rectangle(P(fl1 - 10, zb - 3), 10, 6, fc=ST, ec=INK, lw=0.5, zorder=5))', '        ax.add_patch(Rectangle(P(fl1 - 10, zb - 3), 10, 6, fc=ST, ec=INK, lw=0.5, zorder=5))'),
    ('    ax.plot(*zip(P(fl0 - 6, pz), P(-59, pz), P(-69, pz - 10), P(-69, pz - 60)),', '    ax.plot(*zip(P(shx + 4, pz), P(-59, pz), P(-69, pz - 10), P(-69, pz - 60)),'),
    ('    hdim(ax, P(-22, 0)[0], P(22, 0)[0], 0, 0, P(0, 236)[1], "Ø44 H8 bore [D]")', '    hdim(ax, P(-22, 0)[0], P(22, 0)[0], P(-22, 236)[1], P(22, 236)[1], P(0, 236)[1], "Ø44 H8 bore [D]")'),
    ('    hdim(ax, P(fl0 - 10, 0)[0], P(0, 0)[0], P(fl0 - 10, pz + 40)[1], P(0, 0)[1], P(0, pz + 52)[1], f"{-(fl0 - 10):g} shell outer to group axis")',
     '    hdim(ax, P(shx, 0)[0], P(0, 0)[0], P(shx, pz + 40)[1], P(0, pz + 52)[1], P(0, pz + 52)[1], f"{-shx:g} shell OD to group axis")'),
    ('    s = 2.0; ox, oy = 20 - 96 * s, 76 - (pz - 32) * s', '    s = 2.0; ox, oy = 36 - 96 * s, 76 - (pz - 32) * s'),
    ('''    xs = [(shell_x, f"X{shell_x:g} shell OD"), (shell_x + 4, ""), (D["PAD_X1"] - 7.5, ""), (D["PAD_X1"], f"X{D['PAD_X1']} pad face"), (fl1, f"X{fl1} flange"),
          (fl1 + 4, ""), (bw, f"X{bw:g} body"), (bw + 3, f"X{bw + 3:g} bore")]''',
     '''    xs = [(shell_x, f"X{shell_x:g} shell OD"), (fl1 - 10, "X113 bolt tip"), (shell_x + 4, ""), (D["PAD_X1"], f"X{D['PAD_X1']} pad face"), (fl1, f"X{fl1} flange"),
          (fl1 + 4, "X127 head"), (bw, f"X{bw:g} body"), (bw + 3, f"X{bw + 3:g} bore")]'''),
    ('''    leader(ax, P(D["PAD_X1"] - 4, pz + 19), (P(100, 0)[0], P(0, pz + 30)[1]), "pad: drill Ø5 ↧7.5, M6-6H ↧6 (2)")
    leader(ax, P(D["PAD_X1"] - 0.6, pz - 6), (P(100, 0)[0], P(0, pz - 12)[1]), "recess Ø16 x 1.2 for Cu washer 44")
    leader(ax, P(shell_x + 6, pz), (P(100, 0)[0], P(0, pz - 18)[1]), "port Ø6 x 4 (face) / Ø8 H7 x 4 (tube)")
    leader(ax, P(shell_x - 0.7, pz - 5), (P(100, 0)[0], P(0, pz - 26)[1]), "shell hole Ø14, pad Ag-brazed, R40 seat")''',
     '''    RX = P(bw + 14, 0)[0]
    leader(ax, P(D["PAD_X1"] - 4, pz + 19), (RX, P(0, pz + 40)[1]), "boss 69: drill Ø5 ↧7.5, M6-6H ↧6 (2)")
    leader(ax, P(D["PAD_X1"] - 0.6, pz - 6), (RX, P(0, pz + 10)[1]), "recess Ø16 x 1.2 for Cu washer 44")
    leader(ax, P(shell_x + 6, pz), (RX, P(0, pz + 4)[1]), "port Ø6 x 4 (face) / Ø8 H7 x 4 (tube)")
    leader(ax, P(shell_x - 0.7, pz - 9), (RX, P(0, pz - 12)[1]), "shell hole Ø14; boss Ag-brazed, R40 seat")'''),
    ('    leader(ax, P(D["PAD_X1"] + 2.5, pz + 19), (P(bw + 14, 0)[0], P(0, pz + 34)[1]), "flange hole Ø6.4 THRU (2)")',
     '    leader(ax, P(D["PAD_X1"] + 2.5, pz + 19), (RX, P(0, pz + 30)[1]), "flange hole Ø6.4 THRU (2)")'),
    ('    cx0, cy0 = 300, 120', '    cx0, cy0 = 352, 128'),
    ('    leader(ax, R_(X0 + 40 * math.cos(0.3), 40 * math.sin(0.3)), (R_(100, 0)[0] - 12, R_(0, 20)[1]), "R40 seat on Ø80 shell")',
     '    leader(ax, R_(X0 + 40 * math.cos(0.3), 40 * math.sin(0.3)), (R_(100, 0)[0] + 6, R_(0, 34)[1]), "R40 seat on Ø80 shell")'),
    ('    ax.text(cx0 + 5, cy0 - 40, "VIEW C', '    ax.text(cx0 - 5, cy0 - 40, "VIEW C'),
    ('    bx0, by0 = 255, 168', '    bx0, by0 = 268, 200'),
])
print("ok")

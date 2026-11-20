import os
os.chdir(r"C:\coffee\drawings")
s = open('parts_sheets.py', encoding='utf-8').read()
i = s.index('def lever_drawing(cell):'); j = s.index('def grid_drawing(cell):')
new = '''def lever_drawing(cell):
    """Item 49: lever = 2 fork cheeks + Ø16 boss + Ø11 rod (+ handle 53 on M8 stud). Side view + top view, lever laid horizontal."""
    ax = cell.ax; pin = 27.6; L = D["LEV_L"]; hl = D["HANDLE_L"]
    s = 0.5; cell.set_scale(s)
    ox, oy = cell.x + 16, cell.y + cell.h * 0.66
    P = lambda x, y: (ox + (x + 14) * s, oy + y * s)
    cheek = [(-14, -8), (pin + 10, -8), (pin + 22, -6), (pin + 22, 6), (pin + 10, 8), (-14, 8)]
    ax.add_patch(Polygon([P(*p) for p in cheek], closed=True, fc="#3a3a3a", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(pin + 22, -8), P(pin + 37, -8), P(pin + 37, 8), P(pin + 22, 8)], closed=True, fc="#d8d8d8", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(pin + 37, -5.5), P(L - hl, -5.5), P(L - hl, 5.5), P(pin + 37, 5.5)], closed=True, fc="#eeeeee", ec=INK, lw=0.6, zorder=3))
    ax.add_patch(Polygon([P(L - hl, -10), P(L, -11), P(L, 11), P(L - hl, 10)], closed=True, fc="#e8d2b0", ec=INK, lw=0.6, zorder=3, hatch="----"))
    for x in (0, pin): ax.add_patch(Circle(P(x, 0), 3.05 * s, fc="white", ec=INK, lw=0.5, zorder=4))
    cl(ax, P(-18, 0), P(L + 4, 0))
    yb = P(0, -11)[1] - 4
    hdim(ax, P(0, 0)[0], P(pin, 0)[0], P(0, 0)[1], P(pin, 0)[1], yb, f"{pin} pin c/c", size=4)
    hdim(ax, P(-14, 0)[0], P(0, 0)[0], P(-14, -8)[1], P(0, 0)[1], yb, "14", size=4)
    hdim(ax, P(pin, 0)[0], P(pin + 22, 0)[0], P(pin, 0)[1], P(pin + 22, -6)[1], yb, "22", size=4)
    hdim(ax, P(pin + 22, 0)[0], P(pin + 37, 0)[0], P(pin + 22, -8)[1], P(pin + 37, -8)[1], yb, "15 boss", size=4)
    hdim(ax, P(pin + 37, 0)[0], P(L - hl, 0)[0], P(pin + 37, -5.5)[1], P(L - hl, -5.5)[1], yb, f"{L - hl - pin - 37:.1f} rod Ø11 (+15 in boss)", size=4)
    hdim(ax, P(L - hl, 0)[0], P(L, 0)[0], P(L - hl, -10)[1], P(L, -11)[1], yb, f"{hl} handle", size=4)
    hdim(ax, P(0, 0)[0], P(L, 0)[0], P(0, 0)[1], P(L, -11)[1], yb - 7, f"{L} fulcrum to handle end", size=4.4)
    vdim(ax, P(0, -8)[1], P(0, 8)[1], P(-14, -8)[0], P(-14, 8)[0], P(-14, 0)[0] - 4, "16", size=4)
    leader(ax, P(pin + 30, 8), (P(pin + 30, 0)[0] + 8, P(0, 8)[1] + 9), "boss Ø16, rod pressed ↧15 + Ag-braze")
    leader(ax, P(0, 0), (P(0, 0)[0] - 2, P(0, 8)[1] + 9), "Ø6.1 H8 fulcrum")
    leader(ax, P(pin, 0), (P(pin, 0)[0] + 2, P(0, 8)[1] + 15), "Ø6.1 H8 rod pin")
    leader(ax, P(L - 40, 10.5), (P(L - 40, 0)[0] - 6, P(0, 11)[1] + 9), "handle Ø20→Ø22, M8 insert ↧25")
    # top view
    oy2 = cell.y + cell.h * 0.26
    Q = lambda x, y: (ox + (x + 14) * s, oy2 + y * s)
    for yy in (9, -12):
        ax.add_patch(Polygon([Q(-14, yy), Q(pin + 22, yy), Q(pin + 22, yy + 3), Q(-14, yy + 3)], closed=True, fc="#3a3a3a", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Polygon([Q(pin + 22, -8), Q(pin + 37, -8), Q(pin + 37, 8), Q(pin + 22, 8)], closed=True, fc="#d8d8d8", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Polygon([Q(pin + 37, -5.5), Q(L - hl, -5.5), Q(L - hl, 5.5), Q(pin + 37, 5.5)], closed=True, fc="#eeeeee", ec=INK, lw=0.5, zorder=3))
    ax.add_patch(Polygon([Q(L - hl, -10), Q(L, -11), Q(L, 11), Q(L - hl, 10)], closed=True, fc="#e8d2b0", ec=INK, lw=0.5, zorder=3))
    for yy in (-16, 16): ax.plot([Q(0, yy)[0], Q(0, yy)[0]], [Q(0, yy)[1], Q(0, -yy)[1]], lw=0.2, color="#555", ls=(0, (3, 1.5)), zorder=4)
    vdim(ax, Q(0, -12)[1], Q(0, 12)[1], Q(-14, -12)[0], Q(-14, 12)[0], Q(-14, 0)[0] - 4, "24", size=4)
    vdim(ax, Q(0, -9)[1], Q(0, 9)[1], Q(pin + 22, -9)[0], Q(pin + 22, 9)[0], Q(pin + 22, 0)[0] + 3, "18 gap", size=4, side="right")
    ax.text(*Q(L / 2, -22), "TOP VIEW: cheeks 3 thick, 18 gap straddles column (16) + rod eye", fontsize=4.2, ha="center")
    ax.text(cell.x + 3, cell.y + 3, f"Assembled: fulcrum X{D['FX']} Z{D['FZ']}, rod pin X{D['ROD_PIN_X']} Z{D['ROD_PIN_Z']}, rest {D['LEV_ANG']}° below horizontal. Ratio {L}/{pin} = {L / pin:.1f}:1.",
            fontsize=4.1, va="bottom", color=NOTE)

'''
s = s[:i] + new + s[j:]
open('parts_sheets.py', 'w', encoding='utf-8').write(s)
print("ok")

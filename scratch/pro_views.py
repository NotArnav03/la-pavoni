import os
os.chdir(r"C:\coffee\professional")
s = open('views.py', encoding='utf-8').read()
i = s.index('# ----------------------------------------------------------------- key dimensions'); j = s.index('def rounded_trap')
s = s[:i] + '''# ----------------------------------------------------------------- key dimensions (single source of truth) - PROFESSIONAL v3.1 copper/brass
COPPER, BRASSP = "#e0956a", "#ecc865"
D = dict(
    L=290, W_REAR=200, W_FRONT=186, BASE_R=58, BASE_H=65, RUB_H=10,
    BX=80,                      # boiler axis from base rear
    FOOT_D=112, FOOT_Z=76,      # brass foot ring Z65-76
    SH_D=100, SH_Z1=254,        # copper shell OD [D 100 mm], shoulder start
    SEAM_Z=192,                 # upper/lower shell joint band
    SHO_Z=274, NECK_D=46, NECK_Z=284, CAP_Z=324, TOP=345, KNOB_D=58,
    GX=179,                     # group axis (BX + 99)
    PORT_Z=218, BOLT_CC=44, ROD_PIN_X=179, ROD_PIN_Z=271.4, COL_X0=148, COL_X1=162,
    PF_Z0=160, BELL_Z0=176, BELL_Z1=198, BELL_D=76, BODY_Z1=262, YOKE_Z1=291, ACORN_Z=312,
    SPOUT_Z=132, PF_D=62, BODY_D=58,
    FX=154, FZ=283,
    LEV_ANG=24.9, LEV_L=272, HANDLE_L=101, HANDLE_D=24,
    SG_X=50, SG_Y=-56, SG_Z0=104, SG_Z1=241, GAUGE_Z=282, GAUGE_D=44,
    SV_X=108, SV_Y=18, PAD_X0=128, PAD_X1=138, FL_X1=143, PAD_W=60, PAD_H=26, SHELL_TOP=254,
    STK_X=45, STK_Y0=-40, STK_Y1=20, STK_D=37, STK_Z=300, STK_KNOB_Y=-62, STK_X0=-1,
    PF_ANG=242,
    TRAY_X0=140, TRAY_L=136, TRAY_W=120,
    SW_X=62, SW_Z=38, SW_W=22, SW_H=30,
    BADGE_Y=-34, BADGE_Z=38, BADGE_D=38,
)

''' + s[j:]
i = s.index('def model():'); j = s.index('class ViewPort:')
s = s[:i] + '''def model():
    d = D; M = []
    bx, gx = d["BX"], d["GX"]
    # base (brass shell) + plastic sub-base + grid
    M.append(Loft(rounded_trap(d["W_REAR"], d["W_FRONT"], d["L"], d["BASE_R"]), d["RUB_H"],
                  rounded_trap(d["W_REAR"] - 14, d["W_FRONT"] - 14, d["L"] - 14, d["BASE_R"] - 7, x0=7), d["BASE_H"], fc=BRASSP, name="base"))
    M.append(Loft(rounded_trap(d["W_REAR"] + 2, d["W_FRONT"] + 2, d["L"] + 2, d["BASE_R"] + 1, x0=-1), 4,
                  rounded_trap(d["W_REAR"] + 2, d["W_FRONT"] + 2, d["L"] + 2, d["BASE_R"] + 1, x0=-1), d["RUB_H"], fc=RUBBER, bias=2, name="sub-base"))
    for fx_, fy_ in ((30, -70), (30, 70), (255, -62), (255, 62)):
        M.append(Cyl((fx_, fy_, 0), (fx_, fy_, 4), 9, fc=RUBBER, name="foot"))
    tr = rounded_trap(d["TRAY_W"], d["TRAY_W"] - 6, d["TRAY_L"], 24, x0=d["TRAY_X0"])
    M.append(Loft(tr, 62, tr, 64, fc="#2b2b2b", bias=1, name="tray rim"))
    tg = rounded_trap(d["TRAY_W"] - 8, d["TRAY_W"] - 14, d["TRAY_L"] - 8, 20, x0=d["TRAY_X0"] + 4)
    M.append(Loft(tg, 64, tg, 64.8, fc=BRASSP, bias=1.2, name="grid"))
    M.append(Holes([(d["TRAY_X0"] + 14 + i * 12.2, -45 + j * 12.8) for i in range(10) for j in range(8) if not (abs(i - 4.5) < 1 and abs(j - 3.5) < 1)], 3.6, 64.9))
    sx, sz, sw, sh = d["SW_X"], d["SW_Z"], d["SW_W"], d["SW_H"]
    M.append(Box(sx - sw / 2 - 2, sx + sw / 2 + 2, -101, -97, sz - sh / 2 - 2, sz + sh / 2 + 2, fc="#222222", bias=3, name="switch"))
    M.append(Box(sx - sw / 2, sx + sw / 2, -101.5, -98, sz - sh / 2, sz + sh / 2, fc="#1f8a3a", bias=4))
    M.append(Cyl((285, d["BADGE_Y"], d["BADGE_Z"]), (289, d["BADGE_Y"], d["BADGE_Z"]), d["BADGE_D"] / 2, fc="#d93030", bias=3, name="badge"))
    M.append(Cyl((-6, 45, 30), (6, 45, 30), 8, fc=STEEL, bias=3, name="gland")); M.append(Cyl((0, 45, 30), (3, 45, 30), 11, fc=STEEL, shape="hex", bias=3))
    M.append(Tube([(-6, 45, 30), (-30, 50, 20), (-48, 54, 8)], 7, fc="#222222", cap="butt", name="cord"))
    M.append(Cyl((bx, 0, 65), (bx, 0, d["FOOT_Z"]), d["FOOT_D"] / 2, d["SH_D"] / 2 + 2, fc=BRASSP, name="foot"))
    M.append(Cyl((bx, 0, d["FOOT_Z"]), (bx, 0, d["SH_Z1"]), d["SH_D"] / 2, fc=COPPER, name="shell"))
    M.append(Cyl((bx, 0, d["SEAM_Z"] - 2), (bx, 0, d["SEAM_Z"] + 2), d["SH_D"] / 2 + 0.6, fc=COPPER, bias=0.5, name="seam"))
    M.append(Cyl((bx, 0, d["SH_Z1"]), (bx, 0, d["SHO_Z"]), d["SH_D"] / 2, d["NECK_D"] / 2 + 1, fc=COPPER, name="shoulder"))
    M.append(Cyl((bx, 0, d["SHO_Z"]), (bx, 0, d["NECK_Z"]), d["NECK_D"] / 2, fc=BRASSP, name="neck"))
    M.append(Cyl((bx, 0, d["NECK_Z"]), (bx, 0, d["CAP_Z"]), 14, 19, fc=WOOD, name="capcone"))
    M.append(Cyl((bx, 0, d["CAP_Z"]), (bx, 0, d["TOP"]), d["KNOB_D"] / 2, fc=WOOD, shape="lobed", name="capknob"))
    sgx, sgy = d["SG_X"], d["SG_Y"]
    for z in (d["SG_Z0"], d["SG_Z1"]):
        M.append(Box(sgx - 9, sgx + 9, sgy - 9, sgy + 9, z - 9, z + 9, fc=BRASSP, bias=1))
    M.append(Cyl((sgx, sgy, d["SG_Z0"] + 9), (sgx, sgy, d["SG_Z1"] - 9), 9, fc="#dff0f8", bias=1, name="sg guard"))
    M.append(Cyl((sgx, sgy, d["SG_Z0"] - 15), (sgx, sgy, d["SG_Z0"] - 9), 8.5, fc=BRASSP, shape="hex", bias=1))
    M.append(Cyl((sgx, sgy, d["SG_Z1"] + 9), (sgx, sgy, d["GAUGE_Z"] - 20), 6, fc=BRASSP, bias=1, name="gauge adapter"))
    M.append(Cyl((sgx, sgy, d["GAUGE_Z"] - 22), (sgx, sgy, d["GAUGE_Z"] - 16), 8.1, fc=BRASSP, shape="hex", bias=1))
    M.append(Cyl((sgx, sgy + 12, d["GAUGE_Z"]), (sgx, sgy - 14, d["GAUGE_Z"]), d["GAUGE_D"] / 2, fc=BRASSP, bias=1.5, name="gauge"))
    M.append(Cyl((sgx, sgy - 14, d["GAUGE_Z"]), (sgx, sgy - 15, d["GAUGE_Z"]), 19, fc="#f8f8f0", bias=1.6, name="dial"))
    z = d["STK_Z"]; x = d["STK_X"]
    M.append(Cyl((x, -12, 262), (x, -12, z - 6), 7, fc=BRASSP, name="steam riser"))
    M.append(Cyl((x, d["STK_Y0"], z), (x, d["STK_Y1"], z), 7.5, fc=BRASSP, name="steam valve"))
    M.append(Cyl((x, d["STK_Y0"], z), (x, d["STK_Y0"] - 8, z), 8, fc=BRASSP, shape="hex"))
    M.append(Cyl((x, d["STK_Y0"] - 8, z), (x, d["STK_KNOB_Y"] + 22, z), 3, fc=BRASSP))
    M.append(Cyl((x, d["STK_KNOB_Y"] + 22, z), (x, d["STK_KNOB_Y"], z), d["STK_D"] / 2, d["STK_D"] / 2 - 3, fc=WOOD, shape="lobed", name="steam knob"))
    M.append(Tube([(x, d["STK_Y1"], z), (x + 8, d["STK_Y1"] + 4, z), (150, 24, z)], 8, fc=BRASSP, name="steam pipe"))
    M.append(Cyl((150, 24, z + 6), (150, 24, z - 6), 8.1, fc=BRASSP, shape="hex", name="swivel"))
    M.append(Tube([(150, 24, z - 6), (156, 26, z - 14), (196, 34, 236)], 8, fc=BRASSP, bias=0.5, name="wand"))
    M.append(Cyl((196, 34, 236), (196, 34, 230), 4.5, fc=BRASSP))
    M.append(Cyl((d["SV_X"], d["SV_Y"], 262), (d["SV_X"], d["SV_Y"], 268), 8.1, fc=BRASSP, shape="hex"))
    M.append(Cyl((d["SV_X"], d["SV_Y"], 268), (d["SV_X"], d["SV_Y"], 290), 11, fc=BRASSP, name="sv cup"))
    M.append(Tube([(d["SV_X"] + 9, d["SV_Y"] + 6, 276), (136, 34, 266), (140, 36, 240), (140, 36, 120), (146, 36, 66)], 5, fc=COPPER, name="drain"))
    pz = d["PORT_Z"]; bc = d["BOLT_CC"] / 2
    M.append(Box(bx + 46, d["PAD_X1"], -30, 30, pz - 13, pz + 13, fc=BRASSP, name="pad"))
    M.append(Box(d["PAD_X1"], d["FL_X1"], -30, 30, pz - 13, pz + 13, fc=BRASSP, name="flange"))
    for yy in (-bc, bc):
        M.append(Cyl((d["FL_X1"], yy, pz), (d["FL_X1"] + 4, yy, pz), 5.77, fc=STEEL, shape="hex", bias=1))
    M.append(Cyl((d["FL_X1"], 0, pz), (gx - 27, 0, pz), 11, fc=BRASSP))
    M.append(Cyl((gx, 0, d["PF_Z0"]), (gx, 0, d["BELL_Z0"] + 12), d["PF_D"] / 2 - 3, d["PF_D"] / 2, fc=BRASSP, name="pf"))
    M.append(Cyl((gx, 0, d["BELL_Z0"]), (gx, 0, d["BELL_Z1"]), d["BELL_D"] / 2, fc=BRASSP, name="bell"))
    M.append(Cyl((gx, 0, d["BELL_Z1"]), (gx, 0, 210), d["BELL_D"] / 2, d["BODY_D"] / 2, fc=BRASSP))
    M.append(Cyl((gx, 0, 210), (gx, 0, d["BODY_Z1"]), d["BODY_D"] / 2, fc=BRASSP, name="cyl"))
    M.append(Box(d["COL_X0"], d["COL_X1"], -8, 8, d["BODY_Z1"] - 4, d["YOKE_Z1"], fc=BRASSP, name="column"))
    M.append(Cyl((gx, 0, d["BODY_Z1"]), (gx, 0, 299), 5, fc=STEEL, name="rod"))
    M.append(Cyl((gx, 0, 295), (gx, 0, 301), 7.5, fc=BRASSP, shape="hex"))
    M.append(Cyl((gx, 0, 301), (gx, 0, d["ACORN_Z"]), 7.5, 5, fc=BRASSP, shape="hex", name="acorn"))
    M.append(Cyl((gx, 0, 146), (gx, 0, d["PF_Z0"]), 6, 7, fc=BRASSP, name="spout"))
    M.append(Tube([(gx, -5, 147), (gx, -15, d["SPOUT_Z"] + 3)], 6, fc=BRASSP)); M.append(Tube([(gx, 5, 147), (gx, 15, d["SPOUT_Z"] + 3)], 6, fc=BRASSP))
    a = math.radians(d["PF_ANG"]); ux, uy = math.cos(a), math.sin(a)
    p = lambda r, zz: (gx + r * ux, r * uy, zz)
    M.append(Tube([p(30, 172), p(54, 170)], 15, fc=BRASSP, name="pf arm")); M.append(Tube([p(54, 170), p(154, 165)], 26, fc=WOOD, name="pf handle"))
    la = math.radians(d["LEV_ANG"]); lx, lz = math.cos(la), -math.sin(la)
    q = lambda r: (d["FX"] + r * lx, 0, d["FZ"] + r * lz)
    M.append(Tube([q(-14), q(60)], 22, fc="#b8952e", name="fork"))
    M.append(Tube([q(55), q(d["LEV_L"] - d["HANDLE_L"] + 4)], 11, fc=BRASSP, name="lever rod"))
    M.append(Tube([q(d["LEV_L"] - d["HANDLE_L"]), q(d["LEV_L"])], d["HANDLE_D"], fc=WOOD, name="lever handle"))
    M.append(Cyl((d["FX"], -13, d["FZ"]), (d["FX"], 13, d["FZ"]), 3.5, fc=STEEL, bias=2, name="fulcrum pin"))
    M.append(Cyl((d["ROD_PIN_X"], -13, d["ROD_PIN_Z"]), (d["ROD_PIN_X"], 13, d["ROD_PIN_Z"]), 3.5, fc=STEEL, bias=2, name="rod pin"))
    return M

''' + s[j:]
s = s.replace('"""Simple 3D primitive model of the Europiccola v2.2', '"""Simple 3D primitive model of the La Pavoni Professional v3.1 (copper/brass)')
s = s.replace('CHROME, BRASS, WOOD, BASEC, RUBBER, STEEL = "#ececec", "#e6c98f", "#d2ae7e", "#cfeee3", "#2b2b2b", "#d0d0d0"',
              'CHROME, BRASS, WOOD, BASEC, RUBBER, STEEL = "#ecc865", "#e6c98f", "#8a5434", "#ecc865", "#2b2b2b", "#d0d0d0"')
open('views.py', 'w', encoding='utf-8').write(s)
import views; print(len(views.model()))

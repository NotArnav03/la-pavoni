"""Simplified Professional part-drawing build: isometric + plain-language key table for every part (SI units, mm)."""
import pro_parts as PP
import parts_sheets as PS
import simple_parts as SP
from partdraw import pipe as _pipe

TURNED, RINGS, PIPES, grid = PP.TURNED, dict(PP.RINGS), PP.PIPES, PP.grid
CU, BR, BRB, POL = PP.CU, PP.BR, PP.BRB, PP.POL
RINGS.pop(47, None)
RINGS[90] = ("Frother O-ring", "Silicone VMQ", 1, "D/E", (12, 8, 2, "oring"), "Auto-frother O-ring [D].")
TURNED[24] = ("Plug M10x1, slotted (bottom = item 70)", BRB + POL, 1, "V/E", dict(segs=[dict(L=3, D=14), dict(L=6, D=10, t="M10x1")], notes=["Slot 1.6 wide x 1.5 deep."]))
TURNED[40] = ("Brass washer with holes", "Brass", 1, "D/E", dict(segs=[dict(L=1, D=20)], bl=[(1, 10.5)], notes=["4 holes Ø2 on 15 circle (lets water past) [D type]."]))

KEYS = {
 1: [("", "Copper tube, outside Ø100 [D], wall 1.5, inside Ø97"), ("", "Length 122 (machine height Z70 to Z192)"),
     ("H1", "Hole Ø12.5 for lower sight glass, centre Z104,"), ("", "  236° round from the group direction"), ("", "Bottom 6 sits in the brass foot socket (brazed)"),
     ("", "Top joins seam ring 84 at Z192")],
 85: [("", "Copper tube, outside Ø100 [D], wall 1.5"), ("", "Length 70 (Z192 to Z262), top 8 inside the dome"),
      ("H1", "Hole Ø14 for the group port, centre Z218, facing front"), ("H2", "Hole Ø12.5 for upper sight glass, Z241, 236°")],
 35: [("", "Bell: Ø76 outside, 22 tall (bottom face = Z176)"), ("", "Skirt: inside Ø64.5, 12 deep, 2 bayonet ramps"),
      ("", "Gasket groove: Ø60 outside / Ø50 inside, 5.5 deep"), ("", "Screen recess Ø54 x 1 deep"), ("", "Sleeve bore Ø50.2 (H8), 57.5 deep"),
      ("", "Body Ø58 outside, top 86 above the bell face"), ("", "Top: rod hole Ø10.5, seal recess Ø20 x 6 deep"),
      ("", "Flange to boiler: 60 x 26 x 5 thick"), ("", "  2 holes Ø6.4, 44 apart (side by side)"), ("", "Water port Ø8, 42 above bell face (Z218)"),
      ("", "Lever column 14 x 16, top 115 above bell face"), ("", "Fulcrum bore Ø10.1 (H8), 25 behind the axis")],
 69: [("", "Block 60 wide x 26 tall"), ("", "8 thick on the centre line, 15 at the ends"), ("", "Back face curved R50 to sit on the Ø100 shell"),
      ("A,B", "2 tapped holes M6, 44 apart, 6 deep"), ("C", "Port: Ø6 at the face, Ø8 at the back (tube)"), ("D", "O-ring groove Ø11 / Ø16.2, 2 deep")],
 4: [("", "Internal thread M80 x 1.5 right through [D]"), ("", "Ring outside Ø98, 12 thick"), ("", "3 ears, radius 8, on a Ø104 circle"),
     ("", "Each ear tapped M5 for the element screws [D]")],
 6: [("", "Flange Ø84 x 6, stainless steel"), ("", "3 ears with Ø5.5 holes on a Ø104 circle"), ("", "Coil: 6 turns, Ø56 centre line, 80 tall"),
     ("", "1000 W at 230 V (52.9 Ω cold) [D]"), ("", "2 terminals + earth stud, M4"), ("", "Pressurestat port G1/8 (ISO 228, Ø9.73)"),
     ("", "Seals with O-ring 3.53 x 73.98 [D]")],
 61: [("", "Length 290 [D], width 200 rear [D] / 186 front"), ("", "Shell height 55 (Z10 to Z65), brass 0.8 thick"),
      ("", "Boiler hole Ø82, centre 80 from the back"), ("", "Tray opening 136 x 120, starts 140 from back"), ("", "Switch cut-out 22 x 30 in the left wall"),
      ("", "Cable hole Ø16.5 in the back wall, Z30"), ("", "Badge: 2 pin holes Ø2.2 in the front wall")],
 79: [("", "Plastic plate 292 x 202, rim 6 tall, 2.5 wall"), ("", "4 foot holes Ø6"), ("", "Centre post with M4 screw into the base")],
 62: [("", "Plate 128 x 112, 0.8 thick brass"), ("", "76 holes Ø7.2 in a 10 x 8 grid"), ("", "Hole spacing 12.2 x 12.8, centre hole Ø5")],
 71: [("", "Dial Ø40 [D], bezel Ø44, case 26 deep"), ("", "Stem at the bottom: G1/8 male, 14 long"), ("", "Range 0 to 250 kPa (dial reads 0-2.5 bar)")],
 19: [("", "Block 18 x 18 x 18"), ("", "Spigot to boiler M12 x 1, 14 long, Ø5 hole"), ("", "Gland boss M16 x 1, 8 long"), ("", "Glass bore Ø12.2, 9 deep"),
      ("", "Plug thread M10 x 1 on the far end")],
 25: [("", "Main body Ø15, 48 long overall"), ("", "Hexagon 17 across flats, 6 long"), ("", "Threads M12 x 1 at both ends"),
      ("", "Stem thread inside M8 x 1"), ("", "Outlet boss Ø14 with M10 x 1 thread")],
 49: [("", "Pin centres 27.6 apart"), ("", "Fulcrum to handle end 272"), ("", "2 cheeks 3 thick, 18 gap"), ("", "Boss Ø16 x 15, rod Ø11"),
      ("", "Handle Ø22 to Ø24 x 101 (item 53)")],
}

def build(pdf, Sheet):
    def page(title, layout, cells):
        sh = Sheet(None, title, "see cells")
        for (x, y, w, h), fn in zip(grid(sh.ax, *layout), cells): fn(sh.ax, x, y, w, h)
        sh.save(pdf)
    T = lambda it: (lambda ax, x, y, w, h: SP.cell_turned(ax, x, y, w, h, it, *TURNED[it][:4], TURNED[it][4]))
    R = lambda it: (lambda ax, x, y, w, h: SP.cell_ring(ax, x, y, w, h, it, *RINGS[it][:4], RINGS[it][4], RINGS[it][5]))
    PI = lambda it: (lambda ax, x, y, w, h: SP.cell_pipe(ax, x, y, w, h, it, *PIPES[it][:4], PIPES[it][4:], _pipe))
    C = lambda it, name, mat, qty, conf, fn, lf=0.30: (lambda ax, x, y, w, h: SP.cell_custom(ax, x, y, w, h, it, name, mat, qty, conf, fn, KEYS.get(it, []), lf))
    page("PART DRAWINGS 1 - COPPER SHELLS", (2, 1), [C(1, "Lower shell", CU + " tube, polished + lacquer", 1, "D/E", lambda c: PP.shell_drawing(c, "lower"), 0.28),
                                                      C(85, "Upper shell", CU + " tube, polished + lacquer", 1, "D/E", lambda c: PP.shell_drawing(c, "upper"), 0.28)])
    page("PART DRAWINGS 2 - GROUP BODY (MILLENNIUM)", (1, 1), [C(35, "Group body", BR + POL, 1, "D/V/E", PP.group_body, 0.27)])
    page("PART DRAWINGS 3 - BOILER CASTINGS", (2, 2), [T(2), T(3), T(86), T(9)])
    page("PART DRAWINGS 4 - BOSS, RING NUT, ELEMENT, CAP KNOB", (2, 2), [C(69, "Boiler boss / pad", BR + ", brazed to 85", 1, "V/E", PP.pad_drawing),
                                                                        C(4, "Fixing ring nut", BR, 1, "D/V", PP.ringnut_drawing),
                                                                        C(6, "Heating element 1000 W", "AISI 316", 1, "D/V", PP.element_drawing), T(11)])
    page("PART DRAWINGS 5 - BASE, SUB-BASE, GRID, CAP SCREW", (2, 2), [C(61, "Base shell", "Brass 0.8" + POL, 1, "D/V/E", PP.base_drawing),
                                                                      C(79, "Sub-base", "ABS black", 1, "D/E", PP.subbase_drawing),
                                                                      C(62, "Drip grid", "Brass 0.8" + POL, 1, "V", PP.grid_drawing), T(12)])
    page("PART DRAWINGS 6 - SIGHT GLASS & GAUGE", (2, 2), [C(19, "Sight-glass block", BRB + POL, 2, "D/V/E", PS.sgblock_drawing), T(17),
                                                       C(71, "Pressure gauge", "Bought-in, brass case", 1, "D", PP.gauge_drawing), T(72)])
    page("PART DRAWINGS 7 - SIGHT GLASS FITTINGS", (2, 2), [T(18), T(20), T(21), T(24)])
    page("PART DRAWINGS 8 - STEAM VALVE", (2, 2), [C(25, "Steam-valve body", BRB + POL, 1, "D/V/E", PS.valvebody_drawing), T(26), T(27), T(30)])
    page("PART DRAWINGS 9 - STEAM PARTS & SAFETY VALVE", (2, 2), [T(87), T(33), T(13), T(16)])
    page("PART DRAWINGS 10 - FROTHER, TIP, PIN, GLAND", (2, 2), [T(89), T(34), T(31), T(66)])
    page("PART DRAWINGS 11 - PISTON, SLEEVE, ROD, ROLLER", (2, 2), [T(36), T(76), T(38), T(52)])
    page("PART DRAWINGS 12 - LEVER, PINS, HANDLE, ACORN", (2, 2), [C(49, "Lever fork + rod", "Brass" + POL, 1, "V/E", PS.lever_drawing), T(50), T(53), T(48)])
    page("PART DRAWINGS 13 - PORTAFILTER", (2, 2), [T(54), T(55), T(59), T(60)])
    page("PART DRAWINGS 14 - SMALL PARTS", (2, 2), [T(46), T(47), T(40), T(43) if 43 in TURNED else T(31)])
    page("PART DRAWINGS 15 - PIPES (bend tables)", (3, 1), [PI(32), PI(88), PI(45)])
    page("PART DRAWINGS 16 - PIPES (bend tables)", (2, 1), [PI(16), PI(74)])
    page("PART DRAWINGS 17 - SEALS 1", (3, 3), [R(5), R(7), R(10), R(22), R(23), R(28), R(29), R(37), R(39)])
    page("PART DRAWINGS 18 - SEALS 2", (3, 3), [R(41), R(42), R(44), R(77), R(51), R(90)])

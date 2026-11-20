# La Pavoni Professional, copper & brass (PB-16 / PRG, v3.1 2007->): reconstruction drawing set

33 A3 sheets in LaPavoni_Professional_CopperBrass_drawings.pdf (+ sheetNN.png / .svg, BOM.csv).
ALL UNITS SI: lengths in mm, pressure in kPa, torque in N·m, mass in kg, volume in L / mL, temperature in °C,
roughness in µm. Pipe threads are ISO 228 G-threads (G1/8 = Ø9.73 x 0.907, G1/4 = Ø13.16 x 1.337).

| Sheets | Content |
|---|---|
| 1-2 | Isometric assembled; exploded isometric with every part ballooned (89 item numbers) |
| 3-5 | Front/rear, left/right, top/bottom views with heights and positions from fixed datums |
| 6-9 | Boiler section, Millennium group section (stroke 29.5 mm, 45 mL), group-to-boiler joint (side bolts), wiring |
| 10-27 | Part drawings: EVERY part has its own isometric view, a simple drawing with letter tags, and a plain-language KEY DIMENSIONS table |
| 28-29 | OPTION: group pressure-gauge kit (2nd gauge, 0-16 bar, on top of the lever) - assembly section, gauge, hollow piston/rod, extension, adapter, nut, screws (items 91-98) |
| 30 | Fastener master table (29 positions, torques in N·m) |
| 31-32 | Bill of materials |
| 33 | Seal schedule, assembly sequence, checks, mass estimate |

How to read a part drawing: find the letter (A, B, C...) on the drawing, then read its line in the KEY DIMENSIONS table
("Diameter Ø43.9, 4 long (from 0 to 4)"). The only arrows drawn are the length chain and the overall length.

Basis: published specs (1.6 L boiler, 1000 W, Ø100 copper tank, Ø40 gauge, 60x50x5.5 group gasket, 44 mm piston, M5x12 element
screws, M80x1.5 boiler thread, pressurestat with G1/8 + G1/4 pipe nuts, 127 °C reset thermostat) from La Pavoni / Parts Guru /
Espresso Shop diagrams, F. Ceccarelli, L. Wright and retailers; proportions scaled from product photos (refs in C:\coffee\refs).
Tags: [D] documented, [V] scaled from photos (about ±5 mm), [E] engineering estimate. Measure [V]/[E] values before machining.

Generator: python make_drawings.py (views.py = dimensions D + model, iso.py = itemised 3D, pro_parts.py / pro_build.py /
simple_parts.py = part drawings, pro_misc.py = assemblies, joint, wiring, fasteners, BOM).

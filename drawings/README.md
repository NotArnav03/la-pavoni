# La Pavoni Europiccola v2.2 (Feb 1979): reconstruction drawing set, Rev B

Source video: https://www.youtube.com/watch?v=J31RKk_7p68 ("Not Terrible Restorations" restomod)
Reference diagrams (Parts Guru, Stefano's, Nuova Ricambi, La Pavoni, L. Wright cross-section): C:\coffee\refs\images (see SOURCES.md)

| Sheet | Content |
|---|---|
| 1 | Isometric, assembled (shaded 3D, every part) |
| 2 | Exploded isometric: every part, fastener and seal ballooned, with item legend |
| 3-5 | Orthographic views: front/rear, left/right, top/bottom, ordinate-dimensioned |
| 6 | Boiler assembly section |
| 7 | Brew group assembly section (stroke, displacement, every Z level) |
| 8 | Group-to-boiler joint: section 2:1, boss face, plan section, bolt stack |
| 9 | Base, drip grid, rubber cover, wiring |
| 10-18 | Part drawings: every diameter, step, depth, thread, groove, hole (hole tables), pipe bends (bend tables), seal sections |
| 19 | Fastener master table: 25 positions, size, standard, material, tool, torque, locking |
| 20-21 | Bill of materials (70 items) |
| 22 | Seal schedule, assembly sequence, verification list, weights |

Files: LaPavoni_Europiccola_1979_drawings.pdf (all sheets), sheetNN.png/.svg, BOM.csv.
Generator: `python make_drawings.py` (views.py = 3D model + shared dimensions `D`; iso.py = itemised model and isometrics;
partdraw.py = detail-drawing engine; parts_sheets.py = part data; joint.py = group/joint/fasteners; sections.py, view_sheets.py, bom.py).

Datums: Z0 table, X0 rear end of base, Y0 machine centre line (-Y = switch side).
Confidence tags: [D] documented by vendor/archive/parts list, [V] scaled from video, [E] engineering estimate. Measure [V]/[E] before cutting metal.

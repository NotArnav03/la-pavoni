# La Pavoni lever machines - reconstruction drawings

| Folder | Content |
|---|---|
| `drawings/` | La Pavoni Europiccola v2.2 (1979): 22-sheet A3 drawing set (PDF/PNG/SVG), BOM, generator scripts |
| `professional/` | La Pavoni Professional copper & brass v3.1: 33-sheet A3 set in SI units, every part with isometric + key table, optional group pressure-gauge kit, BOM, scripts |
| `refs/` | Reference parts diagrams and product photos collected online (see `refs/images/SOURCES.md`) |
| `scratch/` | Working files: video frame extracts, contact sheets, notes, patch scripts |
| `video/` | Subtitles + metadata of the restoration video (the .mp4 itself is not stored - see `.gitignore`) |

Rebuild a set: `cd professional && python make_drawings.py` (needs numpy, matplotlib).
Unofficial reverse-engineered reference, not a La Pavoni document. [D]/[V]/[E] tags mark documented / photo-scaled / estimated values.

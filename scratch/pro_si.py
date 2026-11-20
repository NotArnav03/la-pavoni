import os, re
os.chdir(r"C:\coffee\professional")
p = 'pro_parts.py'; s = open(p, encoding='utf-8').read()
i = s.find('# ================================================================== simplified build')
if i > 0: s = s[:i]
rep = {'"1/8 BSP-F"': '"G1/8-F (ISO 228)"', '"1/8 BSP male (bottom entry) [D]"': '"G1/8 male (ISO 228, Ø9.73) [D]"',
       '"Range 0-2.5 bar, class 2.5, glycerine-free, brass case, glass lens [D La Pavoni 453040 type]."': '"Range 0-250 kPa (dial 0-2.5 bar), class 2.5, brass case, glass lens [D, La Pavoni 453040 type]."',
       '"Poppet seat 90° at Ø4/Ø6.5. Opens ~1.5 bar,", "anti-vacuum lifts below 0 bar [D type]."': '"Poppet seat 90° at Ø4/Ø6.5. Opens ~150 kPa,", "anti-vacuum lifts below 0 kPa gauge [D type]."',
       '("1/8 BSP nut on element port [D]", "1/4 BSP nut on pressurestat [D]")': '("G1/8 nut on element port [D]", "G1/4 nut on pressurestat [D]")',
       'Copper tube Ø4 x 0.7 + 1/8 & 1/4 BSP nuts': 'Copper tube Ø4 x 0.7 + G1/8 & G1/4 nuts',
       '"pressurestat port 1/8 BSP, boss Ø14"': '"pressurestat port G1/8, boss Ø14"',
       'face Ra 1.6, flat 0.02.': 'face Ra 1.6 µm, flatness 0.02.',
       '"1000 W 230 V (R = 52.9 Ω) [D]; 110 V version 12.1 Ω.': '"1000 W at 230 V (R = 52.9 Ω) [D]; 120 V version 14.4 Ω.',
       'Spigot end face = element O-ring face."': 'Spigot end face = element O-ring face, Ra 3.2 µm."'}
for a, b in rep.items():
    if a in s: s = s.replace(a, b)
    else: print("miss", a[:60])
open(p, 'w', encoding='utf-8').write(s)
print([l for l in s.split('\n') if re.search(r'\bbar\b|BSP|\blb\b|\boz\b', l)][:10])

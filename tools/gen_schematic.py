"""Generuje schematic.svg (v3). Użycie: python3 tools/gen_schematic.py > schematic.svg

Symbole (dioda, NPN, rezystor) są zdefiniowane raz, a oba tory powstają z channel(),
więc kierunek diod jest identyczny w torze A/B i C. Po zmianie: wyrenderuj PNG i sprawdź
kierunki diod wizualnie (plan wdrożenia, Task 3 Step 7).
"""

W, H = 1400, 900
ISO_X = 1000
out = []


def add(s):
    out.append(s)


def line(x1, y1, x2, y2, w=2, extra=""):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="{w}" {extra}/>')


def poly(points, fill="#111"):
    pts = " ".join(f"{x},{y}" for x, y in points)
    add(f'<polygon points="{pts}" fill="{fill}" stroke="#111" stroke-width="1.5"/>')


def text(x, y, s, cls="lbl", anchor="middle"):
    add(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{s}</text>')


def dot(x, y):
    add(f'<circle cx="{x}" cy="{y}" r="4" fill="#111"/>')


def gnd(x, y, label="GND_mod"):
    line(x, y, x, y + 10)
    line(x - 14, y + 10, x + 14, y + 10)
    line(x - 9, y + 15, x + 9, y + 15)
    line(x - 4, y + 20, x + 4, y + 20)
    if label:
        text(x, y + 36, label, "val")


def res_h(x1, x2, y, name, value):
    """Rezystor poziomy między x1 a x2 (korpus 60 px na środku)."""
    cx = (x1 + x2) / 2
    line(x1, y, cx - 30, y)
    add(f'<rect x="{cx - 30}" y="{y - 10}" width="60" height="20" fill="white" stroke="#111" stroke-width="2"/>')
    line(cx + 30, y, x2, y)
    text(cx, y - 16, name, "lbl")
    text(cx, y + 28, value, "val")


def res_v(x, y1, y2, name, value, side="right"):
    cy = (y1 + y2) / 2
    line(x, y1, x, cy - 25)
    add(f'<rect x="{x - 10}" y="{cy - 25}" width="20" height="50" fill="white" stroke="#111" stroke-width="2"/>')
    line(x, cy + 25, x, y2)
    dx, anchor = (16, "start") if side == "right" else (-16, "end")
    text(x + dx, cy - 4, name, "lbl", anchor)
    text(x + dx, cy + 12, value, "val", anchor)


def cap_h(x1, x2, y, name, value):
    cx = (x1 + x2) / 2
    line(x1, y, cx - 6, y)
    line(cx - 6, y - 16, cx - 6, y + 16, 3)
    line(cx + 6, y - 16, cx + 6, y + 16, 3)
    line(cx + 6, y, x2, y)
    text(cx, y + 34, f"{name} {value}", "val")


def diode_up(x, y_bottom, y_top, name, value, side="left"):
    """Dioda pionowa przewodząca W GÓRĘ: anoda na dole, katoda (pasek) na górze."""
    cy = (y_bottom + y_top) / 2
    line(x, y_bottom, x, cy + 11)
    poly([(x - 11, cy + 11), (x + 11, cy + 11), (x, cy - 9)])
    line(x - 11, cy - 9, x + 11, cy - 9, 3)
    line(x, cy - 9, x, y_top)
    dx, anchor = (-16, "end") if side == "left" else (16, "start")
    text(x + dx, cy - 2, name, "lbl", anchor)
    text(x + dx, cy + 14, value, "val", anchor)


def npn(cx, cy, name, value):
    """NPN: baza z lewej (cx-22, cy), kolektor do góry (cx, cy-26), emiter w dół (cx, cy+26)."""
    add(f'<circle cx="{cx - 4}" cy="{cy}" r="24" fill="none" stroke="#111" stroke-width="1.5"/>')
    line(cx - 22, cy - 14, cx - 22, cy + 14, 3)
    line(cx - 22, cy - 6, cx, cy - 22)
    line(cx, cy - 22, cx, cy - 26)
    line(cx - 22, cy + 6, cx, cy + 22)
    line(cx, cy + 22, cx, cy + 26)
    # strzałka emitera skierowana NA ZEWNĄTRZ (od bazy)
    poly([(cx, cy + 22), (cx - 11, cy + 19), (cx - 5, cy + 12)])
    text(cx + 30, cy - 4, name, "lbl", "start")
    text(cx + 30, cy + 12, value, "val", "start")


def jack(x, y, label):
    """Gniazdo: tip wychodzi w prawo z (x+14, y), sleeve w dół do GND_mod."""
    add(f'<circle cx="{x}" cy="{y}" r="14" fill="white" stroke="#111" stroke-width="2"/>')
    dot(x, y)
    text(x, y - 22, label, "lbl")
    line(x, y + 14, x, y + 34)
    gnd(x, y + 34)


def switch_spst(x1, x2, y, name, note):
    cx = (x1 + x2) / 2
    line(x1, y, cx - 20, y)
    add(f'<circle cx="{cx - 20}" cy="{y}" r="4" fill="white" stroke="#111" stroke-width="2"/>')
    add(f'<circle cx="{cx + 20}" cy="{y}" r="4" fill="white" stroke="#111" stroke-width="2"/>')
    line(cx - 17, y - 2, cx + 18, y - 16)
    line(cx + 24, y, x2, y)
    text(cx, y - 24, name, "lbl")
    text(cx, y + 18, note, "val")


def optocoupler(y_top, name):
    """PC817 przecinany linią izolacji. Zwraca współrzędne pinów."""
    x0, x1 = 880, 1120
    p1 = (x0, y_top + 30)
    p2 = (x0, y_top + 90)
    p4 = (x1, y_top + 30)
    p3 = (x1, y_top + 90)
    add(f'<rect x="{x0}" y="{y_top}" width="{x1 - x0}" height="120" rx="8" fill="#eef4fb" stroke="#111" stroke-width="2"/>')
    text(x0, y_top - 10, f"{name} PC817", "head", "start")
    # LED: anoda (pin 1) u góry, katoda (pin 2) u dołu — trójkąt w DÓŁ
    lx = 935
    line(p1[0], p1[1], lx, p1[1])
    line(lx, p1[1], lx, y_top + 50)
    poly([(lx - 11, y_top + 50), (lx + 11, y_top + 50), (lx, y_top + 70)])
    line(lx - 11, y_top + 70, lx + 11, y_top + 70, 3)
    line(lx, y_top + 70, lx, p2[1])
    line(lx, p2[1], p2[0], p2[1])
    # strzałki światła
    for dy in (52, 64):
        line(955, y_top + dy, 985, y_top + dy, 1.5)
        poly([(985, y_top + dy), (977, y_top + dy - 4), (977, y_top + dy + 4)])
    # fototranzystor
    bx = 1045
    line(bx, y_top + 40, bx, y_top + 80, 3)
    line(bx, y_top + 50, 1080, y_top + 30)
    line(1080, y_top + 30, p4[0], p4[1])
    line(bx, y_top + 70, 1080, y_top + 90)
    line(1080, y_top + 90, p3[0], p3[1])
    poly([(1080, y_top + 90), (1069, y_top + 88), (1074, y_top + 80)])
    for (px, py), lbl, anchor, dx in ((p1, "1+", "end", -6), (p2, "2−", "end", -6), (p4, "4 C", "start", 6), (p3, "3 E", "start", 6)):
        text(px + dx, py - 6, lbl, "pin", anchor)
    return p1, p2, p4, p3


def channel(y0, name_suffix, labels, with_select):
    """Jeden tor. y0 = linia R2 (górna). Zwraca (pin4, pin3)."""
    C, R_LED, R_BASE, R_SH, R_PD, D_LED, D_CL, Q, OC = labels
    bus_x = 320
    y_led = y0
    y_ctl = y0 + 170
    # magistrala wejścia in_*
    line(bus_x, y_led, bus_x, y_ctl + 90)
    in_y = y0 + 95
    dot(bus_x, in_y)
    text(bus_x - 8, in_y - 8, f"in_{name_suffix}", "val", "end")
    # tor LED
    res_h(bus_x, 560, y_led, R_LED, "470Ω 0,6 W")
    led_plus_x = 840
    line(560, y_led, 880, y_led)
    dot(led_plus_x, y_led)
    text(led_plus_x - 6, y_led - 10, "LED+", "val", "end")
    p1, p2, p4, p3 = optocoupler(y_led - 30, OC)
    # D antyparalel: anoda na LED− (dół), katoda (pasek) na LED+ (góra)
    diode_up(led_plus_x, p2[1], y_led, D_LED, "1N4148", "left")
    line(led_plus_x, p2[1], p2[0], p2[1])
    dot(led_plus_x, p2[1])
    text(led_plus_x + 6, p2[1] + 16, "LED−", "val", "start")
    # tranzystor: kolektor do LED−
    q_cy = y_ctl
    npn(led_plus_x, q_cy, Q, "BC547B")
    line(led_plus_x, p2[1], led_plus_x, q_cy - 26)
    line(led_plus_x, q_cy + 26, led_plus_x, q_cy + 50)
    gnd(led_plus_x, q_cy + 50, "")
    # sterowanie bazą
    node_h_x = 520
    cap_h(bus_x, node_h_x, y_ctl, C, "0.22µF")
    dot(bus_x, y_ctl)
    dot(node_h_x, y_ctl)
    text(node_h_x + 6, y_ctl - 8, "node_h", "val", "start")
    base_x = 760
    res_h(node_h_x, base_x, y_ctl, R_BASE, "47kΩ")
    line(base_x, y_ctl, led_plus_x - 22, y_ctl)
    dot(base_x, y_ctl)
    diode_up(base_x, y_ctl + 90, y_ctl, D_CL, "1N4148", "left")
    gnd(base_x, y_ctl + 90, "")
    res_v(node_h_x, y_ctl, y_ctl + 90, R_SH, "100kΩ", "right")
    gnd(node_h_x, y_ctl + 90, "")
    # pull-down R7/R8 na dole magistrali
    line(bus_x, y_ctl, bus_x, y_ctl + 20)
    res_v(bus_x, y_ctl + 20, y_ctl + 90, R_PD, "47kΩ", "right")
    gnd(bus_x, y_ctl + 90, "")
    if with_select:
        # GATE/TRIG równolegle do C1: in_AB (bus) ↔ node_h
        y_sw = y_ctl - 60
        dot(bus_x, y_sw)
        switch_spst(bus_x, node_h_x, y_sw, "SW_HP — GATE/TRIG", "ON = GATE (zwarty), OFF = TRIG")
        line(node_h_x, y_sw, node_h_x, y_ctl)
    return in_y, p4, p3


add('<?xml version="1.0" encoding="UTF-8"?>')
add(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Arial, sans-serif" font-size="13">')
add("""  <style>
    .lbl  { font-size: 13px; fill: #111; }
    .val  { font-size: 11px; fill: #444; }
    .pin  { font-size: 12px; fill: #111; font-weight: bold; }
    .head { font-size: 15px; font-weight: bold; fill: #111; }
    .note { font-size: 12px; fill: #333; font-style: italic; }
    .iso  { font-size: 12px; fill: #c00; font-weight: bold; }
    .sect { font-size: 13px; fill: #666; font-weight: bold; }
    line  { stroke-linecap: round; stroke-linejoin: round; }
  </style>""")
add(f'<rect width="{W}" height="{H}" fill="white"/>')
add(f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="none" stroke="#bbb" stroke-width="1"/>')
text(W / 2, 36, "CV Tap Tempo Mod v3 — schemat ideowy (jeden pedał)", "head")

# linia izolacji
add(f'<line x1="{ISO_X}" y1="56" x2="{ISO_X}" y2="800" stroke="#c00" stroke-width="1.5" stroke-dasharray="8,5"/>')
text(ISO_X - 10, 70, "GND_mod (modular)", "iso", "end")
text(ISO_X + 10, 70, "GND_ped (pedał)", "iso", "start")

# tor A/B
text(30, 92, "Tor A/B (SELECT + GATE/TRIG)", "sect", "start")
in_ab_y, p4a, p3a = channel(130, "AB", ("C1", "R2", "R5", "R1", "R7", "D1", "D3", "Q1", "OC1"), True)
# jacki A, B i SELECT
jack(60, 130, "CV A")
jack(60, 330, "CV B")
sel_a = (200, 130)
sel_b = (200, 330)
sel_c = (260, in_ab_y)
line(74, 130, sel_a[0] - 4, 130)
line(74, 330, sel_b[0] - 4, 330)
for (x, y) in (sel_a, sel_b, sel_c):
    add(f'<circle cx="{x}" cy="{y}" r="4" fill="white" stroke="#111" stroke-width="2"/>')
line(sel_c[0] - 3, sel_c[1] - 3, sel_a[0] + 3, sel_a[1] + 3)
add(f'<line x1="{sel_c[0] - 3}" y1="{sel_c[1] + 3}" x2="{sel_b[0] + 3}" y2="{sel_b[1] - 3}" stroke="#111" stroke-width="2" stroke-dasharray="5,4"/>')
line(sel_c[0] + 4, sel_c[1], 320, in_ab_y)
text(215, in_ab_y - 16, "SELECT", "lbl", "end")
text(215, in_ab_y + 2, "A / OFF / B", "val", "end")

# tor C
text(30, 452, "Tor C (zawsze TRIG)", "sect", "start")
in_c_y, p4c, p3c = channel(500, "C", ("C2", "R4", "R6", "R3", "R8", "D2", "D4", "Q2", "OC2"), False)
jack(60, in_c_y, "CV C")
line(74, in_c_y, 320, in_c_y)

# strona pedału
tap_x, gnd_x = 1240, 1170
line(p4a[0], p4a[1], tap_x, p4a[1])
# pin 4 OC2 przecina szynę GND_ped bez połączenia — mostek (łuk)
line(p4c[0], p4c[1], gnd_x - 9, p4c[1])
add(f'<path d="M {gnd_x - 9} {p4c[1]} A 9 9 0 0 1 {gnd_x + 9} {p4c[1]}" fill="none" stroke="#111" stroke-width="2"/>')
line(gnd_x + 9, p4c[1], tap_x, p4c[1])
line(tap_x, p4a[1], tap_x, 740)
dot(tap_x, p4c[1])
line(p3a[0], p3a[1], gnd_x, p3a[1])
line(p3c[0], p3c[1], gnd_x, p3c[1])
line(gnd_x, p3a[1], gnd_x, 740)
dot(gnd_x, p3c[1])
text(tap_x + 8, p4a[1] - 8, "tap_pin", "lbl", "start")
text(tap_x + 8, p4a[1] + 8, "→ PCB pedału (~3.3V)", "val", "start")
text(gnd_x + 8, p3a[1] + 18, "GND_ped", "lbl", "start")
# REC
y_rec = 740
dot(tap_x, y_rec)
dot(gnd_x, y_rec)
add(f'<circle cx="{gnd_x + 22}" cy="{y_rec + 30}" r="4" fill="white" stroke="#111" stroke-width="2"/>')
add(f'<circle cx="{tap_x - 22}" cy="{y_rec + 30}" r="4" fill="white" stroke="#111" stroke-width="2"/>')
line(gnd_x, y_rec, gnd_x, y_rec + 30)
line(gnd_x, y_rec + 30, gnd_x + 18, y_rec + 30)
line(tap_x, y_rec, tap_x, y_rec + 30)
line(tap_x, y_rec + 30, tap_x - 18, y_rec + 30)
line(gnd_x + 25, y_rec + 28, tap_x - 25, y_rec + 14)
text((gnd_x + tap_x) / 2, y_rec + 52, "REC (ON/OFF)", "lbl")

# notatki
notes = [
    "D1/D2: antyparalel do LED — katoda (pasek) → pin 1 PC817, anoda → pin 2",
    "D3/D4: klamp bazy — anoda → GND_mod, katoda (pasek) → baza Q",
    "R7/R8: pull-down wejścia (in → GND_mod) — kolejne gate'y działają też przy źródle, które nie ściąga do 0V",
    "TRIG: impuls 15–133 ms · GATE: tap tak długi jak gate · odporne na ±12V (20 Vpp i 24 Vpp)",
    "Przecięcie z łukiem = brak połączenia. Kropka = połączenie. Wartości i połączenia: spec.md (v3)",
]
for i, n in enumerate(notes):
    text(30, 822 + i * 15, n, "note", "start")
add("</svg>")
print("\n".join(out))

"""Liczy impulsy, w których prąd LED przekracza próg (domyślnie 1 mA), z pliku wrdata ngspice.

Użycie: analyze.py plik [próg_w_amperach]
"""
import sys

THRESHOLD_A = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-3
rows = [line.split() for line in open(sys.argv[1]) if line.strip()]
t = [float(r[0]) for r in rows]
i = [float(r[1]) for r in rows]
pulses, on, start = [], False, 0.0
for k in range(len(t)):
    if not on and i[k] > THRESHOLD_A:
        on, start = True, t[k]
    elif on and i[k] <= THRESHOLD_A:
        on = False
        pulses.append(t[k] - start)
if on:
    pulses.append(t[-1] - start)
widths = [p * 1e3 for p in pulses]
summary = f"impulsów: {len(widths):2d}"
if widths:
    summary += f"  szer. min {min(widths):6.1f} ms  max {max(widths):6.1f} ms"
print(summary)

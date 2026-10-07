#!/bin/sh
# Odtwarza wszystkie liczby z sekcji "Dlaczego v3" w spec.md.
# Wymaga: ngspice (brew install ngspice), python3.
set -e
export LC_ALL=C
cd "$(dirname "$0")"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

meas() { ngspice -b "$1" 2>&1 | awk '/^(ipk|t_dn|vneg)/{printf "%s=%s  ", $1, $3} END{print ""}'; }

echo "== v2: filtr 0.1u/10k obciążony LED (t_dn - 1ms = czas impulsu >1mA)"
for V in 5 10; do for RS in 1m 1k; do
  sed -e "s/^.param .*/.param VCV=$V RSRC=$RS/" v2_hp.cir > "$TMP/v2.cir"
  printf "CV=%-2sV Rs=%-3s: " "$V" "$RS"; meas "$TMP/v2.cir"
done; done

echo "== v2: dioda w kierunku z schematic.svg (prąd LED)"
ngspice -b v2_diode_svg.cir 2>&1 | grep 'i(vlsense)'

v3() { # $1 CBV, $2 VCV, $3 RSRC, $4 R2V, $5 źródło, $6 tstop, $7 opis
  sed -e "s|^.param .*|.param VCV=$2 RSRC=$3 R2V=$4 CBV=$1|" \
      -e "s|^\* __SOURCE__.*|VIN in 0 $5|" \
      -e "s|^\* __ANALYSIS__.*|.tran 20u $6\n.control\nrun\nwrdata $TMP/out.txt i(VLsense)\nmeas tran ipk MAX i(VLsense)\n.endc|" \
      v3_gate.cir > "$TMP/v3.cir"
  printf "%-36s" "$7"
  ngspice -b "$TMP/v3.cir" > "$TMP/log.txt" 2>&1
  printf "%s  " "$(awk '/^ipk/{printf "I_LED pk %.1f mA", $3*1e3}' "$TMP/log.txt")"
  python3 analyze.py "$TMP/out.txt"
}

echo "== v3: przypadki brzegowe (Cb=0.22u, R2=470, wyjście modułu 1k)"
for V in 5 10; do
  echo "-- CV=${V}V"
  v3 0.22u $V 1k 470 "PULSE(0 {VCV} 1m 1u 1u 1m 500m)"   2   "trigger 1ms co 500ms"
  v3 0.22u $V 1k 470 "PULSE(0 {VCV} 1m 1u 1u 10m 500m)"  2   "trigger 10ms co 500ms"
  v3 0.22u $V 1k 470 "PULSE(0 {VCV} 1m 1u 1u 250m 500m)" 2   "gate 50% @120BPM"
  v3 0.22u $V 1k 470 "PULSE(0 {VCV} 1m 1u 1u 180m 200m)" 2   "gate 90% @300BPM"
  v3 0.22u $V 1k 470 "PWL(0 0 1m 0 1.001m {VCV} 3.001 {VCV} 3.002 0 3.5 0)" 3.5 "długi gate 3s"
  # Tryb GATE: SW_HP zwiera Cb - modelowane jako Cb=1F (zwarcie w skali sekund)
  v3 1 $V 1k 470 "PWL(0 0 1m 0 1.001m {VCV} 3.001 {VCV} 3.002 0 3.5 0)" 3.5 "GATE: długi gate 3s"
done

echo "== v3: długi gate (1s), wpływ amplitudy, Rs i R2"
for R2 in 470 330 220; do for V in 5 10 12; do for RS in 1m 1k; do
  v3 0.22u $V $RS $R2 "PWL(0 0 1m 0 1.001m {VCV} 1.001 {VCV} 1.002 0 1.1 0)" 1.1 "R2=$R2 CV=${V}V Rs=$RS"
done; done; done

echo "== v3: ujemne CV (np. bipolarne LFO), źródło 0Ω, Cb=0.22u"
for V in -5 -10 -12; do
  sed -e "s|^.param .*|.param VCV=$V RSRC=1m R2V=470 CBV=0.22u|" \
      -e "s|^\* __SOURCE__.*|VIN in 0 PWL(0 0 1m 0 1.001m {VCV} 1 {VCV})|" \
      -e "s|^\* __ANALYSIS__.*|.tran 20u 1\n.control\nrun\nlet vled = v(l) - v(s)\nmeas tran vbe_min MIN v(b) from=0 to=1\nmeas tran vled_min MIN vled from=0 to=1\nmeas tran imod MAX i(VIN) from=0.5 to=1\n.endc|" \
      v3_gate.cir > "$TMP/neg.cir"
  printf "CV=%-4s: " "$V"
  ngspice -b "$TMP/neg.cir" 2>&1 | awk '/^(vbe_min|vled_min|imod)/{printf "%s=%s  ", $1, $3} END{print ""}'
done

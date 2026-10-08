#!/bin/sh
# Odtwarza liczby z sekcji "Parametry" i "Dlaczego v3" w spec.md.
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

echo "== v3: rozrzut - hFE BC547 (110-800; grupa B = 200-450), próg tapu, tolerancja C ±10%, długi gate 1s"
echo "   (min: 5V, Rs=0, C-10%; max: 12V, Rs=1k, C+10%)"
for CNOM in 0.22 0.33 0.47; do
  CMIN=$(python3 -c "print(f'{$CNOM*0.9:.4f}u')"); CMAX=$(python3 -c "print(f'{$CNOM*1.1:.4f}u')")
  for BF in 110 200 450 800; do
    sed -e "s/BF=400/BF=$BF/" models.inc > "$TMP/models.inc"
    for THR in 1e-3 1e-4; do
      for CASE in "min 5 1m $CMIN" "max 12 1k $CMAX"; do
        set -- $CASE
        sed -e "s|^.include .*|.include $TMP/models.inc|" \
            -e "s|^.param .*|.param VCV=$2 RSRC=$3 R2V=470 CBV=$4|" \
            -e "s|^\* __SOURCE__.*|VIN in 0 PWL(0 0 1m 0 1.001m {VCV} 1.001 {VCV} 1.002 0 1.1 0)|" \
            -e "s|^\* __ANALYSIS__.*|.tran 20u 1.1\n.control\nrun\nwrdata $TMP/sw.txt i(VLsense)\n.endc|" \
            v3_gate.cir > "$TMP/sw.cir"
        ngspice -b "$TMP/sw.cir" > /dev/null 2>&1
        printf "Cb=%-4su hFE=%-3s próg=%-4s %-3s: " "$CNOM" "$BF" "$THR" "$1"
        python3 analyze.py "$TMP/sw.txt" "$THR"
      done
    done
  done
done

echo "== v3: sygnały bipolarne 20 Vpp (±10V) i 24 Vpp (±12V), źródło 0Ω (najgorszy przypadek)"
echo "   P_R2 = moc na R2 470Ω (średnia / szczyt), Vbe_min, V_LED_min (napięcie wsteczne LED), I_LED_max"
for MODE in TRIG GATE; do
  if [ "$MODE" = TRIG ]; then CB=0.22u; else CB=1; fi
  for SRC in "SIN(0 10 1)|3|LFO sinus ±10V 1Hz" \
             "SIN(0 10 1k)|50m|sinus ±10V 1kHz" \
             "PULSE(-10 10 0 1u 1u 0.5m 1m)|50m|prostokąt ±10V 1kHz" \
             "PULSE(-12 12 0 1u 1u 250m 500m)|3|prostokąt ±12V 2Hz" \
             "PWL(0 0 1m 0 1.001m 12 3 12)|3|DC +12V (stały gate)"; do
    S=${SRC%%|*}; REST=${SRC#*|}; TSTOP=${REST%%|*}; NAME=${REST#*|}
    sed -e "s|^.param .*|.param VCV=0 RSRC=1m R2V=470 CBV=$CB|" \
        -e "s|^\* __SOURCE__.*|VIN in 0 $S|" \
        -e "s|^\* __ANALYSIS__.*|.tran 20u $TSTOP\n.control\nrun\nlet pr2 = (v(a)-v(l))^2/470\nlet vled = v(l) - v(s)\nmeas tran pavg AVG pr2\nmeas tran ppk MAX pr2\nmeas tran vbe_min MIN v(b)\nmeas tran vled_min MIN vled\nmeas tran iled MAX i(VLsense)\n.endc|" \
        v3_gate.cir > "$TMP/bip.cir"
    printf "%-5s %-24s: " "$MODE" "$NAME"
    ngspice -b "$TMP/bip.cir" 2>&1 | awk '/^pavg/{a=$3}/^ppk/{p=$3}/^vbe_min/{b=$3}/^vled_min/{l=$3}/^iled/{i=$3} END{printf "P_R2 %5.0f / %5.0f mW  Vbe_min %6.2f V  V_LED_min %6.2f V  I_LED_max %5.1f mA\n", a*1e3, p*1e3, b, l, i*1e3}'
  done
done

echo "== v3: test ręczny - 3 dotknięcia 5V przez 1k (1 s dotyk, 1 s przerwy, wejście pływa po puszczeniu)"
echo "   (bez_R7: pierwszy impuls skrócony, bo punkt pracy DC wstępnie ładuje C1 - nie wpływa na wniosek)"
for RIN in bez_R7 R7_47k; do
  sed -e "s|^.param .*|.param VCV=5 RSRC=1k R2V=470 CBV=0.22u|" \
      -e "s|^RS in a {RSRC}|SW1 in in2 ctl 0 SWM\nVCTL ctl 0 PWL(0 0 0.5 0 0.501 1 1.5 1 1.501 0 2.5 0 2.501 1 3.5 1 3.501 0 4.5 0 4.501 1 5.5 1 5.501 0 6 0)\n.model SWM SW(VT=0.5 RON=1 ROFF=1e12)\nRS in2 a {RSRC}|" \
      -e "s|^\* __SOURCE__.*|VIN in 0 5|" \
      -e "s|^\* __ANALYSIS__.*|.tran 50u 6\n.control\nrun\nwrdata $TMP/touch.txt i(VLsense)\n.endc|" \
      v3_gate.cir > "$TMP/touch.cir"
  [ "$RIN" = bez_R7 ] && sed -i.bak '/^R7 a 0 47k/d' "$TMP/touch.cir"
  ngspice -b "$TMP/touch.cir" > /dev/null 2>&1
  printf "%-8s: " "$RIN"; python3 analyze.py "$TMP/touch.txt"
done

echo "== v3: wyjście modułu przez diodę (źródło tylko podaje prąd, nie ściąga do 0V), Rs=1k"
for V in 5 10; do for G in "250m 500m|120BPM 50%" "180m 200m|300BPM 90%"; do
  W=${G%%|*}; NAME=${G#*|}
  sed -e "s|^.param .*|.param VCV=$V RSRC=1k R2V=470 CBV=0.22u|" \
      -e "s|^RS in a {RSRC}|DSRC in in2 D1N4148\nRS in2 a {RSRC}|" \
      -e "s|^\* __SOURCE__.*|VIN in 0 PULSE(0 {VCV} 1m 1u 1u $W)|" \
      -e "s|^\* __ANALYSIS__.*|.tran 20u 2\n.control\nrun\nwrdata $TMP/dio.txt i(VLsense)\n.endc|" \
      v3_gate.cir > "$TMP/dio.cir"
  ngspice -b "$TMP/dio.cir" > /dev/null 2>&1
  printf "CV=%-2sV %-12s: " "$V" "$NAME"; python3 analyze.py "$TMP/dio.txt"
done; done

echo "== v3: prostokąt bipolarny (skok z -V na +V), Rs=1k, najgorszy rozrzut (hFE 800, C+10%, próg 0.1mA i 1mA)"
sed -e "s/BF=400/BF=800/" models.inc > "$TMP/models800.inc"
for V in 10 12; do for THR in 1e-3 1e-4; do
  sed -e "s|^.include .*|.include $TMP/models800.inc|" \
      -e "s|^.param .*|.param VCV=$V RSRC=1k R2V=470 CBV=0.242u|" \
      -e "s|^\* __SOURCE__.*|VIN in 0 PULSE({-VCV} {VCV} 0 1u 1u 1 2)|" \
      -e "s|^\* __ANALYSIS__.*|.tran 20u 4\n.control\nrun\nwrdata $TMP/bsq.txt i(VLsense)\n.endc|" \
      v3_gate.cir > "$TMP/bsq.cir"
  ngspice -b "$TMP/bsq.cir" > /dev/null 2>&1
  printf "±%-2sV 0.25Hz próg=%-4s: " "$V" "$THR"; python3 analyze.py "$TMP/bsq.txt" "$THR"
done; done

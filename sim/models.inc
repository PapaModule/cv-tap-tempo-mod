* Modele do symulacji CV tap tempo mod (ngspice)
* Ograniczenia: DLED to model behawioralny dopasowany do Vf ~1.2V @ 10mA
* (typowa wartość z datasheetu PC817), nie model producenta. Fototranzystor
* PC817 nie jest modelowany - przyjmujemy, że I_LED > 1 mA = tap aktywny.
.model DLED D(IS=1e-18 N=1.9 RS=2 BV=6 IBV=10u)
.model D1N4148 D(IS=2.52n RS=0.568 N=1.752 CJO=4p BV=100 IBV=100u TT=20n)
.model BC547 NPN(IS=1.8e-14 BF=400 VAF=80 IKF=0.1 RB=10 RC=1 CJE=11p CJC=5p TF=0.5n)

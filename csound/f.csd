<CsoundSynthesizer>
<CsOptions>
; Select audio/midi flags here according to platform
-odac      ;;;realtime audio out
;-iadc    ;;;uncomment -iadc if realtime audio input is needed too
; For Non-realtime ouput leave only the line below:
; -o foscil.wav -W ;;; for file output any platform
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs  = 1

instr 1

kcps = 440
kcar = 1
kmod = p4
kndx line 0, p3, 20	;intensivy sidebands
ifn = p5

asig foscil .5, kcps, kcar, kmod, kndx, ifn
     outs asig, asig

endin
</CsInstruments>
<CsScore>
; sine
f1 0 16384 10 1
f2 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111   ; Sawtooth
f3 0 16384 10 1 0   0.3 0    0.2 0     0.14 0     .111   ; Square
f4 0 16384 10 1 1   1   1    0.7 0.5   0.3  0.1          ; Pulse

; i id st dt m
;


;id  st dt m 
i 1  0  3  0.05 1
i 1  1  2  0.01 1
i 1  3  8  0.02 3
i 1  4  7  0.04 3




;i 1 0  9 .01	;vibrato
;i 1 10 .  1
;i 1 20 . 1.414	;gong-ish
;i 1 30 5 2.05	;with "beat"
e
</CsScore>
</CsoundSynthesizer>

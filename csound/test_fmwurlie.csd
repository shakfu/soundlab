<CsoundSynthesizer>
<CsOptions>
; Select audio/midi flags here according to platform
-odac     ;;;realtime audio out
;-iadc    ;;;uncomment -iadc if realtime audio input is needed too
; For Non-realtime ouput leave only the line below:
; -o fmwurlie.wav -W ;;; for file output any platform
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32  
nchnls = 2
0dbfs  = 1

instr 1

kfreq = 440
kc1 = p4
kc2 = 1
kvdepth = 0.05
kvrate = 6
ifn1 = 1
ifn2 = 1
ifn3 = 1
ifn4 = 2
ivfn = 1

asig fmwurlie .5, kfreq, kc1, kc2, kvdepth, kvrate, ifn1, ifn2, ifn3, ifn4, ivfn
     outs asig, asig

endin
</CsInstruments>
<CsScore>
; sine wave
f 1 0 32768 10 1
; audio file
f 2 0 256 1 "fwavblnk.aiff" 0 0 0

i 1 0 3 6
i 1 + 3 30
i 1 + 2 60
e
</CsScore>
</CsoundSynthesizer>
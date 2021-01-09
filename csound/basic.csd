<CsoundSynthesizer>

<CsOptions>
-odac -d
</CsOptions>

<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1


instr 1
iFreq = p4
iAmp = p5
iAtt = 0.1
iDec = 0.4
iSus = 0.6
iRel = 0.7
iCutoff = 5000
iRes = .4
kEnv madsr iAtt, iDec, iSus, iRel 
aVco vco2 iAmp, iFreq
aLp moogladder aVco, iCutoff*kEnv, iRes
out aLp*kEnv
endin

</CsInstruments>
<CsScore>
i1 0 1 100 1
i1 1 1 200 .2
i1 2 1 300 .7
</CsScore>
</CsoundSynthesizer>


<CsoundSynthesizer>
<CsOptions>
-odac -d
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1


</CsInstruments>
<CsScore>

</CsScore>
</CsoundSynthesizer>


<CsoundSynthesizer>
<CsOptions>
; Select audio/midi flags here according to platform ; Audio out Audio in No messages
-odac -d ;
;;RT audio I/O
; For Non-realtime ouput leave only the line below: ; -o bbcutm.wav -W ;;; for file output any platform 
</CsOptions>
<CsInstruments>
          ; Initialize the global variables.
sr = 44100 
kr = 4410 
ksmps = 10 
nchnls = 1
          ; Instrument #1 - Play an audio file normally.
instr 1
	asource soundin "beats.wav" out asource
endin
          ; Instrument #2 - Cut-up an audio file.
instr 2
asource soundin "beats.wav"
ibps = 4 
isubdiv = 8 
ibarlength = 4 
iphrasebars = 1 
inumrepeats = 2

a1 bbcutm asource, ibps, isubdiv, ibarlength, iphrasebars, inumrepeats
out a1
endin
</CsInstruments>
<CsScore>
; Play Instrument #1 for two seconds.
i 1 0 2
; Play Instrument #2 for two seconds. 
i 2 3 2

e
<bsbPanel>
 <label>Widgets</label>
 <objectName/>
 <x>100</x>
 <y>100</y>
 <width>320</width>
 <height>240</height>
 <visible>true</visible>
 <uuid/>
 <bgcolor mode="nobackground">
  <r>255</r>
  <g>255</g>
  <b>255</b>
 </bgcolor>
</bsbPanel>
<bsbPresets>
</bsbPresets>

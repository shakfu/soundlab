/* Getting started.. 1.1 Hello World

The 'Basics Chapter' of the Tutorials, will explain the root functionality of CsoundQt.
You will find the descriptions as comments directly in the code. 

This first example is focused on the different comment-types and shows a simple program, which outputs a "Hello World - 440Hz beep" to the computer's audio output and the "Hello World" string to the console.

To start it, press the RUN Button in the CsoundQt-toolbar, or choose "Control->Run Csound" from the menu. 
*/

<CsoundSynthesizer>

<CsOptions>
</CsOptions>

<CsInstruments>
ksmps=32

/*
instr starts an instrument block and refers it to a number. In this case, it is 123.
You can put comments everywhere, they will not become compiled.
'prints' will print a string to the Csound console.
the opcode 'oscils' here generates a 440 Hz sinetone signal at -12dB FS
here the signal is assigned to the computer audio output endin
*/

instr 1
	aSin oscils 0dbfs/4, 440, 0
	out aSin
endin

instr 2
	aSin oscils 0dbfs/4, 460, 0
	out aSin
endin

instr 3
	aSin oscils 0dbfs/4, 420, 0
	out aSin
endin

</CsInstruments>

; i <instr_n> <starttime_secs> <play_duration_secs>

<CsScore>
/*
i 1 1 1 					; the instrument is called by its number (123) to be played
i 2 0 1
i 3 2 1
*/
i1 0 4 100
i2 1 4 200
i3 2 4 300

e 							; e - ends the score
</CsScore>

</CsoundSynthesizer>
; written by Alex Hofmann (Nov. 2009) - Incontri HMT-Hannover 

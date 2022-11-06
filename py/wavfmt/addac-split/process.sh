sox piano.wav -b 16 out.wav channels 1 rate 22050
sox out.wav s.wav trim 0 10 : newfile : restart


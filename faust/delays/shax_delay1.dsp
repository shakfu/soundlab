import("stdfaust.lib");


time = int((hslider("time (ms)", 0, 0, 1000, 0.10): si.smoo) * ba.millisec)-1; 
fb = (hslider("feedback", 0, 0, 100, 0.1): si.smoo)/100.0;

myecho  = +~(de.delay(65536, time) * fb);

process = vgroup("stereo echo", (myecho, myecho));




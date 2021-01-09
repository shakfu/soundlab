import("stdfaust.lib");


echo  = +~(de.delay(65536, ms) * fb)
with {
    ms = int((hslider("time (ms)", 0, 0, 1000, 0.10): si.smoo) * ba.millisec)-1;
    fb = (hslider("feedback", 0, 0, 100, 0.1): si.smoo)/100.0;
};

process = vgroup("stereo echo", (echo, echo));




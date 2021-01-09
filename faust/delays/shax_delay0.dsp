import("stdfaust.lib");

myecho  = +~(de.delay(65536,
    int((hslider("millisecond", 0, 0, 1000, 0.10): si.smoo) * ba.millisec)-1) *
    ((hslider("feedback", 0, 0, 100, 0.1): si.smoo)/100.0));

process = vgroup("stereo echo", (myecho, myecho));



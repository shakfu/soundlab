import("stdfaust.lib");

/*
echo1s  = vgroup("echo  1000", +~(de.delay(65536,   int(hslider("millisecond", 0, 0,	1000, 0.10)*ba.millisec)-1) * (hslider("feedback", 0, 0,  100, 0.1)/100.0)));
echo2s  = vgroup("echo  2000", +~(de.delay(131072,  int(hslider("millisecond", 0, 0,	2000, 0.25)*ba.millisec)-1) * (hslider("feedback", 0, 0,  100, 0.1)/100.0)));
echo5s  = vgroup("echo  5000", +~(de.delay(262144,  int(hslider("millisecond", 0, 0,	5000, 0.50)*ba.millisec)-1) * (hslider("feedback", 0, 0,  100, 0.1)/100.0)));
echo10s = vgroup("echo 10000", +~(de.delay(524288,  int(hslider("millisecond", 0, 0,  10000, 1.00)*ba.millisec)-1) * (hslider("feedback", 0, 0,  100, 0.1)/100.0)));
echo21s = vgroup("echo 21000", +~(de.delay(1048576, int(hslider("millisecond", 0, 0,  21000, 1.00)*ba.millisec)-1) * (hslider("feedback", 0, 0,  100, 0.1)/100.0)));
echo43s = vgroup("echo 43000", +~(de.delay(2097152, int(hslider("millisecond", 0, 0,  43000, 1.00)*ba.millisec)-1) * (hslider("feedback", 0, 0,  100, 0.1)/100.0)));
*/


echo  = +~(de.sdelay(65536, it, ms) * fb)
with {
    it = 1024;
    ms = int((hslider("time (ms)", 0, 0, 1000, 0.10): si.smoo) * ba.millisec)-1;
    fb = (hslider("feedback", 0, 0, 100, 0.1): si.smoo)/100.0;
};

process = vgroup("stereo echo", (echo, echo));




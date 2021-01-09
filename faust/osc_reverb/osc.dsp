import("stdfaust.lib");

cutfreq = hslider("Freq", 500, 26, 10000, 0.01);
q = hslider("Res", 5, 1, 30, 0.1);
gain = hslider("Gain", 1, 0, 1, 0.01);

process = os.osc(261.63) : fi.resonlp(cutfreq, q, gain) <: dm.zita_light; 



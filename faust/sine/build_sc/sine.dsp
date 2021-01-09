import("stdfaust.lib");

// input parameters with GUI elements
freq  = hslider("frequency",100, 10, 1000, 0.001);
gain  = hslider("gain",0, 0, 1, 0.001);

// a sine oscillator with controllable freuency and amplitude:
process = os.osc(freq)*gain;


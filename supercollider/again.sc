s.meter;
s.scope;

// a function definition
f = {arg a, b=10; a+b;};
f.value(2).postln;


f = {|a=10, m=500, n=1500 | SinOsc.ar(LFNoise0.kr(a).range(m, n), mul: 0.1)}.play;
f.value(2, 5, 30);
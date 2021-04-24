SynthDef.new("ShxSinOsc", { Out.ar(0, SinOsc.ar(440, 0, 0.2)) }).add;

x = Synth.new("ShxSinOsc");
y = Synth.new("ShxSinOsc");
x.free;
y.free;

f = { "Function evaluated".postln; };
f;
f.value;

{ [SinOsc.ar(440, 0, 0.2), SinOsc.ar(442, 0, 0.2)] }.play;

f = { arg a; a.value + 3 };
f.value(10);


Platform.userExtensionDir;
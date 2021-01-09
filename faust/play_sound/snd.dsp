import("stdfaust.lib");

process = 0,_~+(1):soundfile("son[url:{'snd.wav'}]",2):!,!,_,_;


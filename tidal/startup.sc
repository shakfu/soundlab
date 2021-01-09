SuperDirt.start
MIDIClient.init;

~midiOut = MIDIOut.newByName("SHX_MIDI_OUT", "SHX_MIDI_OUT");

~dirt.soundLibrary.addMIDI(\midi, ~midiOut);
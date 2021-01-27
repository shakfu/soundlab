SuperDirt.start
MIDIClient.init
~midiOut = MIDIOut.newByName("to Hosting AU", "to Hosting AU") // substitute your own device here
~dirt.soundLibrary.addMIDI(\midi, ~midiOut)


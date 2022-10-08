#!/usr/bin/env python3
"""
# wavfmt: preparation of .wav samples for modular synthesis.

## Modules

- bastl-grandpa: mono, 22050hz, 16-bit
- qubit-wave: mono, 44100hz, 16-bit
- addac-wave: mono, 22050hz, 16-bit
- endorphin-two-of-cups
- erica-sample-drum
- squarp-rample
- makenoise-morphagene
- 2hp-play
- disting





Audio Formats
-------------

- default: mono, 44100hz, 16-bit
- bastl: mono, 22050hz, 16-bit
- qubit: mono, 44100hz, 16-bit

MIDI Formats
------------

- disting: type 0


Requirements
------------

    pip install sox


also see:

- pysox at https://github.com/rabitt/pysox
- pydub at https://github.com/jiaaro/pydub


Rationale
---------

Different modules have different configuration scripts and accept different 
types of samplea and midi files. This tool attempts to remove the hassle of
preparing samples and midi files for use.


Features
--------

1. Split and Shuffle

    - Split wav file into equal sized numbered wav chunks (files)
    - Randomly shuffle the numbers
    - Rename the files (to the new shuffled numbers)
    - Optionally:
        - remove first and last chunk

This works well with Ableton Live's follow actions.


Notes:

sox split file into 30 sec chunks:
    sox in.wav .wav trim 0 30 : newfile : restart

"""

import argparse
import copy
import glob
import itertools
import os
import pathlib
import random
import string
from pathlib import Path

import jinja2
import mido
import sox

FORMATS = ["default", "bastl", "qubit", "play", "disting"]

disting_audio_tmpl = """
disting playlist v1
-loop=1
-fadeOut=3
-fadeIn=3
-gap=3
-retriggerOnSampleChange=1
-fixedPitch=0
-ramp=0
-triggers=0
-clocks=4
-wavelength=600
-natural=0
-switch=0
-playToCompletion=0
-useStartOnSampleChange=0
-startQuantize=0
-useLoopMarkers=1
{% for sample in samples %}
{{ sample }}
{% endfor %}
"""

# The maximum number of MIDI files per playlist is 32
disting_midi_tmpl = """
disting playlist v1
-loop=1
-zeroVNote=48
-bendRange=2
-cc1offset=0
-cc1scale=5
-cc2offset=0
-cc2scale=5
-retriggerOnSampleChange=1
{% for midifile in midifiles %}
{{ midifile }}
{% endfor %}
"""



class ModFormat:
    """Prepare MIDI files for the require format of a module."""
    def __init__(self, fmt, wav_dir, mid_dir=None, root_dir='.', **config):
        self.fmt = fmt
        self.wav_dir = Path(wav_dir)
        self.mid_dir = Path(mid_dir) if mid_dir else None
        self.root_dir = Path(root_dir)

        dst_wav_dir = self.root_dir / 'samples'
        dst_mid_dir = self.root_dir / 'midifiles'

        self.wav_mgr = WavFormat(fmt, wav_dir, dst_wav_dir)
        if self.mid_dir:
            self.mid_mgr = MidiFormat(fmt, mid_dir, dst_mid_dir) if mid_dir else None

    def convert(self):
        """Conversion dispatcher."""
        self.wav_mgr.convert()
        if self.mid_dir and self.mid_mgr:
            self.mid_mgr.convert()

    @classmethod
    def cmd_line(cls):

        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--format",
            help=f"specify conversion format: {FORMATS}",
            default="default")
        parser.add_argument("-s", "--shuffle", 
            action="store_true", help="shuffle files")
        parser.add_argument("src", help="src directory")
        parser.add_argument("dst", help="dst directory")
        args = parser.parse_args()
        # hand off to app
        app = cls(args.format, args.src, args.dst, **vars(args))
        app.convert()

class MidiFormat:
    """Prepare MIDI files for the require format of a module."""
    def __init__(self, fmt, src_dir, dst_dir, **config):
        self.fmt = fmt
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.config = config

        self.midifiles = Path(src_dir)

    def convert(self):
        """Conversion dispatcher."""
        getattr(self, "convert_" + self.fmt)()

    def convert_disting(self):
        """Convert .wav samples to disting format."""

class WavFormat:
    """Prepares .wav samples to the required format of a module.
    """
    def __init__(self, fmt, src_dir, dst_dir, **config):
        self.fmt = fmt
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.config = config

        self.samples = Path(src_dir)

    def convert(self):
        """Conversion dispatcher."""
        getattr(self, "convert_" + self.fmt)()

    def convert_default(self):
        """Convert .wav samples to default format."""

        for sample in self.samples.glob("*.wav"):
            tfm = sox.Transformer()
            tfm.convert(n_channels=1, bitdepth=16)
            tfm.norm()
            src = f"{sample.parent}/{sample.name}"
            dst = f"{self.dst_dir}/{sample.name}"
            print(f"converting {src} to {dst}")
            tfm.build(src, dst)

    def convert_bastl(self):
        """Convert .wav samples to bastl grandpa format."""

        suffixes = [c for c in (string.ascii_uppercase + string.digits)]

        for sample in self.samples.glob("*.wav"):
            if not suffixes:
                return
            suffix = suffixes.pop()
            tfm = sox.Transformer()
            tfm.convert(n_channels=1, bitdepth=16, samplerate=22050)
            tfm.norm()
            src = f"{sample.parent}/{sample.name}"
            dst = f"{self.dst_dir}/P{suffix}.wav"
            print(f"converting {src} to {dst}")
            tfm.build(src, dst)

    def convert_qubit(self):
        """Convert .wav samples to qu-bit wave format.

        Has two methods of populating the samples outputs:

            1. Read from a list of .wav files in a directory
            2. Look for 4 subfolders in the directary to populate each bank (TODO)
        """

        banks = ["A", "B", "C", "D"]
        samples_per_bank = [str(i) for i in range(1, 5)]
        channels = [str(i) for i in range(1, 5)]

        names = [
            "".join(x)
            for x in list(itertools.product(banks, samples_per_bank, channels))
        ]

        if len(list(self.samples.iterdir())) == 4:
            print("MODE 2: banks discovered")
        else:
            print("MODE 1: single list")
            samples = self.samples.glob("*.wav")
            if self.config['shuffle']:
                samples = random.shuffle(list(samples))
            for sample in self.samples.glob("*.wav"):
                if not names:
                    return
                name = names.pop()
                tfm = sox.Transformer()
                tfm.convert(n_channels=1, bitdepth=16, samplerate=44100)
                tfm.norm()
                src = f"{sample.parent}/{sample.name}"
                dst = f"{self.dst_dir}/{name}.wav"
                print(f"converting {src} to {dst}")
                tfm.build(src, dst)




if __name__ == "__main__":
    ModFormat.cmd_line()

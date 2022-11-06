# wavdb - sample splitting and mgmt

This an audio utility script for splitting larges `.wav` samples into smaller files while capturing metadata to a sqlite database.

It is essentially a wrapper over the excellent `sox` tool and uses it to split `.wav` files on silence (see [ref](docs/sox-split-on-silence.md)) as well for its analytical features. 

## Usage


For a single `demo.wav` file:

```bash
$ wavdb info demo.wav
file           	text           	demo.wav
parent         	text
name           	text           	demo
suffix         	text           	.wav
encoding       	text           	Signed Integer PCM
file_size      	text           	1.32M
file_size_k    	integer        	1351
channels       	integer        	1
sample_rate    	real           	44100
bitdepth       	integer        	16
bitrate        	real           	706k
samples        	integer        	658944
duration       	real           	14.942041
mean_norm      	real           	0.031804
max_amp        	real           	0.472931
min_amp        	real           	-0.50119
mid_amp        	real           	-0.01413
mean_amp       	real           	-0.000241
rms_amp        	real           	0.057396
max_delta      	real           	0.030029
min_delta      	real           	0.0
rms_delta      	real           	0.002723
mean_delta     	real           	0.001474
freq           	integer        	332
vol_adj        	real           	1.995
dc_offset      	real           	-0.000241
crest_factor   	real           	8.73
flat_factor    	real           	4.44
scale_max      	real           	1.0
window_s       	real           	0.05
peak_level_db  	real           	-6.0
rms_level_db   	real           	-24.82
rms_peak_db    	real           	-15.69
rms_trough_db  	real           	-58.39
peak_count     	real           	3

$ wavdb split demo.wav
04:57:08 [INFO] SampleCollection: splitting files

$ ls
demo-clips/ demo.wav

$ ls demo-clips
_meta/ demo/

$ ls demo-clips/demo
demo-001.wav  demo-002.wav  demo-003.wav

$ ls demo-clips/_meta
clips.db

$ wavdb report demo-clips 'select * from clips'
# generates report.html with metadata of split clips

$ wavdb cli demo-clips
# launches litecli repl accessing _meta/clips.db
```

To split a folder of `.wav` files (assumming folder is `samples`):

```bash
$ wavdb split samples
05:08:57 [INFO] SampleCollection: splitting files
 processing: [########################################] 11/11

$ ls
samples/  samples-clips/

$ ls sample-clips
_meta/ s101/  s103/  s105/  s107/  s109/
s100/  s102/  s104/  s106/  s108/  s110/

$ ls sample-clips/s101
$ ls samples-clips/s101/
s101-001.wav  s101-007.wav  s101-013.wav  s101-019.wav  s101-025.wav
s101-002.wav  s101-008.wav  s101-014.wav  s101-020.wav  s101-026.wav
s101-003.wav  s101-009.wav  s101-015.wav  s101-021.wav  s101-027.wav
s101-004.wav  s101-010.wav  s101-016.wav  s101-022.wav
s101-005.wav  s101-011.wav  s101-017.wav  s101-023.wav
s101-006.wav  s101-012.wav  s101-018.wav  s101-024.wav

```

All clip metadata is stored int the sqlite db as in the single file case.

There are other currently undocumented features which can be accessed via the commandline interface.


## See Also

- [audiohit](https://github.com/icaroferre/AudioHit): Rust-based CLI for batch processing audio samples.




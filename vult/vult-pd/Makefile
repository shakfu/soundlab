# Needs Makefile.pdlibbuilder as helper makefile for platform-dependent build
# settings and rules.

VULTC = ../bin/vultc
RUNTIME = ../include/vult/runtime
INPUTS = $(wildcard src/*.vult)

cflags = -I$(RUNTIME) -std=c++11 -mmacosx-version-min=10.9

# library name
lib.name = vult_demo

# input source file (class name == source file basename)
class.sources = \
	cpp/ad.cpp \
	cpp/adsr.cpp \
	cpp/ahr.cpp \
	cpp/bitcrush.cpp \
	cpp/blit.cpp \
	cpp/clipper.cpp \
	cpp/fold.cpp \
	cpp/gates.cpp \
	cpp/kick.cpp \
	cpp/ladder.cpp \
	cpp/lfo.cpp \
	cpp/monocv.cpp \
	cpp/noise.cpp \
	cpp/phase.cpp \
	cpp/phd.cpp \
	cpp/polycv.cpp \
	cpp/rescomb.cpp \
	cpp/saturate.cpp \
	cpp/saturate_soft.cpp \
	cpp/saw_blit.cpp \
	cpp/saw_eptr.cpp \
	cpp/saw_ptr1.cpp \
	cpp/saw_ptr2.cpp \
	cpp/saw_r.cpp \
	cpp/sawcore.cpp \
	cpp/short_delay.cpp \
	cpp/sine.cpp \
	cpp/svf.cpp \
	cpp/swept.cpp \
	cpp/tricore.cpp \
	cpp/voice_4.cpp \
	$(empty)

# all extra files to be included in binary distribution of the library
datafiles = 

include Makefile.pdlibbuilder

reset: clean
	@rm -rf cpp

transpile:
	@mkdir -p cpp
	@for f in $(INPUTS) ; do \
		$(VULTC) -ccode -template pd "$$f" -o cpp/"`basename -s .vult $$f`" ; \
	done


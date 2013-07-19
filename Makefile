
CC       = g++
#LIBS      = -lm
CFLAGS   = -g  -O2 -Wall 
#CFLAGS   = -g  -Wall 
LDFLAGS  = -L.

PROGRAMS = mastermind-cc

default: $(PROGRAMS)

mastermind-cc: mastermind-cc.cc
	$(CC) $< $(CFLAGS) -o $@

.PHONY: clean

clean:
	rm -f  $(PROGRAMS) *.a *.o *~ tmp.csv





CPP      = g++
CC       = cc
#LIBS      = -lm
CFLAGS   = -g  -O2 -Wall 
#CFLAGS   = -g  -Wall 
LDFLAGS  = -L.

PROGRAMS = mastermind-cc match match-continuation-passing

default: $(PROGRAMS)

mastermind-cc: mastermind-cc.cc match-continuation-passing
	$(CPP) $< $(CFLAGS) -o $@

match: match.c scw-misc.h
	$(CC) $< $(CFLAGS) -o $@
match-continuation-passing: match-continuation-passing.c scw-misc.h
	$(CC) $< $(CFLAGS) -o $@

.PHONY: clean

clean:
	rm -f  $(PROGRAMS) *.a *.o *~ tmp.csv




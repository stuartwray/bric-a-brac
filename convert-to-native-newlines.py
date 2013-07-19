#!/usr/bin/python3
import sys
import tempfile
import os

def process(inf, outf):
    for line in inf:
        text = line.rstrip()
        print(text, file=outf)

if len(sys.argv) == 1:
        # just pipe stdin -> stdout
        process(sys.stdin, sys.stdout)
else:
    # take names of files from arglist
    for name in sys.argv[1:]:
        inf = open(name)
        outf = tempfile.NamedTemporaryFile(mode='w', delete=False, dir='.')
        process(inf, outf)
        inf.close()
        outf.close()
        if os.name == 'nt':
            # ugly, but can't rename over existing file in NT
            os.remove(name)
        os.rename(outf.name, name)


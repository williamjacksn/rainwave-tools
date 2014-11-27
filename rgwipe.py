#!/usr/bin/env python3

import mutagen.id3
import sys

def log(message):
    print(message)

if len(sys.argv) < 1:
    log('** please provide one or more mp3 file names')
    sys.exit()

for fn in sys.argv[1:]:
    tags = mutagen.id3.ID3(fn)
    tags.delall('TXXX:replaygain_track_peak')
    tags.delall('TXXX:replaygain_track_gain')
    tags.save(fn)

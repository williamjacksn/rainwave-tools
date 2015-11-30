#!/usr/bin/env python3

import mutagen.id3
import sys


def log(m):
    print(m)


def main():
    if len(sys.argv) < 2:
        log('** please provide one or more mp3 file names')
        sys.exit()

    for fn in sys.argv[1:]:
        tags = mutagen.id3.ID3(fn)
        tags.delall('RVA2')
        tags.delall('TXXX:MP3GAIN_MINMAX')
        tags.delall('TXXX:replaygain_album_gain')
        tags.delall('TXXX:replaygain_album_peak')
        tags.delall('TXXX:replaygain_reference_loudness')
        tags.delall('TXXX:replaygain_track_gain')
        tags.delall('TXXX:replaygain_track_peak')
        tags.save(fn)
        log('** wiped replaygain tags from {}'.format(fn))

if __name__ == '__main__':
    main()
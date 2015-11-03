#!/usr/bin/env python3

import mutagen.id3
import sys


def log(m):
    print(m)


def main():
    fn = sys.argv[1]
    url = sys.argv[2]

    tags = mutagen.id3.ID3(fn)
    log('{} : setting www to {}'.format(fn, url))
    tags.delall('WXXX')
    tags.add(mutagen.id3.WXXX(encoding=0, url=url))
    comment = 'Remix Info @ OCR'
    log('{} : setting comment to {!r}'.format(fn, comment))
    tags.delall('COMM')
    tags.add(mutagen.id3.COMM(encoding=3, text=[comment]))
    tags.save(fn)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import mutagen.id3
import sys


def log(message):
    print(message)

fn = sys.argv[1]
url = sys.argv[2]

tags = mutagen.id3.ID3(fn)
log('{} : setting www to {}'.format(fn, url))
tags.delall('WXXX')
tags.add(mutagen.id3.WXXX(encoding=0, url=url))
log('{} : setting comment to {}'.format(fn, url))
tags.delall('COMM')
tags.add(mutagen.id3.COMM(encoding=3, text=['Remix Info @ OCR']))
tags.save(fn)

#!/usr/bin/env python3

import mutagen.id3
import sys

fn = sys.argv[1]
url = sys.argv[2]

tags = mutagen.id3.ID3(fn)
tags.delall('WXXX')
tags.add(mutagen.id3.WXXX(encoding=0, url=url))
tags.delall('COMM')
tags.add(mutagen.id3.COMM(encoding=3, text=['Remix Info @ OCR']))
tags.save(fn)

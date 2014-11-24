#!/usr/bin/env python3

import mutagen.id3
import ocremix
import os
import re

def log(message):
    print(message)

cwd = os.getcwd()
log('{} : current directory'.format(cwd))

mp3s = []

for dirpath, dirnames, filenames in os.walk(cwd):
    for filename in filenames:
        if filename.endswith('.mp3'):
            mp3s.append(os.path.join(dirpath, filename))

m = '** found {} MP3'.format(len(mp3s))
if len(mp3s) != 1:
    m = '{}s'.format(m)
log(m)

for mp3 in mp3s:
    ocr_id = None
    changed = False
    tags = mutagen.id3.ID3(mp3)
    tag_www = tags.getall('WXXX')[0].url
    for match in re.findall('OCR\d{5}', tag_www):
        ocr_id = int(match[3:])
    if ocr_id is None:
        log('{} : not an OCR url'.format(mp3))
        continue
    remix = ocremix.OCReMix(ocr_id)
    try:
        remix._load_from_url()
    except:
        log('{} : could not load url {}'.format(mp3, remix.info_url))
        continue

    if remix.info_url != tag_www:
        log('{} : updating www to {}'.format(mp3, remix.info_url))
        tags.delall('WXXX')
        tags.add(mutagen.id3.WXXX(encoding=0, url=remix.info_url))
        changed = True

    tag_title = tags.getall('TIT2')[0][0]
    if remix.title != tag_title:
        log('{} : updating title to {}'.format(mp3, remix.title))
        tags.delall('TIT2')
        tags.add(mutagen.id3.TIT2(encoding=3, text=[remix.title]))
        changed = True

    if changed:
        tags.save(mp3)
    else:
        log('{} : no change'.format(mp3))

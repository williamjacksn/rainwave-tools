#!/usr/bin/env python3

import mutagen.id3
import ocremix
import os
import stat
import sys
import urllib.request

def log(message):
    print(message)

DEST_DIR = '/home/icecast/ocr-staging'
COMMENT = 'Remix Info @ OCR'
GENRE_PROMPT = 'Enter a genre > '

if len(sys.argv) > 1:
    cmd = sys.argv[1]
else:
    sys.exit('Please provide an OCR ID as the first argument.')

if cmd.isdigit():
    ocr_num = int(cmd)
else:
    sys.exit('{} is not an integer.'.format(cmd))

if ocr_num < 1 or ocr_num > 99999:
    sys.exit('{} is not between 1 and 99999'.format(ocr_num))

log('Processing OCR{:05}'.format(ocr_num))
remix = ocremix.OCReMix(ocr_num)

log('Downloading mp3 file from {}'.format(remix.mp3_url))
temp_file, _ = urllib.request.urlretrieve(remix.mp3_url)
log('Downloaded mp3 file to {}'.format(temp_file))

tags = mutagen.id3.ID3(temp_file)

log('Setting TALB (album) to {}'.format(repr(remix.album)))
tags.delall('TALB')
tags.add(mutagen.id3.TALB(encoding=3, text=[remix.album]))

log('Setting TIT2 (title) to {}'.format(repr(remix.title)))
tags.delall('TIT2')
tags.add(mutagen.id3.TIT2(encoding=3, text=[remix.title]))

log('Setting TPE1 (artist) to {}'.format(repr(remix.artist)))
tags.delall('TPE1')
tags.add(mutagen.id3.TPE1(encoding=3, text=[remix.artist]))

log('Setting WXXX (www) to {}'.format(repr(remix.info_url)))
tags.delall('WXXX')
tags.add(mutagen.id3.WXXX(encoding=0, url=remix.info_url))

log('Setting COMM (comment) to {}'.format(repr(COMMENT)))
tags.delall('COMM')
tags.add(mutagen.id3.COMM(encoding=3, text=[COMMENT]))

tags.delall('TCON')
genre = input(GENRE_PROMPT)
if genre:
    log('Setting TCON (genre) to {}'.format(repr(genre)))
    tags.add(mutagen.id3.TCON(encoding=3, text=[genre]))

log('Dropping unnecessary tags')
for tag in ['APIC', 'TCMP', 'TCOM', 'TCOP', 'TDRC', 'TENC', 'TIT1', 'TIT3',
            'TOAL', 'TOPE', 'TPE2', 'TPUB', 'TRCK', 'TSSE', 'TXXX', 'WOAR']:
    tags.delall(tag)

tags.save(temp_file)

target_file = '{}.mp3'.format(remix.safe_title)
mp3_dest = os.path.join(DEST_DIR, remix.safe_album, target_file)
log('Moving {} to {}'.format(temp_file, mp3_dest))
os.renames(temp_file, mp3_dest)

log('Changing file permissions')
os.chmod(mp3_dest, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)

log('Cleaning up temporary files')
urllib.request.urlcleanup()

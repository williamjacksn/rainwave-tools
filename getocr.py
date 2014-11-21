#!/usr/bin/env python3

import ocremix
import os
import stat
import subprocess
import sys
import urllib.request

def log(message):
    print(message)

DEST_DIR = '/home/icecast/ocr-staging'

def do_cmd(cmd):
    output = subprocess.check_output(cmd, universal_newlines=True)
    for line in output.splitlines():
        log(line)

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

do_cmd(['rwtag', 'set', 'album', remix.album, temp_file])
do_cmd(['rwtag', 'set', 'title', remix.title, temp_file])
do_cmd(['rwtag', 'set', 'artist', remix.artist, temp_file])
do_cmd(['rwtag', 'set', 'www', remix.info_url, temp_file])
do_cmd(['rwtag', 'set', 'comment', 'Remix Info @ OCR', temp_file])
do_cmd(['rwtag', 'drop', 'genre', temp_file])
do_cmd(['rwtag', 'drop', 'track', temp_file])
do_cmd(['rwtag', 'drop', 'year', temp_file])

genre = input('genre > ')
if genre:
    do_cmd(['rwtag', 'set', 'genre', genre, temp_file])

target_file = '{}.mp3'.format(remix.safe_title)
mp3_dest = os.path.join(DEST_DIR, remix.safe_album, target_file)
log('Moving {} to {}'.format(temp_file, mp3_dest))
os.renames(temp_file, mp3_dest)

log('Changing file permissions')
os.chmod(mp3_dest, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)

log('Cleaning up temporary files')
urllib.request.urlcleanup()

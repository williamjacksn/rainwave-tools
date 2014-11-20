#!/usr/bin/env python3

import lxml.html
import os
import stat
import subprocess
import sys
import urllib.request

def log(message):
    print(message)

REMIX_URL_TEMPLATE = 'http://ocremix.org/remix/OCR{:05}'
DEST_DIR = '/home/icecast/ocr-staging'

def make_safe(s):
    unsafe = '!"#%\'()*+,-./:;<=>?@[\]^_`{|}~&あまごい '
    translate_table = {ord(char): None for char in unsafe}
    special = dict(zip(map(ord, 'äÉéêíñóöÜü'), 'aEeeinooUu'))
    translate_table.update(special)
    return s.translate(translate_table)

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
ocr_url = REMIX_URL_TEMPLATE.format(ocr_num)
log('Attempting to read {}'.format(ocr_url))
try:
    ocr_data = urllib.request.urlopen(ocr_url)
except urllib.error.HTTPError as e:
    sys.exit(e)
ocr_page = ocr_data.read().decode()
ocr_tree = lxml.html.fromstring(ocr_page)

album = ocr_tree.xpath('//h1/a')[0].text
title = ocr_tree.xpath('//h1/a')[0].tail[2:-2]
art_tree = ocr_tree.xpath('//div[@id="panel-main"]/div/ul/li')[1]
artist = ', '.join([a.text for a in art_tree.xpath('a')])
mp3_url = ocr_tree.xpath('//div[@id="panel-download"]/ul/li/a/@href')[3]

log('Downloading mp3 file from {}'.format(mp3_url))
temp_file, _ = urllib.request.urlretrieve(mp3_url)
log('Downloaded mp3 file to {}'.format(temp_file))

do_cmd(['rwtag', 'set', 'album', album, temp_file])
do_cmd(['rwtag', 'set', 'title', title, temp_file])
do_cmd(['rwtag', 'set', 'artist', artist, temp_file])
do_cmd(['rwtag', 'set', 'www', ocr_url, temp_file])
do_cmd(['rwtag', 'set', 'comment', 'Remix Info @ OCR', temp_file])
do_cmd(['rwtag', 'drop', 'genre', temp_file])
do_cmd(['rwtag', 'drop', 'track', temp_file])
do_cmd(['rwtag', 'drop', 'year', temp_file])

genre = input('Genre > ')
if genre:
    do_cmd(['rwtag', 'set', 'genre', genre, temp_file])

target_file = '{}.mp3'.format(make_safe(title))
mp3_dest = os.path.join(DEST_DIR, make_safe(album), target_file)
log('Moving {} to {}'.format(temp_file, mp3_dest))
os.renames(temp_file, mp3_dest)

log('Changing file permissions')
os.chmod(mp3_dest, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)

log('Cleaning up temporary files')
urllib.request.urlcleanup()

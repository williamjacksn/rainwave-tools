#!/usr/bin/env python3

import html
import os
import subprocess
import sys
import urllib.request

def log(message):
    print(message)

REMIX_URL_TEMPLATE = 'http://ocremix.org/remix/OCR{:05}'
DEST_DIR = '/home/icecast/ocr-staging'

def make_safe(s):
    unsafe = '!"#%\'()*+,-./:;<=>?@[\]^_`{|}~ '
    translate_table = dict((ord(char), None) for char in unsafe)
    return s.translate(translate_table)

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

_, _, ocr_page = ocr_page.partition('<h1>')
_, _, ocr_page = ocr_page.partition('href')
_, _, ocr_page = ocr_page.partition('">')
album, _, ocr_page = ocr_page.partition('</a>')
album = html.unescape(album)

title, _, ocr_page = ocr_page.partition('</h1>')
_, _, title = title.partition('\'')
title, _, _ = title.rpartition('\'')

_, _, ocr_page = ocr_page.partition('ReMixer(s)</strong>: ')
dirty_artists, _, ocr_page = ocr_page.partition('</li>')
dirty_artists = dirty_artists.split(',')
clean_artists = list()
for artist in dirty_artists:
    _, _, artist = artist.partition('">')
    artist, _, _ = artist.partition('<')
    clean_artists.append(artist)
artist = ', '.join(clean_artists)

_, host, ocr_page = ocr_page.partition('http://ocrmirror.org/')
path, ext, ocr_page = ocr_page.partition('.mp3')
mp3_url = '{}{}{}'.format(host, path, ext)

log('Downloading mp3 file from {}'.format(mp3_url))
temp_file, _ = urllib.request.urlretrieve(mp3_url)
log('Downloaded mp3 file to {}'.format(temp_file))

set_album_cmd = ['rwtag', 'set', 'album', album, temp_file]
set_album = subprocess.check_output(set_album_cmd, universal_newlines=True)
for line in set_album.splitlines():
    log(line)

set_title_cmd = ['rwtag', 'set', 'title', title, temp_file]
set_title = subprocess.check_output(set_title_cmd, universal_newlines=True)
for line in set_title.splitlines():
    log(line)

set_artist_cmd = ['rwtag', 'set', 'artist', artist, temp_file]
set_artist = subprocess.check_output(set_artist_cmd, universal_newlines=True)
for line in set_artist.splitlines():
    log(line)

set_www_cmd = ['rwtag', 'set', 'www', ocr_url, temp_file]
set_www = subprocess.check_output(set_www_cmd, universal_newlines=True)
for line in set_www.splitlines():
    log(line)

set_comment_cmd = ['rwtag', 'set', 'comment', 'Remix Info @ OCR', temp_file]
set_comment = subprocess.check_output(set_comment_cmd, universal_newlines=True)
for line in set_comment.splitlines():
    log(line)

drop_genre_cmd = ['rwtag', 'drop', 'genre', temp_file]
drop_genre = subprocess.check_output(drop_genre_cmd, universal_newlines=True)
for line in drop_genre.splitlines():
    log(line)

drop_track_cmd = ['rwtag', 'drop', 'track', temp_file]
drop_track = subprocess.check_output(drop_track_cmd, universal_newlines=True)
for line in drop_track.splitlines():
    log(line)

drop_year_cmd = ['rwtag', 'drop', 'year', temp_file]
drop_year = subprocess.check_output(drop_year_cmd, universal_newlines=True)
for line in drop_year.splitlines():
    log(line)

target_file = '{}.mp3'.format(make_safe(title))
mp3_dest = os.path.join(DEST_DIR, make_safe(album), target_file)
log('Moving {} to {}'.format(temp_file, mp3_dest))
os.renames(temp_file, mp3_dest)

log('Cleaning up temporary files')
urllib.request.urlcleanup()

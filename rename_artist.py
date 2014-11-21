#!/usr/bin/env python3

import mutagen.id3
import os
import sys

def log(message):
    print(message)

if len(sys.argv) < 3:
    log('Usage: rename_artist <old_name> <new_name>')

_, old_name, new_name = sys.argv

cwd = os.getcwd()
log('{} : current directory'.format(cwd))
log('** looking to replace {} with {}'.format(repr(old_name), repr(new_name)))

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
    changed = False
    tags = mutagen.id3.ID3(mp3)
    artist_tag = tags.getall('TPE1')[0].text[0]
    artists = [a.strip() for a in artist_tag.split(',')]
    for i, artist in enumerate(artists):
        if artist == old_name:
            log('{} : found old artist {}'.format(mp3, repr(old_name)))
            artists[i] = new_name
            changed = True
    if changed:
        artist_tag = ', '.join(artists)
        tags.delall('TPE1')
        tags.add(mutagen.id3.TPE1(encoding=3, text=[artist_tag]))
        tags.save(mp3)
        log('{} : new artist tag {}'.format(mp3, repr(artist_tag)))

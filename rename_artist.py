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
log('** starting in {}'.format(cwd))
log('** looking to replace {} with {}'.format(repr(old_name), repr(new_name)))

mp3s = []

for root, folders, files in os.walk(cwd):
    for filename in files:
        if filename.endswith('.mp3'):
            mp3s.append(os.path.join(root, filename))

m = '** scanning a total of {} file'.format(len(mp3s))
if len(mp3s) != 1:
    m = '{}s'.format(m)
log(m)

mp3s.sort()
change_count = 0

for mp3 in mp3s:
    changed = False
    tags = mutagen.id3.ID3(mp3)
    artist_tag = tags.getall('TPE1')[0].text[0]
    artists = [a.strip() for a in artist_tag.split(',')]
    for i, artist in enumerate(artists):
        if artist == old_name:
            artists[i] = new_name
            changed = True
    if changed:
        change_count += 1
        artist_tag = ', '.join(artists)
        tags.delall('TPE1')
        tags.add(mutagen.id3.TPE1(encoding=3, text=[artist_tag]))
        tags.save(mp3)
        log('{} : new artist tag {}'.format(mp3, repr(artist_tag)))

m = '** updated tags in {} file'.format(change_count)
if change_count != 1:
    m = '{}s'.format(m)
log(m)

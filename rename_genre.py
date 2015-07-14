#!/usr/bin/env python3

import mutagen.id3
import os
import sys


def log(message):
    print(message)

if len(sys.argv) < 3:
    log('Usage: rename_genre <old_name> <new_name>')
    sys.exit()

_, old_name, new_name = sys.argv

cwd = os.getcwd()
log('** starting in {}'.format(cwd))
log('** looking to replace {!r} with {!r}'.format(old_name, new_name))

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
    try:
        genre_tag = tags.getall('TCON')[0].text[0]
    except IndexError:
        continue
    genres = [a.strip() for a in genre_tag.split(',')]
    for i, genre in enumerate(genres):
        if genre == old_name:
            genres[i] = new_name
            changed = True
    if changed:
        change_count += 1
        genre_tag = ', '.join(genres)
        tags.delall('TCON')
        tags.add(mutagen.id3.TCON(encoding=3, text=[genre_tag]))
        tags.save(mp3)
        log('{} : new genre tag {!r}'.format(mp3, genre_tag))

m = '** updated tags in {} file'.format(change_count)
if change_count != 1:
    m = '{}s'.format(m)
log(m)

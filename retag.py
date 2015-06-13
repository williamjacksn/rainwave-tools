#!/usr/bin/env python3

import argparse
import mutagen.id3
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('dir', nargs='?', default='.')

args = parser.parse_args()

def log(message):
    print('** {}'.format(message))

cwd = pathlib.Path(args.dir).resolve()

mp3s = []

for item in cwd.iterdir():
    if item.is_file() and item.suffix == '.mp3':
        mp3s.append(item)

mp3s.sort()

for mp3 in mp3s:
    log(mp3)
    tags = mutagen.id3.ID3(str(mp3))

    album = tags.getall('TALB')[0].text[0]
    new_album = input('album [{}] > '.format(album))
    if new_album:
        tags.delall('TALB')
        tags.add(mutagen.id3.TALB(encoding=3, text=[new_album]))
        tags.save()

    title = tags.getall('TIT2')[0].text[0]
    new_title = input('title [{}] > '.format(title))
    if new_title:
        tags.delall('TIT2')
        tags.add(mutagen.id3.TIT2(encoding=3, text=[new_title]))
        tags.save()

    artist = tags.getall('TPE1')[0].text[0]
    new_artist = input('artist [{}] > '.format(artist))
    if new_artist:
        tags.delall('TPE1')
        tags.add(mutagen.id3.TPE1(encoding=3, text=[new_artist]))
        tags.save()

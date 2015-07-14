#!/usr/bin/env python3

import argparse
import mutagen.id3
import ocremix
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--include-album', action='store_true')
parser.add_argument('dir', nargs='?', default='.')

args = parser.parse_args()


def log(message):
    print('{}'.format(message))

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
    safe_album = ocremix.OCReMix.make_safe(album)
    title = tags.getall('TIT2')[0].text[0]
    safe_title = ocremix.OCReMix.make_safe(title)
    new_name = safe_title + '.mp3'
    if args.include_album:
        new_name = safe_album + '_' + new_name
    new_file = mp3.with_name(new_name)
    log('-> {}'.format(new_file))
    mp3.rename(new_file)

#!/usr/bin/env python3

import mutagen.id3
import os

GENRE_FILE = '_genre.txt'


def log(message):
    print(message)

cwd = os.getcwd()
log('{} : current directory'.format(cwd))

for root, folders, files in os.walk(cwd):
    for filename in files:
        if filename.endswith('.mp3'):
            break
    else:
        log('{} : no mp3s'.format(root))
        continue

    this_genre_file = os.path.join(root, GENRE_FILE)
    if GENRE_FILE in files:
        with open(this_genre_file) as f:
            genre = f.readline().strip()
            log('{} : {}'.format(this_genre_file, genre))
    else:
        log('{} : not found'.format(this_genre_file))
        continue

    if genre == '':
        log('{} : empty, skipping this folder'.format(this_genre_file))
        continue

    for filename in files:
        if filename.endswith('.mp3'):
            mp3_path = os.path.join(root, filename)
            tags = mutagen.id3.ID3(mp3_path)
            for genre_tag in tags.getall('TCON'):
                for genre_text in genre_tag.text:
                    current_genre = genre_text
                break
            else:
                current_genre = ''
            if current_genre == genre:
                log('{} already has genre {}'.format(mp3_path, current_genre))
                continue
            else:
                tags.delall('TCON')
                tags.add(mutagen.id3.TCON(encoding=3, text=[genre]))
                tags.save()
                log('{} : setting genre to {}'.format(mp3_path, genre))

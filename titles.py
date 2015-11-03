#!/usr/bin/env python3

import mutagen.id3
import os
import readline


def log(m):
    print(m)


def main():
    cwd = os.getcwd()
    log('** starting in {}'.format(cwd))

    mp3s = []

    for root, folders, files in os.walk(cwd):
        for filename in files:
            if filename.endswith('.mp3'):
                mp3s.append(os.path.join(root, filename))

    mp3s.sort()
    change_count = 0

    for mp3 in mp3s:
        tags = mutagen.id3.ID3(mp3)
        title = tags.getall('TIT2')[0].text[0]
        new_title = input('{} [{}] > '.format(mp3, title))
        if new_title:
            change_count += 1
            tags.delall('TIT2')
            tags.add(mutagen.id3.TIT2(encoding=3, text=[new_title]))
            tags.save(mp3)

    m = '** updated tags in {} file'.format(change_count)
    if change_count != 1:
        m = '{}s'.format(m)
    log(m)

if __name__ == '__main__':
    main()

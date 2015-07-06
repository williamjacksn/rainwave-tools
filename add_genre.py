#!/usr/bin/env python3

import argparse
import mutagen.id3
import pathlib


def log(message):
    print(message)


def add_genre(path, genre):
    if path.is_dir():
        for child in path.iterdir():
            add_genre(child, genre)
    elif path.suffix == '.mp3':
        tags = mutagen.id3.ID3(str(path))
        genre_tag = tags.getall('TCON')[0].text[0]
        genres = set([a.strip() for a in genre_tag.split(',')])
        if genre not in genres:
            genres.add(genre)
            genre_tag = ', '.join(genres)
            tags.delall('TCON')
            tags.add(mutagen.id3.TCON(encoding=3, text=[genre_tag]))
            tags.save()
            log('{} : new genre tag {}'.format(path, repr(genre_tag)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default='.')
    parser.add_argument('genre')
    args = parser.parse_args()
    path = pathlib.Path(args.path).resolve()
    add_genre(path, args.genre.strip())

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import argparse
import mutagen.id3
import pathlib


def log(m):
    print(m)


def get_genres(file):
    rv = set()
    tags = mutagen.id3.ID3(str(file))
    for genre_tag in tags.getall('TCON'):
        for genre_text in genre_tag.text:
            rv = rv | set([a.strip() for a in genre_text.split(',')])
    return rv


def set_genres(file, genres=None):
    tags = mutagen.id3.ID3(str(file))
    tags.delall('TCON')
    if genres:
        genre_tag = ', '.join(genres)
        tags.add(mutagen.id3.TCON(encoding=3, text=[genre_tag]))
        log('{} : new genre tag {!r}'.format(file, genre_tag))
    else:
        log('{} : dropping genre tag'.format(file))
    tags.save()


def cdg_add(args):
    for f in args.files:
        p = pathlib.Path(f).resolve()
        cdgs = get_genres(p)
        if args.genre not in cdgs:
            cdgs.add(args.genre)
            set_genres(p, cdgs)


def cdg_drop(args):
    for f in args.files:
        p = pathlib.Path(f).resolve()
        cdgs = get_genres(p)
        if args.genre in cdgs:
            cdgs.discard(args.genre)
            set_genres(p, cdgs)


def cdg_list(args):
    file_list = []
    for f in args.paths:
        p = pathlib.Path(f).resolve()
        if p.is_dir():
            for item in p.iterdir():
                if item.name.endswith('.mp3'):
                    file_list.append(item)
        else:
            if p.name.endswith('.mp3'):
                file_list.append(p)
    for f in file_list:
        cdgs = get_genres(f)
        log('{} : {}'.format(f, list(cdgs)))


def cdg_rename(args):
    for f in args.files:
        p = pathlib.Path(f).resolve()
        cdgs = get_genres(p)
        if args.old_genre in cdgs:
            cdgs.discard(args.old_genre)
            cdgs.add(args.new_genre)
            set_genres(p, cdgs)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_list = subparsers.add_parser('list', aliases=['ls'])
    parser_list.add_argument('paths', nargs='*', default='.')
    parser_list.set_defaults(func=cdg_list)

    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('genre')
    parser_add.add_argument('files', nargs='+')
    parser_add.set_defaults(func=cdg_add)

    parser_drop = subparsers.add_parser('drop', aliases=['rm'])
    parser_drop.add_argument('genre')
    parser_drop.add_argument('files', nargs='+')
    parser_drop.set_defaults(func=cdg_drop)

    parser_rename = subparsers.add_parser('rename', aliases=['mv'])
    parser_rename.add_argument('old_genre')
    parser_rename.add_argument('new_genre')
    parser_rename.add_argument('files', nargs='+')
    parser_rename.set_defaults(func=cdg_rename)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

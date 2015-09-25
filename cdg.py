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


def get_mp3s(paths):
    for path in paths:
        p = pathlib.Path(path).resolve()
        if p.is_dir():
            for item in p.iterdir():
                if item.name.endswith('.mp3'):
                    yield item
        else:
            if p.name.endswith('.mp3'):
                yield p


def cdg_add(args):
    for f in get_mp3s(args.path):
        cdgs = get_genres(f)
        if args.group not in cdgs:
            cdgs.add(args.group)
            set_genres(f, cdgs)


def cdg_drop(args):
    for f in get_mp3s(args.path):
        cdgs = get_genres(f)
        if args.group in cdgs:
            cdgs.discard(args.group)
            set_genres(f, cdgs)


def cdg_list(args):
    for f in get_mp3s(args.path):
        cdgs = get_genres(f)
        log('{} : {}'.format(f, list(cdgs)))


def cdg_rename(args):
    for f in get_mp3s(args.path):
        cdgs = get_genres(f)
        if args.old_group in cdgs:
            cdgs.discard(args.old_group)
            cdgs.add(args.new_group)
            set_genres(f, cdgs)


def main():
    desc = 'Manage cooldown groups (genre tags) in mp3 files'
    ap = argparse.ArgumentParser(description=desc)
    sp = ap.add_subparsers(dest='command', title='commands')
    sp.required = True

    path_help = ('A file or directory to process. If you specify a directory, '
                 'all files in the directory will be processed. If you do not '
                 'specify this argument, it will default to the current '
                 'working directory. In any case, only files with the '
                 'extension \'.mp3\' will be processed.')

    ls_help = 'Show the current cooldown groups for one or more mp3 files'
    ps_ls = sp.add_parser('ls', aliases=['list'], help=ls_help,
                          description=ls_help)
    ps_ls.add_argument('path', nargs='*', default='.', help=path_help)
    ps_ls.set_defaults(func=cdg_list)

    add_help = 'Add a cooldown group to one or more mp3 files'
    add_group_help = 'The cooldown group to add to the specified files.'
    ps_add = sp.add_parser('add', help=add_help, description=add_help)
    ps_add.add_argument('group', help=add_group_help)
    ps_add.add_argument('path', nargs='*', default='.', help=path_help)
    ps_add.set_defaults(func=cdg_add)

    rm_help = 'Remove a cooldown group from one or more mp3 files'
    rm_group_help = 'The cooldown group to remove from the specified files.'
    ps_rm = sp.add_parser('rm', aliases=['drop', 'remove'], help=rm_help,
                          description=rm_help)
    ps_rm.add_argument('group', help=rm_group_help)
    ps_rm.add_argument('path', nargs='*', default='.', help=path_help)
    ps_rm.set_defaults(func=cdg_drop)

    mv_help = 'Rename a cooldown group in one or more mp3 files'
    mv_old_group_help = ('The current name of the cooldown group that you want '
                         'to rename.')
    mv_new_group_help = ('The new name for the cooldown group that you want to '
                         'rename.')
    ps_mv = sp.add_parser('mv', aliases=['rename', 'replace'], help=mv_help,
                          description=mv_help)
    ps_mv.add_argument('old_group', help=mv_old_group_help)
    ps_mv.add_argument('new_group', help=mv_new_group_help)
    ps_mv.add_argument('path', nargs='*', default='.', help=path_help)
    ps_mv.set_defaults(func=cdg_rename)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

import argparse
import mutagen.id3
import rainwave_tools.utils
import sys


def get_groups(path):
    rv = set()
    tags = mutagen.id3.ID3(str(path))
    for group_tag in tags.getall('TCON'):
        for group_text in group_tag.text:
            rv |= set([a.strip() for a in group_text.split(',')])
    return rv


def set_groups(path, groups=None):
    if groups is None:
        groups = set()
    tags = mutagen.id3.ID3(str(path))
    tags.delall('TCON')
    if groups:
        group_tag = ', '.join(groups)
        tags.add(mutagen.id3.TCON(encoding=3, text=[group_tag]))
    tags.save()
    print(f'{path} : cooldown groups: {list(groups)!r}')


def cdg_add(args):
    errors = []
    for f in rainwave_tools.utils.get_mp3s(args.path):
        cdgs = get_groups(f)
        if args.group not in cdgs:
            cdgs.add(args.group)
            try:
                set_groups(f, cdgs)
            except PermissionError as e:
                errors.append(e)
    return errors


def cdg_drop(args):
    errors = []
    for f in rainwave_tools.utils.get_mp3s(args.path):
        cdgs = get_groups(f)
        if args.group in cdgs:
            cdgs.discard(args.group)
            try:
                set_groups(f, cdgs)
            except PermissionError as e:
                errors.append(e)
    return errors


def cdg_find(args):
    errors = []
    for f in rainwave_tools.utils.get_mp3s(args.path):
        try:
            cdgs = get_groups(f)
        except mutagen.id3.ID3NoHeaderError as e:
            errors.append(e)
            continue
        if args.group in cdgs:
            if args.print0:
                print(f, end='\x00')
            else:
                print(f)
    return errors


def cdg_list(args):
    errors = []
    for f in rainwave_tools.utils.get_mp3s(args.path):
        try:
            cdgs = get_groups(f)
        except mutagen.id3.ID3NoHeaderError as e:
            errors.append(e)
            continue
        print(f'{f} : {list(cdgs)}')
    return errors


def cdg_rename(args):
    errors = []
    for f in rainwave_tools.utils.get_mp3s(args.path):
        cdgs = get_groups(f)
        if args.old_group in cdgs:
            cdgs.discard(args.old_group)
            cdgs.add(args.new_group)
            try:
                set_groups(f, cdgs)
            except PermissionError as e:
                errors.append(e)
    return errors


def parse_args():
    ap = argparse.ArgumentParser(description='Manage cooldown groups (genre tags) in mp3 files')
    sp = ap.add_subparsers(dest='command', title='commands')
    sp.required = True

    ls_help = 'Show the current cooldown groups for one or more mp3 files'
    ps_ls = sp.add_parser('ls', aliases=['list'], help=ls_help, description=ls_help)
    ps_ls.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    ps_ls.set_defaults(func=cdg_list)

    find_help = 'Find mp3 files that belong to the specified cooldown group'
    find_print0_help = 'Separate file names with a null character instead of a newline'
    ps_find = sp.add_parser('find', aliases=['search'], help=find_help, description=find_help)
    ps_find.add_argument('-0', '--print0', action='store_true', help=find_print0_help)
    ps_find.add_argument('group', help='The cooldown group to search for')
    ps_find.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    ps_find.set_defaults(func=cdg_find)

    add_help = 'Add a cooldown group to one or more mp3 files'
    ps_add = sp.add_parser('add', help=add_help, description=add_help)
    ps_add.add_argument('group', help='The cooldown group to add to the specified files')
    ps_add.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    ps_add.set_defaults(func=cdg_add)

    rm_help = 'Remove a cooldown group from one or more mp3 files'
    ps_rm = sp.add_parser('rm', aliases=['drop', 'remove'], help=rm_help, description=rm_help)
    ps_rm.add_argument('group', help='The cooldown group to remove from the specified files')
    ps_rm.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    ps_rm.set_defaults(func=cdg_drop)

    mv_help = 'Rename a cooldown group in one or more mp3 files'
    ps_mv = sp.add_parser('mv', aliases=['rename', 'replace'], help=mv_help, description=mv_help)
    ps_mv.add_argument('old_group', help='The current name of the cooldown group that you want to rename')
    ps_mv.add_argument('new_group', help='The new name for the cooldown group that you want to rename')
    ps_mv.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    ps_mv.set_defaults(func=cdg_rename)

    return ap.parse_args()


def main():
    args = parse_args()
    errors = args.func(args)
    if errors:
        print('**********', file=sys.stderr)
        print('* ERRORS *', file=sys.stderr)
        print('**********', file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)


if __name__ == '__main__':
    main()

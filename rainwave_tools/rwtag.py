import argparse
import mutagen.id3
import mutagen.mp3
import rainwave_tools.utils


def log(m):
    print(m)


TAG_SPEC = dict(album='TALB', apic='APIC', art='APIC', artist='TPE1',
                artist2='TPE2', bpm='TBPM', comm='COMM', comment='COMM',
                composer='TCOM', disc='TPOS', encoder='TSSE', genre='TCON',
                isrc='TSRC', lyric='USLT', popm='POPM', priv='PRIV',
                private='PRIV', rva2='RVA2', talb='TALB', tbpm='TBPM',
                tcmp='TCMP', tcom='TCOM', tcon='TCON', tcop='TCOP', tdrc='TDRC',
                tdrl='TDRL', tdtg='TDTG', tenc='TENC', text='TXXX', tflt='TFLT',
                tit1='TIT1', tit2='TIT2', tit3='TIT3', title='TIT2',
                tmed='TMED', toal='TOAL', tope='TOPE', tpe1='TPE1', tpe2='TPE2',
                tpos='TPOS', tpub='TPUB', track='TRCK', trck='TRCK',
                tsrc='TSRC', tsse='TSSE', tsst='TSST', txxx='TXXX', ufid='UFID',
                uslt='USLT', wcom='WCOM', woaf='WOAF', woar='WOAR', www='WXXX',
                wxxx='WXXX', year='TDRC')


def tag_drop(args):
    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        try:
            _md = mutagen.id3.ID3(str(mp3))
        except mutagen.id3.ID3NoHeaderError:
            _md = mutagen.id3.ID3()
        _tag = TAG_SPEC.get(args.tag, args.tag)
        _md.delall(_tag)
        try:
            _md.save()
        except IOError as _ioe:
            log('ERROR : {}'.format(_ioe))
            continue
        log('{} : dropped all tags of type {!r}'.format(mp3, args.tag))


def tag_dump(args):
    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        _md = mutagen.id3.ID3(str(mp3))
        log(_md.pprint())
        log('---------')


def tag_set(args):
    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        try:
            _md = mutagen.id3.ID3(str(mp3))
        except mutagen.id3.ID3NoHeaderError:
            _md = mutagen.id3.ID3()
        _tag = TAG_SPEC.get(args.tag, args.tag)
        if _tag in ['COMM', 'TALB', 'TCON', 'TDRC', 'TIT2', 'TPE1', 'TPOS',
                    'TRCK']:
            _md.delall(_tag)
            tag_class = getattr(mutagen.id3, _tag)
            _md.add(tag_class(encoding=3, text=[args.value]))
        elif _tag == 'WXXX':
            _md.delall(_tag)
            _md.add(mutagen.id3.WXXX(encoding=0, url=args.value))
        _md.save(str(mp3))
        log('{}: {} set to {!r}'.format(mp3, args.tag, args.value))


def tag_show(args):
    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        _audio = mutagen.mp3.MP3(str(mp3))
        log('file    : {}'.format(mp3))
        log('length  : {} seconds'.format(int(_audio.info.length)))
        _md = mutagen.id3.ID3(str(mp3))

        for _frame in _md.getall('TALB'):
            for _text in _frame.text:
                log('album   : {}'.format(_text))

        for _frame in _md.getall('TIT2'):
            for _text in _frame:
                log('title   : {}'.format(_text))

        for _frame in _md.getall('TPE1'):
            for _text in _frame.text:
                log('artist  : {}'.format(_text))

        for _frame in _md.getall('TCON'):
            for _text in _frame:
                log('genre   : {}'.format(_text))

        for _frame in _md.getall('TRCK'):
            for _text in _frame:
                log('track   : {}'.format(_text))

        for _frame in _md.getall('TPOS'):
            for _text in _frame:
                log('disc    : {}'.format(_text))

        for _frame in _md.getall('WXXX'):
            log('www     : {}'.format(_frame.url))

        for _frame in _md.getall('COMM'):
            for _text in _frame:
                log('comment : {}'.format(_text))

        for _frame in _md.getall('TDRC'):
            for _text in _frame:
                log('year    : {}'.format(_text))
        log('---------')


def parse_args():
    description = 'View and edit ID3 tags on MP3 files.'
    ap = argparse.ArgumentParser(description=description)

    sp_desc = ('Specify one of the following commands. To get help on an '
               'individual command, use \'rwtag <command> -h\'.')
    sp = ap.add_subparsers(title='Available commands', description=sp_desc,
                           dest='command')
    sp.required = True

    path_help = ('A file or directory to process. If you specify a directory, '
                 'all files and subdirectories in the directory will be '
                 'processed recursively. Only files with the extension '
                 '\'.mp3\' will be processed. You may specify more than one '
                 'file or directory.')

    drop_desc = 'Remove a tag from one or more MP3 files.'
    ps_drop = sp.add_parser('drop', description=drop_desc,
                            aliases=['remove', 'rm'])
    ps_drop.add_argument('tag', help='The name of the tag to remove.')
    ps_drop.add_argument('path', nargs='+', help=path_help)
    ps_drop.set_defaults(func=tag_drop)

    dump_desc = 'Show all tags on one or more MP3 files.'
    ps_dump = sp.add_parser('dump', description=dump_desc)
    ps_dump.add_argument('path', nargs='+', help=path_help)
    ps_dump.set_defaults(func=tag_dump)

    set_desc = 'Set a tag to a certain value on one or more MP3 files.'
    ps_set = sp.add_parser('set', description=set_desc)
    ps_set.add_argument('tag', help='The name of the tag to set.')
    ps_set.add_argument('value', help='The value to set for the tag.')
    ps_set.add_argument('path', nargs='+', help=path_help)
    ps_set.set_defaults(func=tag_set)

    show_desc = ('Show only tags that Rainwave cares about on one or more MP3 '
                 'files.')
    ps_show = sp.add_parser('show', description=show_desc)
    ps_show.add_argument('path', nargs='+', help=path_help)
    ps_show.set_defaults(func=tag_show)

    return ap.parse_args()


def main():
    args = parse_args()
    args.func(args)

if __name__ == '__main__':
    main()

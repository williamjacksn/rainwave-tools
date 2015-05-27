#!/usr/bin/env python3

import mutagen.id3
import mutagen.mp3
import sys


def log(message):
    print(message)


def usage(exit_code=0):
    log('Usage : rwtag help')
    log('         - show this help')
    log('   or : rwtag drop <tag> <filename>')
    log('         - delete all tags of type <tag> from <filename>')
    log('   or : rwtag dump <filename>')
    log('         - display all available metadata (ugly)')
    log('   or : rwtag set <tag> <value> <filename>')
    log('         - set <tag> to <value> on <filename>')
    log('           <tag> can be one of album, title, artist, genre, track, '
        'disc, www, comment, year')
    log('   or : rwtag show <filename>')
    log('         - show tags in an mp3 file')
    exit(exit_code)

tag_spec = dict(album='TALB', art='APIC', artist='TPE1', artist2='TPE2',
                bpm='TBPM', comment='COMM', composer='TCOM', disc='TPOS',
                encoder='TSSE', genre='TCON', isrc='TSRC', popm='POPM',
                private='PRIV', tcmp='TCMP', tcop='TCOP', tdrl='TDRL',
                tdtg='TDTG', tenc='TENC', text='TXXX', tflt='TFLT', tit1='TIT1',
                tit3='TIT3', title='TIT2', tmed='TMED', toal='TOAL',
                tope='TOPE', tpub='TPUB', track='TRCK', tsst='TSST',
                ufid='UFID', wcom='WCOM', woaf='WOAF', woar='WOAR', www='WXXX',
                year='TDRC')

if len(sys.argv) > 1:
    cmd = sys.argv[1]
else:
    log('ERROR : missing command')
    usage(1)

if cmd == 'help':
    usage()
elif cmd == 'drop':
    if len(sys.argv) > 2:
        tag = sys.argv[2]
        if tag in tag_spec.keys():
            if len(sys.argv) > 3:
                for fn in sys.argv[3:]:
                    try:
                        md = mutagen.id3.ID3(fn)
                    except IOError as ioe:
                        log('ERROR : {}'.format(ioe))
                        continue
                    except mutagen.id3.ID3NoHeaderError:
                        md = mutagen.id3.ID3()
                    md.delall(tag_spec[tag])
                    try:
                        md.save()
                    except IOError as ioe:
                        log('ERROR : {}'.format(ioe))
                        continue
                    log('{}: dropped all tags of type {!r}'.format(fn, tag))
            else:
                log('ERROR : missing filename')
                usage(1)
        else:
            log('ERROR : {!r} is not a valid tag name'.format(tag))
            usage(1)
    else:
        log('ERROR : missing tag name')
        usage(1)
elif cmd == 'dump':
    if len(sys.argv) > 2:
        for fn in sys.argv[2:]:
            try:
                md = mutagen.mp3.MP3(fn)
            except IOError as ioe:
                log('ERROR : {}'.format(ioe))
                continue
            log(str(md))
            log('---------')
    else:
        log('ERROR : missing filename')
        usage(1)
elif cmd == 'set':
    if len(sys.argv) > 2:
        tag = sys.argv[2]
        if tag in tag_spec.keys():
            if len(sys.argv) > 3:
                value = sys.argv[3]
                if len(sys.argv) > 4:
                    for fn in sys.argv[4:]:
                        try:
                            md = mutagen.id3.ID3(fn)
                        except IOError as ioe:
                            log('ERROR : {}'.format(ioe))
                            continue
                        except mutagen.id3.ID3NoHeaderError:
                            md = mutagen.id3.ID3()
                        if tag == 'album':
                            md.delall('TALB')
                            md.add(mutagen.id3.TALB(encoding=3, text=[value]))
                        elif tag == 'title':
                            md.delall('TIT2')
                            md.add(mutagen.id3.TIT2(encoding=3, text=[value]))
                        elif tag == 'artist':
                            md.delall('TPE1')
                            md.add(mutagen.id3.TPE1(encoding=3, text=[value]))
                        elif tag == 'genre':
                            md.delall('TCON')
                            md.add(mutagen.id3.TCON(encoding=3, text=[value]))
                        elif tag == 'track':
                            md.delall('TRCK')
                            md.add(mutagen.id3.TRCK(encoding=3, text=[value]))
                        elif tag == 'disc':
                            md.dellall('TPOS')
                            md.add(mutagen.id3.TPOS(encoding=3, text=[value]))
                        elif tag == 'www':
                            md.delall('WXXX')
                            md.add(mutagen.id3.WXXX(encoding=0, url=value))
                        elif tag == 'comment':
                            md.delall('COMM')
                            md.add(mutagen.id3.COMM(encoding=3, text=[value]))
                        elif tag == 'year':
                            md.delall('TDRC')
                            md.add(mutagen.id3.TDRC(encoding=3, text=[value]))
                        md.save(fn)
                        log('{}: {} set to {!r}'.format(fn, tag, value))
                else:
                    log('ERROR : missing filename')
                    usage(1)
            else:
                log('ERROR : missing tag value')
                usage(1)
        else:
            log('ERROR : {!r} is not a valid tag name'.format(tag))
            usage(1)
    else:
        log('ERROR : missing tag name')
        usage(1)
elif cmd == 'show':
    if len(sys.argv) > 2:
        for fn in sys.argv[2:]:
            try:
                audio = mutagen.mp3.MP3(fn)
            except IOError as ioe:
                log('ERROR : {}'.format(ioe))
                continue

            log('file    : {}'.format(fn))
            log('length  : {} seconds'.format(int(audio.info.length)))

            try:
                md = mutagen.id3.ID3(fn)
            except mutagen.id3.ID3NoHeaderError:
                md = mutagen.id3.ID3()

            album_frames = md.getall('TALB')
            for frame in album_frames:
                for txt in frame.text:
                    log('album   : {}'.format(txt))

            title_frames = md.getall('TIT2')
            for frame in title_frames:
                for text in frame:
                    log('title   : {}'.format(text))

            artist_frames = md.getall('TPE1')
            for frame in artist_frames:
                for txt in frame.text:
                    log('artist  : {}'.format(txt))

            genre_frames = md.getall('TCON')
            for frame in genre_frames:
                for text in frame:
                    log('genre   : {}'.format(text))

            track_frames = md.getall('TRCK')
            for frame in track_frames:
                for text in frame:
                    log('track   : {}'.format(text))

            disc_frames = md.getall('TPOS')
            for frame in disc_frames:
                for text in frame:
                    log('disc    : {}'.format(text))

            www_frames = md.getall('WXXX')
            for frame in www_frames:
                log('www     : {}'.format(frame.url))

            comment_frames = md.getall('COMM')
            for frame in comment_frames:
                for text in frame:
                    log('comment : {}'.format(text))

            year_frames = md.getall('TDRC')
            for frame in year_frames:
                for text in frame:
                    log('year    : {}'.format(text))
            log('---------')

    else:
        log('ERROR : missing filename')
        usage(1)
else:
    log('ERROR : {!r} is not a valid command'.format(cmd))
    usage(1)

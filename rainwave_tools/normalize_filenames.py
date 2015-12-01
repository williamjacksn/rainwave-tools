import argparse
import mutagen.id3
import rainwave_tools.ocremix
import rainwave_tools.utils


def log(m):
    print('{}'.format(m))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--include-album', action='store_true')
    parser.add_argument('path', nargs='*', default='.')
    return parser.parse_args()


def main():
    args = parse_args()

    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        log('** {}'.format(mp3))
        tags = mutagen.id3.ID3(str(mp3))
        title = tags.getall('TIT2')[0].text[0]
        safe_title = rainwave_tools.ocremix.OCReMix.make_safe(title)
        new_name = safe_title + '.mp3'
        if args.include_album:
            album = tags.getall('TALB')[0].text[0]
            safe_album = rainwave_tools.ocremix.OCReMix.make_safe(album)
            new_name = safe_album + '_' + new_name
        new_file = mp3.with_name(new_name)
        log('-> {}'.format(new_file))
        mp3.rename(new_file)

if __name__ == '__main__':
    main()

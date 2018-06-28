import argparse
import mutagen.id3
import rainwave_tools.utils


def log(m):
    print(m)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('old_name')
    parser.add_argument('new_name')
    parser.add_argument('path', nargs='*', default='.', help=rainwave_tools.utils.path_help)
    return parser.parse_args()


def main():
    args = parse_args()
    change_count = 0
    errors = []

    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        changed = False
        tags = mutagen.id3.ID3(str(mp3))
        artist_tag = tags.getall('TPE1')[0].text[0]
        artists = [a.strip() for a in artist_tag.split(',')]
        for i, artist in enumerate(artists):
            if artist == args.old_name:
                artists[i] = args.new_name
                changed = True
        if changed:
            artist_tag = ', '.join(artists)
            tags.delall('TPE1')
            tags.add(mutagen.id3.TPE1(encoding=3, text=[artist_tag]))
            try:
                tags.save()
            except PermissionError as e:
                errors.append(e)
            else:
                change_count += 1
                log(f'{mp3} : new artist tag {artist_tag!r}')

    m = f'** updated tags in {change_count} file'
    if change_count != 1:
        m = f'{m}s'
    log(m)
    if errors:
        log('**********')
        log('* ERRORS *')
        log('**********')
        for error in errors:
            log(error)


if __name__ == '__main__':
    main()

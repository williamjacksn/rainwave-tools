import argparse
import mutagen.id3
import rainwave_tools.utils


def log(message):
    print(f'** {message}')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    return parser.parse_args()


def main():
    args = parse_args()

    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        log(mp3)
        tags = mutagen.id3.ID3(str(mp3))

        album = tags.getall('TALB')[0].text[0]
        new_album = input(f'album [{album}] > ')
        if new_album:
            tags.delall('TALB')
            tags.add(mutagen.id3.TALB(encoding=3, text=[new_album]))
            tags.save()

        title = tags.getall('TIT2')[0].text[0]
        new_title = input(f'title [{title}] > ')
        if new_title:
            tags.delall('TIT2')
            tags.add(mutagen.id3.TIT2(encoding=3, text=[new_title]))
            tags.save()

        artist = tags.getall('TPE1')[0].text[0]
        new_artist = input(f'artist [{artist}] > ')
        if new_artist:
            tags.delall('TPE1')
            tags.add(mutagen.id3.TPE1(encoding=3, text=[new_artist]))
            tags.save()


if __name__ == '__main__':
    main()

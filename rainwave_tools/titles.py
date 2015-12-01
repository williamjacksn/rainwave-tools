import argparse
import mutagen.id3
import rainwave_tools.utils


def log(m):
    print(m)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='*', default='.')
    return parser.parse_args()


def main():
    args = parse_args()

    change_count = 0

    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        tags = mutagen.id3.ID3(str(mp3))
        title = tags.getall('TIT2')[0].text[0]
        new_title = input('{} [{}] > '.format(mp3, title))
        if new_title:
            change_count += 1
            tags.delall('TIT2')
            tags.add(mutagen.id3.TIT2(encoding=3, text=[new_title]))
            tags.save()

    m = '** updated tags in {} file'.format(change_count)
    if change_count != 1:
        m = '{}s'.format(m)
    log(m)

if __name__ == '__main__':
    main()

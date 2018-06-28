import argparse
import logging
import mutagen.id3
import rainwave_tools
import sys

log = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    return parser.parse_args()


def main():
    logging.basicConfig(stream=sys.stdout, level='INFO', format='%(message)s')
    args = parse_args()

    change_count = 0

    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        tags = mutagen.id3.ID3(str(mp3))
        titles = tags.getall('TIT2')
        if titles:
            title = tags.getall('TIT2')[0].text[0]
        else:
            title = ''
        new_title = input(f'{mp3} [{title}] > ')
        if new_title:
            change_count += 1
            tags.delall('TIT2')
            tags.add(mutagen.id3.TIT2(encoding=3, text=[new_title]))
            tags.save()

    m = f'** updated tags in {change_count} file'
    if change_count != 1:
        m = f'{m}s'
    log.info(m)


if __name__ == '__main__':
    main()

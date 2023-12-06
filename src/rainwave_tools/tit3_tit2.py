import argparse
import mutagen.id3
import rainwave_tools.utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='+', help=rainwave_tools.utils.path_help)
    return parser.parse_args()


def main():
    args = parse_args()
    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        tags = mutagen.id3.ID3(str(mp3))
        tit3 = tags.getall('TIT3')[0].text[0]
        tags.delall('TIT2')
        tags.add(mutagen.id3.TIT2(encoding=3, text=[tit3]))
        tags.save()


if __name__ == '__main__':
    main()

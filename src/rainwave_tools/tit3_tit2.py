import argparse

import mutagen.id3

from rainwave_tools import utils


class Args:
    path: list[str]


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="+", help=utils.path_help)
    return parser.parse_args(namespace=Args())


def main() -> None:
    args = parse_args()
    for mp3 in utils.get_mp3s(args.path):
        tags = mutagen.id3.ID3(str(mp3))
        tit3 = tags.getall("TIT3")[0].text[0]
        tags.delall("TIT2")
        tags.add(mutagen.id3.TIT2(encoding=3, text=[tit3]))
        tags.save()


if __name__ == "__main__":
    main()

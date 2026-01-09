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
        utils.log(f"** {mp3}")
        tags = mutagen.id3.ID3(str(mp3))

        album = tags.getall("TALB")[0].text[0]
        new_album = input(f"album [{album}] > ")
        if new_album:
            tags.delall("TALB")
            tags.add(mutagen.id3.TALB(encoding=3, text=[new_album]))
            tags.save()

        title = tags.getall("TIT2")[0].text[0]
        new_title = input(f"title [{title}] > ")
        if new_title:
            tags.delall("TIT2")
            tags.add(mutagen.id3.TIT2(encoding=3, text=[new_title]))
            tags.save()

        artist = tags.getall("TPE1")[0].text[0]
        new_artist = input(f"artist [{artist}] > ")
        if new_artist:
            tags.delall("TPE1")
            tags.add(mutagen.id3.TPE1(encoding=3, text=[new_artist]))
            tags.save()


if __name__ == "__main__":
    main()

import argparse

import mutagen.id3

from rainwave_tools import utils


class Args:
    include_album: bool
    path: list[str]


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--include-album", action="store_true")
    parser.add_argument("path", nargs="+", help=utils.path_help)
    return parser.parse_args(namespace=Args())


def main() -> None:
    args = parse_args()

    for mp3 in utils.get_mp3s(args.path):
        utils.log(f"** {mp3}")
        tags = mutagen.id3.ID3(str(mp3))
        title = tags.getall("TIT2")[0].text[0]
        safe_title = utils.make_safe(title)
        new_name = f"{safe_title}.mp3"
        if args.include_album:
            album = tags.getall("TALB")[0].text[0]
            safe_album = utils.make_safe(album)
            new_name = f"{safe_album}_{new_name}"
        new_file = mp3.with_name(new_name)
        utils.log(f"-> {new_file}")
        mp3.rename(new_file)


if __name__ == "__main__":
    main()

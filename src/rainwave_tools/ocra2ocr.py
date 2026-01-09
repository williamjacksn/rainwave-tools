import argparse

import mutagen.id3

from rainwave_tools import utils


class Args:
    file: str
    url: str


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("url")
    return parser.parse_args(namespace=Args())


def main() -> None:
    args = parse_args()

    tags = mutagen.id3.ID3(args.file)
    utils.log(f"{args.file} : setting www to {args.url}")
    tags.delall("WXXX")
    tags.add(mutagen.id3.WXXX(encoding=0, url=args.url))
    comment = "Get @ OCR"
    utils.log(f"{args.file} : setting comment to {comment!r}")
    tags.delall("COMM")
    tags.add(mutagen.id3.COMM(encoding=3, text=[comment]))
    tags.save()


if __name__ == "__main__":
    main()

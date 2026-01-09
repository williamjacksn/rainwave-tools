import argparse

import mutagen.id3

from rainwave_tools import utils


class Args:
    old_name: str
    new_name: str
    path: list[str]


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("old_name")
    parser.add_argument("new_name")
    parser.add_argument("path", nargs="*", default=".", help=utils.path_help)
    return parser.parse_args(namespace=Args())


def main() -> None:
    args = parse_args()
    change_count = 0
    errors = []

    for mp3 in utils.get_mp3s(args.path):
        changed = False
        tags = mutagen.id3.ID3(str(mp3))
        artist_tag = tags.getall("TPE1")[0].text[0]
        artists = [a.strip() for a in artist_tag.split(",")]
        for i, artist in enumerate(artists):
            if artist == args.old_name:
                artists[i] = args.new_name
                changed = True
        if changed:
            artist_tag = ", ".join(artists)
            tags.delall("TPE1")
            tags.add(mutagen.id3.TPE1(encoding=3, text=[artist_tag]))
            try:
                tags.save()
            except PermissionError as e:
                errors.append(e)
            else:
                change_count += 1
                utils.log(f"{mp3} : new artist tag {artist_tag!r}")

    m = f"** updated tags in {change_count} file"
    if change_count != 1:
        m = f"{m}s"
    utils.log(m)
    if errors:
        utils.log("**********")
        utils.log("* ERRORS *")
        utils.log("**********")
        for error in errors:
            utils.log(error)


if __name__ == "__main__":
    main()

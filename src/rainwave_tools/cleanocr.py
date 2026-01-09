import argparse
import re

import mutagen.id3

from rainwave_tools import ocremix, utils


class Args:
    titles: bool
    urls: bool
    path: list[str]


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--titles", action="store_true", help="update titles")
    parser.add_argument("-u", "--urls", action="store_true", help="update URLs")
    parser.add_argument("path", nargs="+", help=utils.path_help)
    return parser.parse_args(namespace=Args())


def get_url(tags: mutagen.id3.ID3) -> str:
    for frame in tags.getall("WXXX"):
        return frame.url


def main() -> None:
    args = parse_args()

    for mp3 in utils.get_mp3s(args.path):
        ocr_id = None
        changed = False
        tags = mutagen.id3.ID3(str(mp3))
        url = get_url(tags)
        if url:
            for match in re.findall("OCR\d{5}", url):
                ocr_id = int(match[3:])
        if ocr_id is None:
            utils.log(f"{mp3} : not an OCR url")
            continue
        remix = ocremix.OCReMix(ocr_id)

        if args.urls:
            if remix.info_url != url:
                utils.log(f"{mp3} : updating url to {remix.info_url}")
                tags.delall("WXXX")
                tags.add(mutagen.id3.WXXX(encoding=0, url=remix.info_url))
                changed = True

        if args.titles:
            tag_title = tags.getall("TIT2")[0][0]
            if remix.title != tag_title:
                utils.log(f"{mp3} : updating title to {remix.title}")
                tags.delall("TIT2")
                tags.add(mutagen.id3.TIT2(encoding=3, text=[remix.title]))
                changed = True

        if changed:
            tags.save()


if __name__ == "__main__":
    main()

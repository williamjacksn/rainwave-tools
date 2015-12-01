import argparse
import mutagen.id3
import rainwave_tools.ocremix
import rainwave_tools.utils
import re


def log(m):
    print(m)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='*', default='.')
    return parser.parse_args()


def main():
    args = parse_args()

    for mp3 in rainwave_tools.utils.get_mp3s(args.path):
        ocr_id = None
        changed = False
        tags = mutagen.id3.ID3(str(mp3))
        tag_www = tags.getall('WXXX')[0].url
        for match in re.findall('OCR\d{5}', tag_www):
            ocr_id = int(match[3:])
        if ocr_id is None:
            log('{} : not an OCR url'.format(mp3))
            continue
        remix = rainwave_tools.ocremix.OCReMix(ocr_id)
        try:
            remix.load_from_url()
        except:
            log('{} : could not load url {}'.format(mp3, remix.info_url))
            continue

        if remix.info_url != tag_www:
            log('{} : updating www to {}'.format(mp3, remix.info_url))
            tags.delall('WXXX')
            tags.add(mutagen.id3.WXXX(encoding=0, url=remix.info_url))
            changed = True

        tag_title = tags.getall('TIT2')[0][0]
        if remix.title != tag_title:
            log('{} : updating title to {}'.format(mp3, remix.title))
            tags.delall('TIT2')
            tags.add(mutagen.id3.TIT2(encoding=3, text=[remix.title]))
            changed = True

        if changed:
            tags.save()
        else:
            log('{} : no change'.format(mp3))

if __name__ == '__main__':
    main()

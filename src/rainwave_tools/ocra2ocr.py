import argparse
import mutagen.id3


def log(m):
    print(m)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('url')
    return parser.parse_args()


def main():
    args = parse_args()

    tags = mutagen.id3.ID3(args.file)
    log(f'{args.file} : setting www to {args.url}')
    tags.delall('WXXX')
    tags.add(mutagen.id3.WXXX(encoding=0, url=args.url))
    comment = 'Get @ OCR'
    log(f'{args.file} : setting comment to {comment!r}')
    tags.delall('COMM')
    tags.add(mutagen.id3.COMM(encoding=3, text=[comment]))
    tags.save()


if __name__ == '__main__':
    main()

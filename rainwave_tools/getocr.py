import argparse
import mutagen.id3
import os
import rainwave_tools.ocremix
import stat
import urllib.request

DEST_DIR = '/home/icecast/ocr-staging'
COMMENT = 'Get @ OCR'
GENRE_PROMPT = 'Enter a genre > '


def log(m):
    print(m)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ocr_num', type=int)
    return parser.parse_args()


def main():
    args = parse_args()

    log(f'Processing OCR{args.ocr_num:05}')
    remix = rainwave_tools.ocremix.OCReMix(args.ocr_num)

    log(f'Downloading mp3 file from {remix.mp3_url}')
    temp_file, _ = urllib.request.urlretrieve(remix.mp3_url)
    log(f'Downloaded mp3 file to {temp_file}')

    tags = mutagen.id3.ID3(temp_file)

    log(f'Setting TALB (album) to {remix.album!r}')
    tags.delall('TALB')
    tags.add(mutagen.id3.TALB(encoding=3, text=[remix.album]))

    log(f'Setting TIT2 (title) to {remix.title!r}')
    tags.delall('TIT2')
    tags.add(mutagen.id3.TIT2(encoding=3, text=[remix.title]))

    log(f'Setting TPE1 (artist) to {remix.artist!r}')
    tags.delall('TPE1')
    tags.add(mutagen.id3.TPE1(encoding=3, text=[remix.artist]))

    log(f'Setting WXXX (www) to {remix.info_url!r}')
    tags.delall('WXXX')
    tags.add(mutagen.id3.WXXX(encoding=0, url=remix.info_url))

    log(f'Setting COMM (comment) to {COMMENT!r}')
    tags.delall('COMM')
    tags.add(mutagen.id3.COMM(encoding=3, text=[COMMENT]))

    if remix.has_lyrics:
        log('** This remix has lyrics!')

    tags.delall('TCON')
    genre = input(GENRE_PROMPT)
    if genre:
        log(f'Setting TCON (genre) to {genre!r}')
        tags.add(mutagen.id3.TCON(encoding=3, text=[genre]))

    log('Dropping unnecessary tags')
    for tag in ['APIC', 'TCMP', 'TCOM', 'TCOP', 'TDRC', 'TENC', 'TIT1', 'TIT3', 'TOAL', 'TOPE', 'TPE2', 'TPUB', 'TRCK',
                'TSSE', 'TXXX', 'USLT', 'WOAR']:
        tags.delall(tag)

    tags.save(temp_file)

    target_file = f'{remix.safe_title}.mp3'
    mp3_dest = os.path.join(DEST_DIR, remix.safe_album, target_file)
    log(f'Moving {temp_file} to {mp3_dest}')
    os.renames(temp_file, mp3_dest)

    log('Changing file permissions')
    perms = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP
    os.chmod(mp3_dest, perms)

    log('Cleaning up temporary files')
    urllib.request.urlcleanup()


if __name__ == '__main__':
    main()

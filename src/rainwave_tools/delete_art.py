import argparse
import pathlib


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', default='/var/www/rainwave.cc/album_art', type=pathlib.Path)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('album_id', type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    pattern = f'*_{args.album_id}_*'
    for f in args.folder.glob(pattern):
        print(f'Deleting {f}')
        if args.live:
            f.unlink()

    if not args.live:
        print('**')
        print('** No files were deleted. Use --live to actually delete files.')
        print('**')

if __name__ == '__main__':
    main()

import argparse
import pathlib


class Args:
    folder: pathlib.Path
    live: bool
    album_id: int


def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--folder", default="/var/www/rainwave.cc/album_art", type=pathlib.Path
    )
    parser.add_argument("--live", action="store_true")
    parser.add_argument("album_id", type=int)
    return parser.parse_args(namespace=Args())


def main() -> None:
    args = parse_args()
    pattern = f"*_{args.album_id}_*"
    for f in args.folder.glob(pattern):
        print(f"Deleting {f}")
        if args.live:
            f.unlink()

    if not args.live:
        print("**")
        print("** No files were deleted. Use --live to actually delete files.")
        print("**")


if __name__ == "__main__":
    main()

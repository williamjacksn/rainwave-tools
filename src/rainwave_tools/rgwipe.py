import argparse

import mutagen.id3

from rainwave_tools import utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="+", help=utils.path_help)
    return parser.parse_args()


def main():
    args = parse_args()

    for mp3 in utils.get_mp3s(args.path):
        tags = mutagen.id3.ID3(str(mp3))
        tags.delall("RVA2")
        tags.delall("TXXX:MP3GAIN_MINMAX")
        tags.delall("TXXX:replaygain_album_gain")
        tags.delall("TXXX:replaygain_album_peak")
        tags.delall("TXXX:replaygain_reference_loudness")
        tags.delall("TXXX:replaygain_track_gain")
        tags.delall("TXXX:replaygain_track_peak")
        tags.save()
        utils.log("** wiped replaygain tags from {}".format(mp3))


if __name__ == "__main__":
    main()

import pathlib

from typing import Any

__all__ = ['get_mp3s', 'make_safe', 'path_help']


def get_mp3s(paths: Any):
    if not isinstance(paths, list):
        paths = [paths]
    for path in paths:
        if isinstance(path, pathlib.Path):
            p = path.resolve()
        else:
            p = pathlib.Path(path).resolve()
        if p.is_dir():
            for item in p.iterdir():
                for mp3 in get_mp3s(item):
                    yield mp3
        else:
            if p.suffix.lower() == '.mp3':
                yield p


# Special characters sorted by results of ord()
# {
#  '²': 178
#  'É': 201,
#  'Ü': 220,
#  'à': 224,
#  'á': 225,
#  'â': 226,
#  'ã': 227,
#  'ä': 228,
#  'ç': 231,
#  'è': 232,
#  'é': 233,
#  'ê': 234,
#  'í': 237,
#  'ð', 240,
#  'ñ': 241,
#  'ó': 243,
#  'ö': 246,
#  'ú': 250,
#  'ü': 252,
#  'ş': 351,
#  'К': 1050,
#  'С': 1057,
#  'а': 1072,
#  'в': 1074,
#  'е': 1077,
#  'и': 1080,
#  'й': 1081,
#  'к': 1082,
#  'м': 1084,
#  'н': 1085,
#  'о': 1086,
#  'с': 1089,
#  'т': 1090
# }

def make_safe(s):
    translate_table = {ord(char): None for char in ' !"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~–—あいごま고말싶은하'}
    special = dict(zip(map(ord, '²ÉÜàáâãäçèéêíðñóöúüşКСавеийкмност'), '2EUaaaaaceeeidnoouusKSaveijkmnost'))
    translate_table.update(special)
    return s.translate(translate_table)


path_help = ("A file or directory to process. If you specify a directory, all files and subdirectories in the "
             "directory will be processed recursively. Only files with the extension '.mp3' will be processed. You may "
             "specify more than one file or directory.")

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


def make_safe(s):
    translate_table = {ord(char): None for char in ' !"#%&\'()*+,-./:;<=>?@[\\]^_`{|}~–—あいごま'}
    special = dict(zip(map(ord, 'àáãäÉéêèíñóöşÜüСоветскийКмна'), 'aaaaEeeeinoosUuSovetskijKmna'))
    translate_table.update(special)
    return s.translate(translate_table)


path_help = ("A file or directory to process. If you specify a directory, all files and subdirectories in the "
             "directory will be processed recursively. Only files with the extension '.mp3' will be processed. You may "
             "specify more than one file or directory.")

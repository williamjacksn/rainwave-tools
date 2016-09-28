import pathlib

__all__ = ['get_mp3s', 'make_safe']


def get_mp3s(paths):
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
    unsafe = ' !"#%&\'()*+,-./:;<=>?@[\]^_`{|}~—あいごま'
    translate_table = {ord(char): None for char in unsafe}
    special = dict(zip(map(ord, 'áäÉéêèíñóöşÜüСоветскийКмна'), 'aaEeeeinoosUuSovetskijKmna'))
    translate_table.update(special)
    return s.translate(translate_table)

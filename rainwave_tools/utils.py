import pathlib

__all__ = ['get_mp3s']


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

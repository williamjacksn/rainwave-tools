import rainwave_tools

from setuptools import find_packages, setup

REQUIREMENTS = []
with open('requirements.txt') as f:
    while True:
        req = f.readline()
        if req == '':
            break
        REQUIREMENTS.append(req.strip())

setup(
    name="rainwave-tools",
    version=rainwave_tools.__version__,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'apply_genres = rainwave_tools.apply_genres:main',
            'assign_genres = rainwave_tools.assign_genres:main',
            'cdg = rainwave_tools.cdg:main',
            'cleanocr = rainwave_tools.cleanocr:main',
            'getocr = rainwave_tools.getocr:main',
            'missing_art = rainwave_tools.missing_art:main',
            'normalize_filenames = rainwave_tools.normalize_filenames:main',
            'ocra2ocr = rainwave_tools.ocra2ocr:main',
            'rename_artist = rainwave_tools.rename_artist:main',
            'retag = rainwave_tools.retag:main',
            'rgwipe = rainwave_tools.rgwipe:main',
            'rwtag = rainwave_tools.rwtag:main',
            'song_search = rainwave_tools.song_search:main',
            'titles = rainwave_tools.titles:main',
            'url_check = rainwave_tools.url_check:main'
        ]
    }
)

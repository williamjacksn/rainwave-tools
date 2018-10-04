from setuptools import find_packages, setup

setup(
    name="rainwave-tools",
    version='0.7.1',
    author='William Jackson',
    author_email='william@subtlecoolness.com',
    url='https://github.com/williamjacksn/rainwave_tools',
    description='Tools for maintaining a local library of music for Rainwave',
    license='MIT License',
    packages=find_packages(),
    install_requires=['lxml', 'mutagen', 'psycopg2', 'requests'],
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
            'tit3_tit2 = rainwave_tools.tit3_tit2:main',
            'titles = rainwave_tools.titles:main',
            'url_check = rainwave_tools.url_check:main'
        ]
    }
)

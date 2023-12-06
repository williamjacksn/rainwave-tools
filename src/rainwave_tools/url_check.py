import argparse
import json
import mutagen.id3
import os
import pathlib
import psycopg2
import requests
import sys

from requests.exceptions import ConnectionError, MissingSchema, ReadTimeout
from urllib3.exceptions import ReadTimeoutError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--skip', help='skip URLs that match this substring')
    return parser.parse_args()


def get_config():
    data = {}
    home = pathlib.Path(os.environ.get('HOME')).resolve()
    config = home / '.config/rainwave_tools/url_check.json'
    if not config.parent.exists():
        config.parent.mkdir(parents=True)
    if config.exists():
        with config.open() as f:
            data = json.load(f)
    return data


def set_config(c):
    home = pathlib.Path(os.environ.get('HOME')).resolve()
    config = home / '.config/rainwave_tools/url_check.json'
    if not config.parent.exists():
        config.parent.mkdir(parents=True)
    with config.open('w') as f:
        json.dump(c, f, indent=1)


def get_files_with_url(cnx, url):
    files = []
    sql = '''
        SELECT DISTINCT song_filename
        FROM r4_songs
        WHERE song_verified IS TRUE AND song_url = %s
        ORDER BY song_filename
    '''
    with cnx.cursor() as cur:
        cur.execute(sql, [url])
        rows = cur.fetchall()

    for row in rows:
        files.append(str(row[0]))

    return files


def replace_url(cnx, old_url, new_url):
    sql = '''
        SELECT DISTINCT song_filename
        FROM r4_songs
        WHERE song_verified IS TRUE AND song_url = %s
        ORDER BY song_filename
    '''
    with cnx.cursor() as cur:
        cur.execute(sql, [old_url])
        files = cur.fetchall()

    for file in files:
        filename = str(file[0])
        tags = mutagen.id3.ID3(filename)
        tags.delall('WXXX')
        tags.add(mutagen.id3.WXXX(encoding=0, url=new_url))
        tags.save()
        print(f'{filename} : new www {new_url!r}')


def main():
    args = parse_args()

    if args.skip:
        print(f'Skipping URLS that match: {args.skip}')

    if 'RW_DB_PASS' in os.environ:
        rw_db_pass = os.environ.get('RW_DB_PASS')
    else:
        print('Please set the RW_DB_PASS environment variable.')
        sys.exit()

    c = get_config()

    cnx = psycopg2.connect(f'dbname=rainwave user=orpheus password={rw_db_pass}')

    sql = 'SELECT DISTINCT song_url FROM r4_songs WHERE song_verified IS TRUE ORDER BY song_url'
    with cnx.cursor() as cur:
        cur.execute(sql)
        urls = cur.fetchall()

    count = 0
    for row in urls:
        count += 1
        print(f'{count}\r', end='')
        url = str(row[0])
        if url is None or url in c.get('good_urls', []):
            continue
        if args.skip and args.skip in url:
            continue
        try:
            resp = requests.head(url, timeout=1)
            if resp.status_code in [403, 405]:
                resp = requests.get(url, timeout=1)
            if resp.status_code == 200:
                good_urls = c.get('good_urls', [])
                good_urls.append(url)
                c['good_urls'] = good_urls
                set_config(c)
                continue
            else:
                code = resp.status_code
        except (MissingSchema, ConnectionError, ReadTimeout, ReadTimeoutError, TimeoutError):
            code = '---'
        while True:
            new_url = input('{} {} > '.format(code, url))
            if new_url == '?':
                for file in get_files_with_url(cnx, url):
                    print('  * ' + file)
            elif new_url:
                replace_url(cnx, url, new_url)
                break
            else:
                break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

#!/usr/bin/env python3

import json
import mutagen.id3
import os
import pathlib
import psycopg2
import requests
import requests.exceptions
import sys


def log(message):
    print(message)


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
        json.dump(c, f)


def main():
    if 'RW_DB_PASS' in os.environ:
        rw_db_pass = os.environ.get('RW_DB_PASS')
    else:
        log('Please set the RW_DB_PASS environment variable.')
        sys.exit()

    c = get_config()

    cnx_string = 'dbname=rainwave user=orpheus password={}'.format(rw_db_pass)
    cnx = psycopg2.connect(cnx_string)

    with cnx.cursor() as cur:
        sql = ('select distinct song_url from r4_songs where song_verified is '
               'true order by song_url')
        cur.execute(sql)
        urls = cur.fetchall()

    def replace_url(old_url, _new_url):
        with cnx.cursor() as cur:
            sql = ('select distinct song_filename from r4_songs where '
                   'song_verified is true and song_url = %s order by '
                   'song_filename')
            cur.execute(sql, [old_url])
            files = cur.fetchall()

        for file in files:
            filename = str(file[0])
            tags = mutagen.id3.ID3(filename)
            tags.delall('WXXX')
            tags.add(mutagen.id3.WXXX(encoding=0, url=_new_url))
            tags.save()
            log('{} : new www {!r}'.format(filename, _new_url))

    count = 0
    for row in urls:
        count += 1
        print('{}\r'.format(count), end='')
        url = str(row[0])
        if url in c.get('good_urls', []):
            continue
        try:
            resp = requests.head(url)
            if resp.status_code == 200:
                good_urls = c.get('good_urls', [])
                good_urls.append(url)
                c['good_urls'] = good_urls
                set_config(c)
                continue
            else:
                code = resp.status_code
        except requests.exceptions.MissingSchema:
            code = '---'
        new_url = input('{} {} > '.format(code, url))
        if new_url:
            replace_url(url, new_url)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

#!/usr/bin/env python3

import os
import pathlib
import psycopg2
import sys


def log(m):
    print(m)


def main():
    if 'RW_DB_PASS' in os.environ:
        rw_db_pass = os.environ.get('RW_DB_PASS')
    else:
        log('Please set the RW_DB_PASS environment variable.')
        sys.exit()

    cnx_string = 'dbname=rainwave user=orpheus password={}'.format(rw_db_pass)
    cnx = psycopg2.connect(cnx_string)

    with cnx.cursor() as cur:
        sql = '''SELECT DISTINCT album_id, album_name FROM r4_songs JOIN
                 r4_albums USING (album_id) WHERE song_verified IS TRUE'''
        cur.execute(sql)
        rows = cur.fetchall()

    art_dir = pathlib.Path('/var/www/album_art')

    for row in rows:
        album_id = str(row[0])
        album_name = str(row[1])
        album_fn = 'a_{}_120.jpg'.format(album_id)
        if not art_dir.joinpath(album_fn).exists():
            log(album_name)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import os
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

    conn_string = 'dbname=rainwave user=orpheus password={}'.format(rw_db_pass)
    conn = psycopg2.connect(conn_string)

    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        log('Please provide a search term.')
        sys.exit()

    with conn.cursor() as cur:
        sql = '''SELECT song_id, album_name, song_title, song_filename FROM
                 r4_songs JOIN r4_albums USING (album_id) WHERE song_title ILIKE
                 %s AND song_verified IS TRUE ORDER BY album_name, song_title'''
        cur.execute(sql, ['%{}%'.format(query)])
        rows = cur.fetchall()

    for row in rows:
        song_id = int(row[0])
        album_name = row[1]
        song_title = row[2]
        song_filename = row[3]
        m = '{} // {} // {} // {}'
        log(m.format(song_id, album_name, song_title, song_filename))

if __name__ == '__main__':
    main()

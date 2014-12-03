#!/usr/bin/env python3

import os
import psycopg2
import sys


def log(m):
    print(m)

if 'RW_DB_PASS' in os.environ:
    RW_DB_PASS = os.environ.get('RW_DB_PASS')
else:
    log('Please set the RW_DB_PASS environment variable.')
    sys.exit()

conn_string = 'dbname=rainwave user=orpheus password={}'.format(RW_DB_PASS)
conn = psycopg2.connect(conn_string)

if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    log('Please provide a search term.')
    sys.exit()

with conn.cursor() as cur:
    sql = ('select song_id, album_name, song_title, song_filename from '
           'r4_songs join r4_albums using (album_id) where song_title ilike '
           '%s order by album_name, song_title')
    cur.execute(sql, ['%{}%'.format(query)])
    rows = cur.fetchall()

for row in rows:
    song_id = int(row[0])
    album_name = row[1]
    song_title = row[2]
    song_filename = row[3]
    m = '{} // {} // {} // {}'
    log(m.format(song_id, album_name, song_title, song_filename))

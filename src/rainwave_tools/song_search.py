import argparse
import os
import psycopg2
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    return parser.parse_args()


def main():
    args = parse_args()

    if 'RW_DB_PASS' in os.environ:
        rw_db_pass = os.environ.get('RW_DB_PASS')
    else:
        print('Please set the RW_DB_PASS environment variable.')
        sys.exit()

    conn = psycopg2.connect(f'dbname=rainwave user=orpheus password={rw_db_pass}')

    with conn.cursor() as cur:
        sql = '''
            SELECT
                song_id,
                album_name,
                song_title,
                song_filename
            FROM r4_songs
            JOIN r4_albums USING (album_id)
            WHERE song_title ILIKE %s
            AND song_verified IS TRUE
            ORDER BY album_name, song_title
        '''
        cur.execute(sql, [f'%{args.query}%'])
        rows = cur.fetchall()

    for row in rows:
        song_id = int(row[0])
        album_name = row[1]
        song_title = row[2]
        song_filename = row[3]
        print(f'{song_id} // {album_name} // {song_title} // {song_filename}')


if __name__ == '__main__':
    main()

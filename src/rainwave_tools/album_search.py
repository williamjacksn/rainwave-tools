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
            select
                a.album_id,
                a.album_name,
                array_agg(distinct left(s.song_filename, 0 - position('/' in reverse(s.song_filename)))) album_folders
            from r4_songs s
            join r4_albums a on a.album_id  = s.album_id
            where s.song_verified is true
            and a.album_name ilike %s
            group by a.album_id, a.album_name
            order by a.album_name
        '''
        cur.execute(sql, [f'%{args.query}%'])
        rows = cur.fetchall()

    for row in rows:
        album_id = int(row[0])
        album_name = row[1]
        album_folders = sorted(row[2])
        print(f'{album_id} // {album_name}')
        for f in album_folders:
            print(f'  {f}')


if __name__ == '__main__':
    main()

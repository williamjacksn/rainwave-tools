import os
import pathlib
import psycopg2
import sys


def main():
    if 'RW_DB_PASS' in os.environ:
        rw_db_pass = os.environ.get('RW_DB_PASS')
    else:
        print('Please set the RW_DB_PASS environment variable.')
        sys.exit()

    cnx_string = f'dbname=rainwave user=orpheus password={rw_db_pass}'
    cnx = psycopg2.connect(cnx_string)

    sql = '''
        SELECT DISTINCT
            album_id,
            album_name
        FROM r4_songs
        JOIN r4_albums USING (album_id)
        WHERE song_verified IS TRUE
    '''
    with cnx.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    art_dir = pathlib.Path('/var/www/rainwave.cc/album_art')

    for row in rows:
        album_id = str(row[0])
        album_name = str(row[1])
        album_fn = f'a_{album_id}_120.jpg'
        if not art_dir.joinpath(album_fn).exists():
            print(album_name)


if __name__ == '__main__':
    main()

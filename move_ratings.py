#!/usr/bin/env python3

import os
import psycopg2
import sys


def log(m):
    print(m)


def usage():
    log('Usage: move_ratings <old_id> <new_id>')
    sys.exit()


def connect_db():
    if 'RW_DB_PASS' in os.environ:
        rw_db_pass = os.environ.get('RW_DB_PASS')
    else:
        log('Please set the RW_DB_PASS environment variable.')
        sys.exit()

    conn_string = 'dbname=rainwave user=orpheus password={}'.format(rw_db_pass)
    return psycopg2.connect(conn_string)


def main():
    if len(sys.argv) > 2:
        old_id, new_id = sys.argv[1:2]
    else:
        usage()

    if old_id.isdigit():
        old_id = int(old_id)
    else:
        usage()

    if new_id.isdigit():
        new_id = int(new_id)
    else:
        usage()

    conn = connect_db()

    with conn.cursor() as cur:
        log('** Moving ratings from {} to {} ...'.format(old_id, new_id))
        sql = 'update r4_song_ratings set song_id = %s where song_id = %s'
        cur.execute(sql, [new_id, old_id])
        m = '** Moved {} rating'.format(cur.rowcount)
        if cur.rowcount != 1:
            m = '{}s'.format(m)
        m = '{} from {} to {}.'.format(m, old_id, new_id)
        log(m)

        log('** Searching for duplicate ratings ...')
        sql = ('select user_id, song_id from r4_song_ratings group by user_id, '
               'song_id having count(song_id) > 1')
        cur.execute(sql)
        dup_rating_count = cur.rowcount
        found = '** Found {} duplicate rating'.format(dup_rating_count)
        deleted = '** Deleted {} duplicate rating'.format(dup_rating_count)
        if dup_rating_count != 1:
            found = '{}s'.format(found)
            deleted = '{}s'.format(deleted)
        found = '{}.'.format(found)
        deleted = '{}.'.format(deleted)
        log(found)

        rows = cur.fetchall()
        sql = ('delete from r4_song_ratings where ctid in (select min(ctid) '
               'from r4_song_ratings where user_id = %s and song_id = %s)')
        for row in rows:
            user_id = int(row[0])
            song_id = int(row[1])
            cur.execute(sql, [user_id, song_id])
        log(deleted)

if __name__ == '__main__':
    main()

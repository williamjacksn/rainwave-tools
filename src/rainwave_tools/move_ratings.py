import argparse
import os
import psycopg2
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('old_song_id')
    parser.add_argument('new_song_id')
    parser.add_argument('--live', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()

    rw_db_pass = os.getenv('RW_DB_PASS')
    if rw_db_pass is None:
        print('Please set the RW_DB_PASS environment variable.')
        sys.exit()

    cnx = psycopg2.connect(f'postgres://orpheus:{rw_db_pass}@localhost/rainwave')
    with cnx.cursor() as cur:
        # Look up album and title for old and new songs
        sql = '''
            SELECT album_name, song_title, song_filename
            FROM r4_songs
            JOIN r4_albums USING (album_id)
            WHERE song_id = %(song_id)s
        '''
        cur.execute(sql, {'song_id': args.old_song_id})
        old_song = cur.fetchone()
        print(f'Moving ratings from : {old_song[0]} / {old_song[1]}')
        cur.execute(sql, {'song_id': args.new_song_id})
        new_song = cur.fetchone()
        print(f'Moving ratings to   : {new_song[0]} / {new_song[1]}')

        # Get all ratings for old song
        sql = '''
            SELECT user_id, song_rating_user, song_rated_at
            FROM r4_song_ratings
            WHERE song_id = %(song_id)s
              AND song_rating_user IS NOT NULL
        '''
        cur.execute(sql, {'song_id': args.old_song_id})
        rows = cur.fetchall()
        print(f'Found {len(rows)} ratings for old song')

        moved_ratings = 0
        new_song_already_rated = 0
        for old_song_rating in rows:
            # See if this user has a rating for the new song
            sql = '''
                SELECT song_rating_user, song_rated_at
                FROM r4_song_ratings
                WHERE song_id = %(song_id)s
                  AND user_id = %(user_id)s
            '''
            cur.execute(sql, {'song_id': args.new_song_id, 'user_id': old_song_rating[0]})
            new_song_rating = cur.fetchone()

            if new_song_rating is None:
                # New song was never rated or faved
                sql = '''
                    UPDATE r4_song_ratings
                    SET song_id = %(new_song_id)s
                    WHERE song_id = %(old_song_id)s AND user_id = %(user_id)s
                '''
                params = {
                    'new_song_id': args.new_song_id,
                    'old_song_id': args.old_song_id,
                    'user_id': old_song_rating[0]
                }
                cur.execute(sql, params)
                moved_ratings += 1
            elif new_song_rating[0] is None:
                # New song was faved but not rated
                sql = '''
                    UPDATE r4_song_ratings
                    SET song_rating_user = %(song_rating_user)s, song_rated_at = %(song_rated_at)s
                    WHERE song_id = %(song_id)s AND user_id = %(user_id)s
                '''
                params = {
                    'song_rating_user': old_song_rating[1],
                    'song_rated_at': old_song_rating[2],
                    'song_id': args.new_song_id,
                    'user_id': old_song_rating[0]
                }
                cur.execute(sql, params)
                moved_ratings += 1
            else:
                # New song already has a rating
                new_song_already_rated += 1

    if args.live:
        cnx.commit()
    else:
        print('**')
        print('** No changes will be made in the database. Use --live to commit changes.')
        print('**')

    print(f'Users where rating for old song was applied to new song: {moved_ratings}')
    print(f'Users that already had a rating for the new song: {new_song_already_rated}')


if __name__ == '__main__':
    main()

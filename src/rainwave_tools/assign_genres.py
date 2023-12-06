import mutagen.id3
import os

GENRE_FILE = '_genre.txt'


def log(m):
    print(m)


def main():
    cwd = os.getcwd()
    log(f'{cwd} : current directory')

    for root, folders, files in os.walk(cwd):
        used_genre = ''
        has_mp3s = False
        for filename in files:
            if filename.endswith('.mp3'):
                has_mp3s = True
                if not used_genre:
                    mp3_path = os.path.join(root, filename)
                    tags = mutagen.id3.ID3(mp3_path)
                    genre_frames = tags.getall('TCON')
                    for frame in genre_frames:
                        used_genre = frame.text[0]
                        break
        if not has_mp3s:
            log(f'{root} : no mp3s')
            continue

        this_genre_file = os.path.join(root, GENRE_FILE)
        if GENRE_FILE in files:
            with open(this_genre_file) as f:
                genre = f.readline().strip()
                log(f'{this_genre_file} : {genre}')
            continue
        try:
            new_genre = input(f'{root} : set genre [{used_genre}] > ')
            if new_genre == '':
                continue
            with open(this_genre_file, 'w') as f:
                f.write(f'{new_genre}\n')
        except KeyboardInterrupt:
            print('')
            break


if __name__ == '__main__':
    main()

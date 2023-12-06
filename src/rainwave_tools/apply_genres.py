import mutagen.id3
import os

GENRE_FILE = '_genre.txt'


def log(m):
    print(m)


def main():
    cwd = os.getcwd()
    log(f'{cwd} : current directory')

    for root, folders, files in os.walk(cwd):
        for filename in files:
            if filename.endswith('.mp3'):
                break
        else:
            log(f'{root} : no mp3s')
            continue

        this_genre_file = os.path.join(root, GENRE_FILE)
        if GENRE_FILE in files:
            with open(this_genre_file) as f:
                genre = f.readline().strip()
                log(f'{this_genre_file} : {genre}')
        else:
            log(f'{this_genre_file} : not found')
            continue

        if genre == '':
            log(f'{this_genre_file} : empty, skipping this folder')
            continue

        for filename in files:
            if filename.endswith('.mp3'):
                mp3_path = os.path.join(root, filename)
                tags = mutagen.id3.ID3(mp3_path)
                cur_genre = ''
                for genre_tag in tags.getall('TCON'):
                    for genre_text in genre_tag.text:
                        cur_genre = genre_text
                    break
                if cur_genre == genre:
                    log(f'{mp3_path} already has genre {cur_genre}')
                    continue
                else:
                    tags.delall('TCON')
                    tags.add(mutagen.id3.TCON(encoding=3, text=[genre]))
                    tags.save()
                    log(f'{mp3_path} : setting genre to {genre}')


if __name__ == '__main__':
    main()

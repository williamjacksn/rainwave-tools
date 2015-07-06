Tools for maintaining a local library of music for [Rainwave][]

### Dealing with mp3 files and id3 tags

*   `add_genre`: add a genre to mp3 files, leaving existing genres in place
*   `apply_genres`: apply genres that are assigned using `assign_genres`
*   `assign_genres`: interactively assign genres to directories of mp3 files
*   `normalize_filenames`: automatically rename all files in a directory based
    on information in id3 tags
*   `rename_artist`: change an artist name in mp3 files, keeping multiple
    artists intact
*   `rename_genre`: change a genre in mp3 files, keeping multiple genres intact
*   `retag`: interactively edit title, album, and artist tags on all mp3 files
    in a directory
*   `rgwipe`: remove all replaygain tags from mp3 files
*   `rwtag`: view and manipulate id3 tags on mp3 files
*   `titles`: interactively update titles on all mp3 files in a directory

### Dealing with the database

*   `missing_art`: find albums that do not have album art
*   `move_ratings`: move ratings from one song to another
*   `song_search`: search the database for a song by title substring
*   `url_check`: check the validity of urls in the database

### Dealing with OCR

*   `ocremix.py`: Python module for parsing a remix info page on ocremix.org for
    metadata
*   `getocr`: download remixes from ocremix.org
*   `cleanocr`: update local files with metadata from ocremix.org
*   `ocra2ocr`: update local metadata when a song on an OCR album gets an
    official OCR release

[rainwave]: http://rainwave.cc/

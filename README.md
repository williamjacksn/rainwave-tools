Tools for maintaining a local library of music for [Rainwave][]

## Install

    pip install rainwave-tools

## Tools

### Dealing with mp3 files and id3 tags

*   `apply_genres`: apply genres that are assigned using `assign_genres`
*   `assign_genres`: interactively assign genres to directories of mp3 files
*   `cdg`: manage cooldown groups (genre tags) in mp3 files
*   `normalize_filenames`: automatically rename all files in a directory based on information in id3 tags
*   `rename_artist`: change an artist name in mp3 files, keeping multiple artists intact
*   `retag`: interactively edit title, album, and artist tags on all mp3 files in a directory
*   `rgwipe`: remove all replaygain tags from mp3 files
*   `rwtag`: view and manipulate id3 tags on mp3 files
*   `tit3_tit2`: Copy the contents of TIT3 to TIT2
*   `titles`: interactively update titles on all mp3 files in a directory

### Dealing with album art files

*   `delete_art`: delete generated album art files for a specific album

### Dealing with the database

*   `album_search`: search the database for an album by name substring
*   `missing_art`: find albums that do not have album art
*   `move_ratings`: move song ratings from one song to another (e.g. when removing duplicate songs)
*   `song_search`: search the database for a song by title substring
*   `url_check`: check the validity of urls in the database

### Dealing with OCR

*   `ocremix.py`: Python module for parsing a remix info page on ocremix.org for metadata
*   `getocr`: download remixes from ocremix.org
*   `cleanocr`: update local files with metadata from ocremix.org
*   `ocra2ocr`: update local metadata when a song on an OCR album gets an official OCR release

[rainwave]: https://rainwave.cc/

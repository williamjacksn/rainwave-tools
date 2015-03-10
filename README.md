Tools for maintaining a local library of music for [Rainwave][]

### General tag management

*   rwtag.py: view and manipulate ID3 tags on MP3 files

### Title management

*   titles.py: interactively update titles on all mp3 files in a directory
*   song_search.py: search the database for a song by title substring

### Artist management

*   rename_artist.py: change an artist name in mp3 files, keeping multiple
    artists intact

### Genre management

*   assign_genres.py: interactively assign genres to directories of mp3 files
*   apply_genres.py: apply genres that are assigned using assign_genres.py
*   rename_genre.py: change a genre in mp3 files, keeping multiple genres intact

### Art management

*   missing_art.py: find albums that do not have album art

### Replaygain management

*   rgwipe.py: remove all replaygain tags from mp3 files

### OCR management

*   ocremix.py: module for parsing a remix info page on ocremix.org for metadata
*   getocr.py: download remixes from ocremix.org
*   cleanocr.py: update local files with metadata from ocremix.org
*   ocra2ocr.py: update local metadata when a song on an OCR album gets an
    official OCR release

[rainwave]: http://rainwave.cc/

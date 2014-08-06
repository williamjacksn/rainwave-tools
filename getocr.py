import html
import subprocess
import sys
import urllib.request

def log(message):
    print(message)

REMIX_URL_TEMPLATE = 'http://ocremix.org/remix/OCR{:05}'

if len(sys.argv) > 1:
    cmd = sys.argv[1]
else:
    sys.exit('Please provide an OCR ID as the first argument.')

if cmd.isdigit():
    ocr_num = int(cmd)
else:
    sys.exit('{} is not an integer.'.format(cmd))

if ocr_num < 1 or ocr_num > 99999:
    sys.exit('{} is not between 1 and 99999'.format(ocr_num))

log('Processing OCR{:05} ...'.format(ocr_num))
url = REMIX_URL_TEMPLATE.format(ocr_num)
log('Attempting to read {} ...'.format(url))
try:
    ocr_data = urllib.request.urlopen(url)
except urllib.error.HTTPError as e:
    sys.exit(e)
ocr_page = ocr_data.read().decode()

_, _, ocr_page = ocr_page.partition('<h1>')
_, _, ocr_page = ocr_page.partition('href')
_, _, ocr_page = ocr_page.partition('">')
album, _, ocr_page = ocr_page.partition('</a>')
album = html.unescape(album)

title, _, ocr_page = ocr_page.partition('</h1>')
_, _, title = title.partition('\'')
title, _, _ = title.rpartition('\'')

_, _, ocr_page = ocr_page.partition('ReMixer(s)</strong>: ')
dirty_artists, _, ocr_page = ocr_page.partition('</li>')
dirty_artists = dirty_artists.split(',')
clean_artists = list()
for artist in dirty_artists:
    _, _, artist = artist.partition('">')
    artist, _, _ = artist.partition('<')
    clean_artists.append(artist)
artist = ', '.join(clean_artists)

_, host, ocr_page = ocr_page.partition('http://ocrmirror.org/')
path, ext, ocr_page = ocr_page.partition('.mp3')
url = '{}{}{}'.format(host, path, ext)

log('Downloading mp3 file from {} ...'.format(url))
temp_file, _ = urllib.request.urlretrieve(url)
log('Downloaded mp3 file to {}'.format(temp_file))

log(subprocess.check_output(['rwtag', 'set', 'album', album, temp_file]).encode())
log(subprocess.check_output(['rwtag', 'set', 'title', title, temp_file]).encode())
log(subprocess.check_output(['rwtag', 'set', 'artist', artist, temp_file]).encode())
log(subprocess.check_output(['rwtag', 'set', 'comment', 'Remix Info @ OCR', temp_file]).encode())

log('Cleaning up temporary files ...')
urllib.request.urlcleanup()

#log(ocr_page)

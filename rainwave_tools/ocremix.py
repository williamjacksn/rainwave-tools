import lxml.html
import rainwave_tools.utils
import urllib.request


class OCReMix(object):
    INFO_URL_TEMPLATE = 'http://ocremix.org/remix/OCR{:05}'

    def __init__(self, ocr_id):
        self.ocr_id = ocr_id
        self.info_url = self.INFO_URL_TEMPLATE.format(self.ocr_id)
        self._tree = None
        self._album = None
        self._safe_album = None
        self._title = None
        self._safe_title = None
        self._artist = None
        self._mp3_url = None
        self._has_lyrics = None

    def load_from_url(self):
        data = urllib.request.urlopen(self.info_url)
        page = data.read().decode()
        self._tree = lxml.html.fromstring(page)

    @property
    def album(self):
        if self._album is None:
            if self._tree is None:
                self.load_from_url()
            self._album = self._tree.xpath('//h1/a')[0].text
        return self._album

    @property
    def safe_album(self):
        if self._safe_album is None:
            self._safe_album = rainwave_tools.utils.make_safe(self.album)
        return self._safe_album

    @property
    def title(self):
        if self._title is None:
            if self._tree is None:
                self.load_from_url()
            self._title = self._tree.xpath('//h1/a')[0].tail[2:-2]
        return self._title

    @property
    def safe_title(self):
        if self._safe_title is None:
            self._safe_title = rainwave_tools.utils.make_safe(self.title)
        return self._safe_title

    @property
    def artist(self):
        if self._artist is None:
            if self._tree is None:
                self.load_from_url()
            artist_xpath = '//div[@id="panel-main"]/div/div/ul/li'
            art_tree = self._tree.xpath(artist_xpath)[2]
            self._artist = ', '.join([a.text for a in art_tree.xpath('a')])
        return self._artist

    @property
    def mp3_url(self):
        if self._mp3_url is None:
            if self._tree is None:
                self.load_from_url()
            mp3_url_xpath = '//div[@id="panel-download"]/div/ul/li/a/@href'
            self._mp3_url = self._tree.xpath(mp3_url_xpath)[2]
        return self._mp3_url

    @property
    def has_lyrics(self):
        if self._has_lyrics is None:
            if self._tree is None:
                self.load_from_url()
            lyrics_panel = self._tree.xpath('//div[@id="lyrics"]')
            self._has_lyrics = len(lyrics_panel) > 0
        return self._has_lyrics

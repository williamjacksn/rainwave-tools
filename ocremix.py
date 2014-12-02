import lxml.html
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
            self._safe_album = self.make_safe(self.album)
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
            self._safe_title = self.make_safe(self.title)
        return self._safe_title

    @property
    def artist(self):
        if self._artist is None:
            if self._tree is None:
                self.load_from_url()
            art_tree = self._tree.xpath('//div[@id="panel-main"]/div/ul/li')[1]
            self._artist = ', '.join([a.text for a in art_tree.xpath('a')])
        return self._artist

    @property
    def mp3_url(self):
        if self._mp3_url is None:
            if self._tree is None:
                self.load_from_url()
            mp3_url_xpath = '//div[@id="panel-download"]/ul/li/a/@href'
            self._mp3_url = self._tree.xpath(mp3_url_xpath)[3]
        return self._mp3_url

    @staticmethod
    def make_safe(s):
        unsafe = '!"#%\'()*+,-./:;<=>?@[\]^_`{|}~&あまごい '
        translate_table = {ord(char): None for char in unsafe}
        special = dict(zip(map(ord, 'äÉéêíñóöÜü'), 'aEeeinooUu'))
        translate_table.update(special)
        return s.translate(translate_table)

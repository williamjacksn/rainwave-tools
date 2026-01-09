import urllib.request

import lxml.html

from rainwave_tools import utils


class OCReMix:
    INFO_URL_TEMPLATE = "https://ocremix.org/remix/OCR{:05}"

    def __init__(self, ocr_id: int) -> None:
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
        self._tags = []

    def load_from_url(self) -> None:
        data = urllib.request.urlopen(self.info_url)  # noqa: S310
        page = data.read().decode()
        self._tree = lxml.html.fromstring(page)

    @property
    def album(self) -> str:
        if self._album is None:
            if self._tree is None:
                self.load_from_url()
            self._album = self._tree.xpath("//h1/a")[0].text
        return self._album

    @property
    def safe_album(self) -> str:
        if self._safe_album is None:
            self._safe_album = utils.make_safe(self.album)
        return self._safe_album

    @property
    def title(self) -> str:
        if self._title is None:
            if self._tree is None:
                self.load_from_url()
            self._title = self._tree.xpath("//h1/a")[0].tail[2:-2]
        self._title = self._title.replace("\ufeff", "")
        return self._title

    @property
    def safe_title(self) -> str:
        if self._safe_title is None:
            self._safe_title = utils.make_safe(self.title)
        return self._safe_title

    @property
    def artist(self) -> str:
        if self._artist is None:
            if self._tree is None:
                self.load_from_url()
            self._artist = ", ".join(
                [
                    a.text.replace("\ufeff", "")
                    for a in self._tree.xpath('//h2/a[starts-with(@href, "/artist")]')
                ]
            )
        return self._artist

    @property
    def mp3_url(self) -> str:
        if self._mp3_url is None:
            if self._tree is None:
                self.load_from_url()
            _xpath = (
                '//div[@id="modalDownload"]//a[contains(@href, "ocrmirror.org")]/@href'
            )
            self._mp3_url = self._tree.xpath(_xpath)[0]
        return self._mp3_url

    @property
    def has_lyrics(self) -> bool:
        if self._has_lyrics is None:
            if self._tree is None:
                self.load_from_url()
            self._has_lyrics = bool(self._tree.xpath('//a[@href="#tab-lyrics"]'))
        return self._has_lyrics

    @property
    def tags(self) -> list[str]:
        if not self._tags:
            xpath = (
                '//*[@id="main-content"]/div[1]/div/div[1]/section[1]/div/div'
                "/section[2]/div[2]/section[3]/div/span"
            )
            for t in self._tree.xpath(xpath):
                self._tags.append(t.text)
            self._tags.sort()
        return self._tags

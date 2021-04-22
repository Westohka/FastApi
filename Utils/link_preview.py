# Class for grab information about url

import httpx
from bs4 import BeautifulSoup


class LinkPreview(object):
    def __init__(self,
                 url: str,
                 timeout: int = 20):
        self.url = url
        self.timeout = timeout

        self._data = None

    # Get content and parse data from url

    async def requestPreview(self):
        del self._data

        self._data = None

        async with httpx.AsyncClient() as client:
            data = await client.get(self.url, timeout=self.timeout)
            self._data = BeautifulSoup(data)

    # Title url

    @property
    def title(self) -> str:
        meta = self._data.find("meta", property="og:title")

        if meta and meta["content"]:
            return meta["content"]

        meta = self._data.find("meta", property="twitter:title")

        if meta and meta["content"]:
            return meta["content"]

        if self._data.title and self._data.title.text:
            return self._data.title.text

        return ""

    # Description url

    @property
    def description(self) -> str:
        meta = self._data.find("meta", property="og:description")

        if meta and meta["content"]:
            return meta["content"]

        meta = self._data.find("meta", property="twitter:description")

        if meta and meta["content"]:
            return meta["content"]

        meta = self._data.find("meta", property="description")

        if meta and meta.has_attr('content'):
            return meta["content"]

        return ""

    # Image url

    @property
    def image(self) -> str:
        meta = self._data.find("meta", property="og:image")

        if meta and meta["content"]:
            return meta["content"]

        meta = self._data.find("meta", property="twitter:image")

        if meta and meta["content"]:
            return meta["content"]

        return ""

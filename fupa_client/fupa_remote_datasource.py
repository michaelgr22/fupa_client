import requests as _requests
from bs4 import BeautifulSoup as _BeautifulSoup


class FupaRemoteDatasource:

    def __init__(self, url):
        self.url = url

    def scrap_page(self):
        result = _requests.get(self.url)
        if(result.status_code != 200):
            return False
        html = result.content
        soup = _BeautifulSoup(html, 'lxml')

        return soup

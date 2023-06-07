import dataclasses
import typing
import urllib.parse as urlparse

import bs4
import requests

from src.scraping.scrape_error import ScrapeError


@dataclasses.dataclass
class InputInfo:
    method: str
    type: str
    name: str
    value: str


class FormSpider:
    def __init__(self, url):
        url_parsed = urlparse.urlparse(url)
        self.__domain = url_parsed.netloc
        if url_parsed.scheme in ('http', 'https') and url_parsed.netloc:
            self.url = url
        else:
            raise ScrapeError('URL is not valid')
        self.__form_info = None

    def form_info(self) -> typing.List[InputInfo]:
        if self.__form_info:
            return self.__form_info
        try:
            html_text = self.__get_content()
            self.__get_info(html_text)
        except ScrapeError:
            print(f'Warning: URL "{self.url}" is not valid')
        return self.__form_info

    def __get_content(self) -> str:
        try:
            req = requests.get(self.url, timeout=(3, 7), headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0', })
        except requests.exceptions.RequestException:
            raise ScrapeError(f'Invalid URL: "{self.url}"') from None
        if req.status_code != requests.codes.ok:
            raise ScrapeError('URL is not valid') from None
        return req.text

    def __get_info(self, html: str) -> None:
        soup = bs4.BeautifulSoup(html, 'lxml')
        self.__form_info = list()
        for form_tag in soup.find_all('form'):
            method = 'get'
            if form_tag.has_attr('method'):
                method = form_tag['method'].lower()
            for input_tag in form_tag.find_all('input'):
                input_type = None
                if input_tag.has_attr('type'):
                    input_type = input_tag['type']
                input_name = None
                if input_tag.has_attr('name'):
                    input_name = input_tag['name']
                input_value = None
                if input_tag.has_attr('value'):
                    input_value = input_tag['value']
                self.__form_info.append(InputInfo(method, input_type, input_name, input_value))


URL_TEST = 'https://candidatura.42malaga.com/users/sign_up'

if __name__ == '__main__':
    spider = FormSpider(URL_TEST)
    info = spider.form_info()
    print(info)

import dataclasses
import typing
import urllib.parse as urlparse

import bs4
import requests

from src.scraping.scrape_error import ScrapeError


@dataclasses.dataclass
class InputInfo:
    type: str
    id: str
    name: str
    value: str


@dataclasses.dataclass
class FormInfo:
    method: str
    action: str
    inputs: typing.List[InputInfo]


class FormSpider:
    def __init__(self, url):
        url_parsed = urlparse.urlparse(url)
        self.__domain = url_parsed.netloc
        if url_parsed.scheme in ('http', 'https') and url_parsed.netloc:
            self.url = url
        else:
            raise ScrapeError('URL is not valid')
        self.__forms: typing.Optional[typing.List[FormInfo]] = None

    def form_info(self) -> typing.List[FormInfo]:
        if self.__forms is not None:
            return self.__forms
        try:
            html_text = self.__get_content()
            self.__get_info(html_text)
        except ScrapeError:
            print(f'Warning: URL "{self.url}" is not valid')
        return self.__forms

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
        self.__forms = list()
        for form_tag in soup.find_all('form'):
            method = form_tag.get('method').lower()
            action = urlparse.urljoin(self.url, form_tag.get('action'))

            form = FormInfo(method, action, list())
            for input_tag in form_tag.find_all('input'):
                input_type = input_tag.get('type')
                input_id = input_tag.get('id')
                input_name = input_tag.get('name')
                input_value = input_tag.get('value')
                form.inputs.append(InputInfo(input_type, input_id, input_name, input_value))
            self.__forms.append(form)

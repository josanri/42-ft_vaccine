from src.scraping.form_spider import FormSpider
from src.sql_injection_builder import SQLInjectionBuilder
from src.scraping.form_spider import COMMON_GET_INPUTS
from src.injector_state.sql_injector_database_engine_state import SQLInjectorDatabaseEngineState

import requests
import urllib.parse
import logging

class SQLInjector:
    supported_methods = ("get", "post")
    def __init__(self, url, output_file ="results.txt", method = "get") -> None:
        if method in SQLInjector.supported_methods:
            logging.basicConfig(filename=output_file, format='%(message)s')
            self.url = url
            self.state = SQLInjectorDatabaseEngineState(self)
            self.method = method
            self.forms = [form for form in FormSpider(url).form_info() if form.method == method]
        else:
            raise NotImplementedError(f"{method} method is not supported")

    def inject(self):
        print(self.forms)
        if self.method == "post" and len(self.forms) == 0:
            raise Exception("Could not find any form to inject data")

        if self.method == "get":
            for inputs in COMMON_GET_INPUTS:
                self.try_inject(self.url, inputs)
        for form in self.forms:
            self.try_inject(form.action, form.inputs)

    def try_inject(self, action, inputs):
        default_values = {None: "a",
                          "text": "random text",
                          "email": "valid@gmail.com",
                          "number": 5}
        
        for input_chosen in inputs:
            data = {}
            data[input_chosen.name] = "Try sql injection here"
            for input in inputs:
                if input != input_chosen:
                    if input.value != None:
                        dummy_value = input.value
                    else:
                        dummy_value = default_values.get(input.type, None)
                    data[input.name] = dummy_value
            response = self.http_request_inject(action, data)
            if 200 <= response.status_code <= 300:
                print(f"{response.status_code} - Valid injection with: {data}")
            else:
                print(f"{response.status_code} - Could not resolve injection with {data}")
            
    def http_request_inject(self, url, data = None):
        if self.method == "get":
            if data == None:
                response = requests.get(url)
            else:
                response = requests.get(f"{url}?{urllib.parse.urlencode(data)}")
        elif self.method == "post":
            response = requests.post(url, data=data)
        return response

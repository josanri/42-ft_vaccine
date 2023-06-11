from src.scraping.form_spider import FormSpider
from src.sql_injection_builder import SQLInjectionBuilder
class SQLInjector:
    supported_methods = ("get", "post")
    def __init__(self, url, output_file ="results.txt", method = "get") -> None:
        if method in SQLInjector.supported_methods:
            self.url = url
            self.output_file = output_file
            self.method = method
            self.forms = FormSpider(url).form_info()
        else:
            raise NotImplementedError(f"{method} method is not supported")

    def inject():
        pass

    def _try_error(self):
        for form in self.forms:
            if form.method == self.method:
                pass

    def _retrieve_data():
        pass
class SQLInjector:
    def __init__(self, output_file ="results.txt", method = "GET") -> None:
        self.output_file = output_file
        self.method = method
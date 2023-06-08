class SQLInjector:
    def __init__(self, output_file ="results.txt", method = "get") -> None:
        self.output_file = output_file
        self.method = method
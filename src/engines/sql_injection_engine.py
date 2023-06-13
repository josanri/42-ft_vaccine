from abc import ABC


class SQLInjectionEngine(ABC):
    injection_prefix = "z#-+"
    injection_suffix = "+-#z"

    def __init__(self) -> None:
        pass

    def database_names(self) -> str:
        pass

    def version(self) -> str:
        pass

    def schema(self, columns) -> str:
        pass

    def tables(self, columns, schema_name) -> str:
        pass

    def column_names(self, table_name=None):
        pass

    def query(self, columns, schema_name, table, column_name) -> str:
        pass

    @staticmethod
    def dump_table(table: str):
        return f"select * from {table}"

    @staticmethod
    def identify() -> str:
        pass

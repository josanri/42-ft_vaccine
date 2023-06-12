from abc import ABC

class SQLInjectionEngine(ABC):
    injection_prefix = "z#-+"
    injection_suffix = "+-#z"
    
    def __init__(self) -> None:
        pass

    def database_names(self) -> str:
        pass

    def version(self)  -> str:
        pass

    def tables(self) -> str:
        pass

    def column_names(self, table_name = None):
        pass

    def dump_table(self, table:str):
        return f"select * from {table}"
    
    def identify() -> str:
        pass
from sql_injection_engine import SQLInjectionEngine

class MySQLInjection(SQLInjectionEngine):
    def __init__(self) -> None:
        super().__init__()

    def database_names(self) -> str:
        return "SHOW DATABASES;"

    def version(self)  -> str:
        return "SHOW VARIABLES LIKE 'version';"

    def tables(self) -> str:
        return "SELECT table_name FROM information_schema.tables;"

    def column_names(self, table_name = None):
        if table_name == None:
            return "SHOW `columns` FROM *;"
        else:
            return f"SHOW `columns` FROM `{table_name}`;"

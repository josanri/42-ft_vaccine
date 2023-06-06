from sql_injection_engine import SQLInjectionEngine

class MySQLInjection(SQLInjectionEngine):
    def __init__(self) -> None:
        super().__init__()

    def database_names() -> str:
        return "SHOW DATABASES;"

    def version()  -> str:
        return "SHOW VARIABLES LIKE 'version';"

    def tables() -> str:
        return "SELECT table_name FROM information_schema.tables;"

    def column_names(table_name = None):
        if table_name == None:
            return "SHOW `columns` FROM *;"
        else:
            return f"SHOW `columns` FROM `{table_name}`;"

from sql_injection_engine import SQLInjectionEngine

class PostgreSQL(SQLInjectionEngine):
    def __init__(self) -> None:
        super().__init__()

    def database_names() -> str:
        return "SELECT datname FROM pg_catalog.pg_database;"
    
    def version():
        return "SELECT version();"

    def tables() -> str:
        return "SELECT table_name FROM information_schema.tables;"
    
    def column_names(table_name = None):
        if table_name == None:
            return f"SELECT * FROM information_schema.columns"
        else:
            return f"SELECT * FROM information_schema.columns WHERE table_name = '{table_name}'"
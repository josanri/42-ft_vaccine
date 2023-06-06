class SQLInjections:
    class SQLInjectionEngine:
        def __init__(self) -> None:
            pass

    class SQLInjectionBuilder:
        def __init__(self, engine: SQLInjectionEngine) -> None:
            self.engine = engine

        def union_injection(self):
            return f"\"{self.engine};--"

    class OracleInjection(SQLInjectionEngine):
        def version():
            return "SELECT VERSION, VERSION_FULL FROM V$INSTANCE;"

    class PostgreSQL:
        def version():
            return "SELECT version();"

    class MySQLInjection:
            def database_names() -> str:
                return "SHOW DATABASES;"
            
            def version()  -> str:
                return "SHOW VARIABLES LIKE 'version';"
            
            def tables() -> str:
                return "SELECT table_name FROM information_schema.tables;"
            
            def column_names(str = None):
                if str == None:
                    "SHOW `columns` FROM *;"
                else:
                    return f"SHOW `columns` FROM `{str}`;"

            def dump_table(table:str):
                return f"select * from {table}"

if __name__ == "__main__":
    pass
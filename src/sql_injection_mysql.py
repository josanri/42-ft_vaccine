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
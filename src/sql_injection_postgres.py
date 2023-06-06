from sql_injection_engine import SQLInjectionEngine

class PostgreSQL(SQLInjectionEngine):
    def version():
        return "SELECT version();"

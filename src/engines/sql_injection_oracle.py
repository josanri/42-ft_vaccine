from sql_injection_engine import SQLInjectionEngine

class OracleInjection(SQLInjectionEngine):
    def version():
        return "SELECT VERSION, VERSION_FULL FROM V$INSTANCE;"
    
    # TODO: Bonus for the project
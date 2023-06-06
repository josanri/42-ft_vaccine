class OracleInjection(SQLInjectionEngine):
        def version():
            return "SELECT VERSION, VERSION_FULL FROM V$INSTANCE;"
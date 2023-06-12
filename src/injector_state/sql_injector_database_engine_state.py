from src.injector_state.sql_injector_state import SQLInjectorState
from src.injector_state.sql_injector_version_state import SQLInjectorGetVersionState

from src.engines.sql_injection_mysql import SQLInjectionEngineMySQL
from src.engines.sql_injection_postgres import SQLInjectionEnginePostgreSQL

class SQLInjectorDatabaseEngineState(SQLInjectorState):
    def __init__(self) -> None:
        super().__init__()

    def next(self):
        if True:
            self.sql_injector.state = SQLInjectorGetVersionState(SQLInjectionEngineMySQL())
        else:
            self.sql_injector.state = SQLInjectorGetVersionState(SQLInjectionEnginePostgreSQL())
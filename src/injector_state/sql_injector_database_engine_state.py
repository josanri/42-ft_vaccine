from src.injector_state.sql_injector_state import SQLInjectorState
from src.injector_state.sql_injector_version_state import SQLInjectorGetVersionState

from src.engines.sql_injection_mysql import SQLInjectionEngineMySQL
from src.engines.sql_injection_postgres import SQLInjectionEnginePostgreSQL

class SQLInjectorDatabaseEngineState(SQLInjectorState):
    def __init__(self, sql_injector) -> None:
        super().__init__(sql_injector)

    def next(self):
        if self.engine == "mysql":
            self.sql_injector.state = SQLInjectorGetVersionState(SQLInjectionEngineMySQL())
        elif self.engine == "postgres":
            self.sql_injector.state = SQLInjectorGetVersionState(SQLInjectionEnginePostgreSQL())
    
    def inject(self, action, input_chosen, inputs):
        success = super().injection(action, input_chosen, inputs, "sql_injection_string")
        if success != None:
            self.engine = success
            self.next()
            self.sql_injector.state.inject(action, input_chosen, inputs)
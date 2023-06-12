from src.injector_state.sql_injector_state import SQLInjectorState
from src.injector_state.sql_injector_dump_state import SQLInjectorDumpState

class SQLInjectorGetDatabaseNames(SQLInjectorState):
    def __init__(self, sql_injector) -> None:
        super().__init__(sql_injector)

    def next(self):
        self.sql_injector.state = SQLInjectorDumpState()
        return self.sql_injector.state

    def inject(self, action, input_chosen, inputs):
        databases = super().injection(action, input_chosen, inputs, "sql_injection_string")
        if databases != None:
            self.engine = databases
            self.next().inject(action, input_chosen, inputs)
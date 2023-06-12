from src.injector_state.sql_injector_dump_state import SQLInjectorDumpState
from src.injector_state.sql_injector_state import SQLInjectorState


class SQLInjectorGetDatabaseNames(SQLInjectorState):
    def __init__(self, sql_injector) -> None:
        super().__init__(sql_injector)
        self.databases = None

    def next(self):
        self.sql_injector.state = SQLInjectorDumpState()
        return self.sql_injector.state

    def inject(self, action, input_chosen, inputs):
        databases = super().injection(action, input_chosen, inputs, "sql_injection_string")
        if databases is not None:
            self.databases = databases
            self.next().inject(action, input_chosen, inputs)

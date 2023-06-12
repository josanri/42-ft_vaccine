from src.injector_state.sql_injector_state import SQLInjectorState
from src.injector_state.sql_injector_dump_state import SQLInjectorDumpState

class SQLInjectorGetVersionState(SQLInjectorState):
    def __init__(self, sql_injector) -> None:
        super().__init__(sql_injector)

    def next(self):
        self.sql_injector.state = SQLInjectorDumpState()
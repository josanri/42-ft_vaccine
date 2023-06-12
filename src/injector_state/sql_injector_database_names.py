from src.injector_state.sql_injector_dump_state import SQLInjectorDumpState
from src.injector_state.sql_injector_state import SQLInjectorState
from src.engines.sql_injection_engine import SQLInjectionEngine

class SQLInjectorGetDatabaseNames(SQLInjectorState):
    def __init__(self, sql_injector, engine) -> None:
        super().__init__(sql_injector)
        self.engine = engine
        self.databases = None

    def next(self):
        self.sql_injector.state = SQLInjectorDumpState()
        return self.sql_injector.state

    def inject(self, action, input_chosen, inputs):
        # TODO
        pass

    def get_version_engine(self, action, input_chosen, inputs, previous_str):
        number_of_columns = super().get_number_of_columns(action, input_chosen, inputs, previous_str)
        if number_of_columns is None:
            return None
        else:
            # TODO
            pass
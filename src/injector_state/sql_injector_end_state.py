from src.injector_state.sql_injector_state import SQLInjectorState

class SQLInjectorEndState(SQLInjectorState):
    def __init__(self, sql_injector) -> None:
        super().__init__(sql_injector)

    def next(self):
        raise NotImplementedError("No more states")
    
    def inject(self, action, input_chosen, inputs):
        raise NotImplementedError("Injection cannot be done on final state")

    def end(self):
        return True
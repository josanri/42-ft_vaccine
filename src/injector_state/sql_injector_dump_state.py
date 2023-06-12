from src.injector_state.sql_injector_state import SQLInjectorState

import logging

class SQLInjectorDumpState(SQLInjectorState):
    def __init__(self, sql_injector) -> None:
        super().__init__(sql_injector)

    def next(self):
        return None
    
    def inject(self, action, input_chosen, inputs):
        databases = super().injection(action, input_chosen, inputs, "sql_injection_string")
        if databases != None:
            logging.info("Database Dump:")
            logging.info(databases)
            self.next()
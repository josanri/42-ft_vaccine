class SQLInjectionBuilder:
    def __init__(self, engine) -> None:
        self.engine = engine

    def admin() -> None:
        return f"\' or 1=\"1\";--"

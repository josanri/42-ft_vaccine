from abc import ABC
import logging

class SQLInjectorState(ABC):
    def __init__(self, sql_injector) -> None:
        self.sql_injector = sql_injector
    
    def next(self):
        pass
from abc import ABC
from abc import abstractmethod


class Initialize(ABC):

    @abstractmethod
    def initialize_platform(self):
        ...

    @abstractmethod
    def initialize_symbol(self, *symbols: str):
        ...


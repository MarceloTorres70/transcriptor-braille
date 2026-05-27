from abc import ABC, abstractmethod


class BrailleDictionaryPort(ABC):
    @abstractmethod
    def get_symbol_for_text(self, token: str):
        pass

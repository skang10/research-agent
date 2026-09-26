from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self, content: bytes) -> str:
        pass


class VanillaParser(Parser):
    def parse(self, content: bytes) -> str:
        return content.decode("utf-8")


class LlamaIndexParser(Parser):
    def parse(self, content: bytes) -> str:
        raise NotImplementedError("LlamaIndexParser is not implemented yet.")

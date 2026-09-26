from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self, content: bytes) -> str:
        pass


class VanillaParser(Parser):
    def parse(self, content: bytes, content_type: str) -> str:
        if content_type == "text/plain":
            return content.decode("utf-8")
        else:
            raise ValueError(f"Unsupported content type: {content_type}")


class LlamaIndexParser(Parser):
    def parse(self, content: bytes) -> str:
        raise NotImplementedError("LlamaIndexParser is not implemented yet.")

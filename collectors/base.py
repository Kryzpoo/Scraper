from abc import ABC


class BaseCollector(ABC):

    def collect(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

from abc import ABC
from typing import Tuple, List


class BaseWriter(ABC):

    def write_many(self, data_set: List[Tuple[str, str, dict, list]]) -> None:
        pass

    def stop(self) -> None:
        pass

    def start(self) -> None:
        pass

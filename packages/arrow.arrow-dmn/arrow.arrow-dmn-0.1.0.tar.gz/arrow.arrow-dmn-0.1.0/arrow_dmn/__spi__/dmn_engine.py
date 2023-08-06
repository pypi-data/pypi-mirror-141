from abc import abstractmethod, ABC
from pathlib import Path
from typing import Union

from arrow_dmn.__spi__.process_ref import ProcessRef

BusinessRuleSource = Union[Path]


class DmnEngine(ABC):

    @abstractmethod
    def deploy(self, source: BusinessRuleSource) -> ProcessRef:
        pass

    @abstractmethod
    def execute(self, process_ref: ProcessRef, attributes: dict) -> dict:
        pass

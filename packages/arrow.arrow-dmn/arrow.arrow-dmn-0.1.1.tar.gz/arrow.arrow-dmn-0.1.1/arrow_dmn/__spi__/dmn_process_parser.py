from abc import ABC, abstractmethod
from pathlib import Path

from arrow_dmn.model.dmn_process import DmnProcess

DiagramSource = Path


class DmnProcessParser(ABC):

    @abstractmethod
    def parse(self, source: DiagramSource) -> DmnProcess:
        pass

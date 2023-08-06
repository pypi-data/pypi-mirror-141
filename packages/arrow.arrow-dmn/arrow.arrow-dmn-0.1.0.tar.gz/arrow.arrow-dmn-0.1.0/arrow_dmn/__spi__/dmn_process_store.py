from abc import ABC, abstractmethod

from arrow_dmn.__spi__.process_ref import ProcessRef
from arrow_dmn.model.dmn_process import DmnProcess


class DmnProcessStore(ABC):

    @abstractmethod
    def store_dmn_process(self, business_rules: DmnProcess):
        pass

    @abstractmethod
    def get_dmn_process(self, process_ref: ProcessRef):
        pass

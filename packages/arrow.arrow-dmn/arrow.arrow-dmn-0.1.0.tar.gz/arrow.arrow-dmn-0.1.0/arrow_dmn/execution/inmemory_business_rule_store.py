from typing import Dict

from arrow_dmn.__spi__.dmn_process_store import DmnProcessStore
from arrow_dmn.__spi__.process_ref import ProcessRef
from arrow_dmn.model.dmn_process import DmnProcess


class InMemoryDmnProcessStore(DmnProcessStore):

    def __init__(self):
        self.processes: Dict[str, DmnProcess] = {}

    def store_dmn_process(self, process: DmnProcess):
        self.processes[process.group + ":" + process.process_id] = process

    def get_dmn_process(self, process_ref: ProcessRef):
        return self.processes[str(process_ref)]

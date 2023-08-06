from dataclasses import dataclass
from typing import List

from arrow_dmn.model.dmn_decision import DmnDecision


@dataclass
class DmnProcess:
    group: str
    process_id: str
    decisions: List[DmnDecision]

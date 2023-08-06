from dataclasses import dataclass
from typing import List

from arrow_dmn.model.dmn_rule import DmnRule
from arrow_dmn.model.dmn_value import DmnValue
from arrow_dmn.model.hit_policy import HitPolicy


@dataclass
class DmnDecision:
    id: str
    required: List[str]
    inputs: List[DmnValue]
    outputs: List[DmnValue]
    rules: List[DmnRule]
    hit_policy: HitPolicy

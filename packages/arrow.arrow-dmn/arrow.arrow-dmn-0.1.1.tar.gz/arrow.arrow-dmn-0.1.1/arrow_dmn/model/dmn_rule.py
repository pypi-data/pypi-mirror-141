from dataclasses import dataclass
from typing import List


@dataclass
class DmnRule:
    inputs: List[str]
    outputs: List[str]

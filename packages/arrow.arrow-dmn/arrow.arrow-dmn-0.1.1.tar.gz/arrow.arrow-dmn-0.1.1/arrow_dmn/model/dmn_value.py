from dataclasses import dataclass


@dataclass
class DmnValue:
    name: str
    type: str

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

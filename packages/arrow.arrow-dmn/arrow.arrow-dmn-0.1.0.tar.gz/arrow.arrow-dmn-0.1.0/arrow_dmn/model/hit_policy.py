from enum import Enum


class HitPolicy(Enum):
    UNIQUE = "UNIQUE"
    ANY = "ANY"
    FIRST = "FIRST"
    RULE_ORDER = "RULE ORDER"
    COLLECT = "COLLECT"
    COLLECT_SUM = "SUM"
    COLLECT_MIN = "MIN"
    COLLECT_MAX = "MAX"
    COLLECT_COUNT = "COUNT"

from typing import List, Union, Any, Dict

from arrow_dmn.__spi__.dmn_engine import DmnEngine, BusinessRuleSource
from arrow_dmn.__spi__.dmn_process_store import DmnProcessStore
from arrow_dmn.__spi__.process_ref import ProcessRef
from arrow_dmn.execution.inmemory_business_rule_store import InMemoryDmnProcessStore
from arrow_dmn.model import HitPolicy
from arrow_dmn.model.dmn_decision import DmnDecision
from arrow_dmn.parser import XmlDmnProcessParser


def is_conjunct(obj1: Union[list, dict], obj2: Union[list, dict]) -> bool:
    if len(obj1) == 0:
        return True

    obj1 = list(map(str, obj1)) if isinstance(obj1, list) else obj1
    obj2 = list(map(str, obj2)) if isinstance(obj2, list) else obj2

    obj1 = obj1 if isinstance(obj1, list) else obj1.keys()
    obj2 = obj2 if isinstance(obj2, list) else obj2.keys()
    return set(obj1) <= set(obj2)


def to_numeric(text: str):
    text = text.strip()
    if text.isnumeric():
        return int(text)
    raise ValueError(f"cannot convert {text} to number")


def collect(results: List[Dict[str, Any]]):
    output = {}
    for result in results:
        k = next(list(result.keys()))
        v = result[k]
        if k not in output:
            output[k] = [v]
        else:
            output[k] += [v]
    return output


def cast(v, t):
    if t == "integer":
        return int(v)
    if t == "string":
        return v
    raise ValueError(f"cannot handle type {t}")


class SyncDmnEngine(DmnEngine):
    parser: XmlDmnProcessParser = XmlDmnProcessParser()
    store: DmnProcessStore = InMemoryDmnProcessStore()

    def deploy(self, source: BusinessRuleSource) -> ProcessRef:
        process = self.parser.parse(source)
        self.store.store_dmn_process(process)
        return ProcessRef(process.group, process.process_id)

    def execute(self, process_ref: ProcessRef, attributes: dict) -> dict:
        process = self.store.get_dmn_process(process_ref)
        return self._execute_decisions(process.decisions, [], attributes)

    def _execute_decisions(self, decisions: List[DmnDecision], invoked: List[str], attributes: dict) -> dict:
        if len(decisions) == 0:
            return attributes

        invoked = invoked
        delayed = []

        for decision in decisions:
            if not is_conjunct(decision.required, invoked):
                delayed += [decision]

            elif is_conjunct(decision.inputs, attributes):
                invoked += [decision.id]
                attributes = self._execute_decision(decision, attributes)

            else:
                delayed += [decision]

        assert len(decisions) > len(delayed), "invalid dmn process"
        return self._execute_decisions(delayed, invoked, attributes)

    def _execute_decision(self, decision: DmnDecision, attributes: dict) -> dict:
        _inputs = [attributes[input.name] for input in decision.inputs]
        _outputs_names = [output.name for output in decision.outputs]
        _output_types = [output.type for output in decision.outputs]

        updates = []

        for rule in decision.rules:
            assert len(_inputs) == len(rule.inputs), "input mismatch"
            assert len(_outputs_names) == len(rule.outputs), "input mismatch"

            result = True
            for i in range(len(_inputs)):
                result = result and self._evaluate_input_rule(_inputs[i], rule.inputs[i].strip())
            if result:
                updates.append({k: cast(v, t) for k, v, t in zip(_outputs_names, rule.outputs, _output_types)})

        if decision.hit_policy is HitPolicy.UNIQUE:
            assert len(updates) == 1, "hit policy UNIQUE not fulfilled"
            attributes.update(updates[0])
        if decision.hit_policy == HitPolicy.ANY:
            assert len(set(updates)) == 1, "hit policy ANY not fulfilled"
            attributes.update(updates[0])
        if decision.hit_policy == HitPolicy.FIRST:
            assert len(set(updates)) == 1, "hit policy FIRST not fulfilled"
            attributes.update(updates[0])
        if decision.hit_policy == HitPolicy.RULE_ORDER:
            [attributes.update(update) for update in updates]
        if decision.hit_policy == HitPolicy.COLLECT:
            update = collect(updates)
            print()

        return attributes

    def _evaluate_input_rule(self, x: Any, rule: str) -> bool:
        if rule.startswith(">="):
            return x >= to_numeric(rule[2:])
        elif rule.startswith(">"):
            return x > to_numeric(rule[1:])
        elif rule.startswith("<="):
            return x <= to_numeric(rule[2:])
        elif rule.startswith("<"):
            return x < to_numeric(rule[1:])
        elif rule.startswith("[") and rule.endswith("]"):
            numbers = list(map(to_numeric, rule[1:-1].split("..")))
            if numbers[0] <= x <= numbers[1]:
                return True
        elif rule.startswith("]") and rule.endswith("]"):
            numbers = list(map(to_numeric, rule[1:-1].split("..")))
            if numbers[0] < x <= numbers[1]:
                return True
        elif rule.startswith("[") and rule.endswith("["):
            numbers = list(map(to_numeric, rule[1:-1].split("..")))
            if numbers[0] <= x < numbers[1]:
                return True
        elif rule.startswith("]") and rule.endswith("["):
            numbers = list(map(to_numeric, rule[1:-1].split("..")))
            if numbers[0] < x < numbers[1]:
                return True
        elif rule.startswith("\"") and rule.endswith("\""):
            return x == rule or x == rule[1:-1]
        else:
            raise ValueError(f"invalid rule {rule}")

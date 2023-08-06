import xml.etree.ElementTree as XmlTree
from pathlib import Path
from typing import List

from arrow_dmn.__spi__.dmn_process_parser import DmnProcessParser
from arrow_dmn.model import DmnValue
from arrow_dmn.model import HitPolicy
from arrow_dmn.model.dmn_decision import DmnDecision
from arrow_dmn.model.dmn_process import DmnProcess
from arrow_dmn.model.dmn_rule import DmnRule
from arrow_dmn.parser.xml_element import XMLElement

DiagramSource = Path


class XmlDmnProcessParser(DmnProcessParser):

    def parse(self, source: DiagramSource) -> DmnProcess:
        root = XMLElement(XmlTree.parse(source).getroot())
        decisions = [self._parse_decision(element) for element in root.get_tags("dmn:decision")]
        group = root.get_attribute("arrow:group")

        return DmnProcess(group, root.get_attribute("id"), decisions)

    def _parse_decision(self, decision: XMLElement):
        _id = decision.get_attribute("id")
        required_decisions = [x.get_attribute("href")[1:] for x in decision.get_tags(".//dmn:requiredDecision")]
        decision_table = decision.get_tag("dmn:decisionTable")
        inputs = self._parse_inputs(decision_table)
        outputs = self._parse_outputs(decision_table)

        hit_policies = {h.name: h for h in HitPolicy}
        hit_policy = hit_policies[decision_table.get_attribute("hitPolicy") or "UNIQUE"]

        rules = [self._parse_rule(rule) for rule in decision_table.get_tags("dmn:rule")]
        return DmnDecision(_id, required_decisions, inputs, outputs, rules, hit_policy)

    def _parse_inputs(self, decision_table: XMLElement) -> List[DmnValue]:
        input_expressions = decision_table.get_tags(".//dmn:inputExpression")
        return [DmnValue(e.get_tag("dmn:text").get_text(), e.get_attribute("typeRef")) for e in input_expressions]

    def _parse_outputs(self, decision_table: XMLElement) -> List[DmnValue]:
        outputs = decision_table.get_tags(".//dmn:output")
        return [DmnValue(e.get_attribute("name"), e.get_attribute("typeRef")) for e in outputs]

    def _parse_rule(self, rule: XMLElement) -> DmnRule:
        inputs = list(map(lambda e: e.get_text(), rule.get_tags("dmn:inputEntry/dmn:text")))
        outputs = list(map(lambda e: e.get_text(), rule.get_tags("dmn:outputEntry/dmn:text")))

        return DmnRule(inputs, outputs)

from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode, CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.factory.business_rule_factory import BusinessRuleFactory
from arrow_bpmn.parser.json.json_element import JSONElement
from arrow_bpmn.parser.xml.xml_element import XMLElement


class BusinessRuleTask(BpmnNode):

    def __init__(self, attributes: dict, implementation: str):
        super().__init__(attributes)
        self.implementation = implementation

    def with_business_rule_factory(self, factory: BusinessRuleFactory, environment: Environment):
        if isinstance(self.implementation, str):
            self.implementation = factory.create(environment.group, self.implementation)

    @staticmethod
    def from_json(element: JSONElement) -> 'BusinessRuleTask':
        implementation = element.pop("implementation")
        return BusinessRuleTask(element.as_dict(), implementation)

    @staticmethod
    def from_xml(element: XMLElement) -> 'BusinessRuleTask':
        implementation = element.get_attribute("implementation")
        return BusinessRuleTask(element.get_attributes(), implementation)

    # noinspection PyUnresolvedReferences
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        engine = environment.business_rule_factory(self.implementation)
        process_ref = ProcessRef(environment.group, self.implementation)
        state.properties.update(engine.execute(process_ref, state.properties))

        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"BusinessRuleTask({self.id})"

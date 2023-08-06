from typing import Tuple

from arrow.arrow_dmn.__spi__ import DmnEngine
from arrow.arrow_dmn.__spi__ import ProcessRef

from arrow_bpmn.__spi__ import BpmnNode, CompleteAction
from arrow_bpmn.__spi__.action import Actions, ContinueAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.parser.xml.xml_element import XMLElement


class BusinessRuleTask(BpmnNode):

    def __init__(self, element: XMLElement, business_rule_engine: DmnEngine):
        super().__init__(element)
        self.implementation = element.get_attribute("implementation")
        self.engine = business_rule_engine

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        process_ref = ProcessRef(environment.group, self.implementation)
        state.properties.update(self.engine.execute(process_ref, state.properties))

        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"BusinessRuleTask({self.id})"

from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.types import ServiceFactory
from arrow_bpmn.parser.xml.xml_element import XMLElement


class ServiceTask(BpmnNode):

    def __init__(self, element: XMLElement, service_factory: ServiceFactory):
        super().__init__(element)
        self.implementation = element.get_attribute("implementation")
        self.service_factory = service_factory

    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        delegate = self.service_factory(self.implementation)
        return delegate.execute(state, environment)

    def __repr__(self):
        return f"ServiceTask({self.id})"

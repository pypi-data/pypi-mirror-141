import xml.sax.saxutils as sax
from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions, EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.execution.script_factory import ScriptFactory
from arrow_bpmn.engine.registry.abstract_event_registry import ErrorEvent
from arrow_bpmn.parser.xml.xml_element import XMLElement


class ScriptTask(BpmnNode):

    def __init__(self, element: XMLElement, script_factory: ScriptFactory):
        super().__init__(element)
        self.var_name = element.get_attribute("xy:varName") or "result"
        self.format = element.get_attribute("scriptFormat")
        self.script = sax.unescape(element.get_tag("bpmn:script").get_text())
        self.engine = script_factory.parse(self.format, self.script)

    # noinspection PyBroadException
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        try:
            result = self.engine.execute(state.properties)
            state[self.var_name] = result
        except Exception:
            return state, [EventAction(self.id, ErrorEvent(environment.group, "script-error"))]

        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"ScriptTask({self.id})"

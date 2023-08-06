from typing import Tuple

from arrow_bpmn.__spi__ import BpmnNode
from arrow_bpmn.__spi__ import CompleteAction
from arrow_bpmn.__spi__.action import ContinueAction, Actions, EventAction
from arrow_bpmn.__spi__.execution import Environment
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.engine.registry.abstract_event_registry import ErrorEvent
from arrow_bpmn.parser.json.json_element import JSONElement
from arrow_bpmn.parser.xml.xml_element import XMLElement


class ScriptTask(BpmnNode):

    def __init__(self, attributes: dict, var_name: str, format: str, script: str):
        super().__init__(attributes)
        self.var_name = var_name
        self.format = format
        self.script = script

    @staticmethod
    def from_json(element: JSONElement) -> 'ScriptTask':
        item = element.get_object("item")
        var_name = item.pop("var_name")
        _format = item.pop("format")
        _script = item.pop("script")
        return ScriptTask(item.as_dict(), var_name, _format, _script)

    @staticmethod
    def from_xml(element: XMLElement) -> 'ScriptTask':
        attributes = element.get_attributes()
        var_name = element["xy:varName"] or "result"
        _format = element["scriptFormat"]
        _script = element.get_tag("bpmn:script").get_text(True)

        return ScriptTask(attributes, var_name, _format, _script)

    # noinspection PyBroadException, PyUnresolvedReferences
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        try:
            engine = environment.script_factory(self.format, self.script)
            result = engine.execute(state.properties)
            state[self.var_name] = result
        except Exception:
            return state, [EventAction(self.id, ErrorEvent(environment.group, "script-error"))]

        actions = [ContinueAction(node) for node in environment.get_outgoing_nodes(self.id)]
        return state, [CompleteAction(self.id)] + actions

    def __repr__(self):
        return f"ScriptTask({self.id})"

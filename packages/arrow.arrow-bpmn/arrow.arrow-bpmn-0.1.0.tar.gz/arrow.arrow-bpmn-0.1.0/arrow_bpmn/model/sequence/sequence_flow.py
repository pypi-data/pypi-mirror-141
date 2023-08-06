from arrow_bpmn.__spi__ import BpmnEdge
from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.execution.script_factory import ScriptFactory
from arrow_bpmn.parser.xml.xml_element import XMLElement


class SequenceFlow(BpmnEdge):

    def __init__(self, element: XMLElement, script_factory: ScriptFactory):
        super().__init__(element)
        expression = element.get_tag("bpmn:conditionExpression")
        self.expression = expression.get_text() if expression is not None else None
        self.script_factory = script_factory

    def evaluate(self, state: State) -> bool:
        if self.expression is not None:
            engine = self.script_factory.parse("hypothesis", self.expression)
            return engine.execute(state.properties)

        return True

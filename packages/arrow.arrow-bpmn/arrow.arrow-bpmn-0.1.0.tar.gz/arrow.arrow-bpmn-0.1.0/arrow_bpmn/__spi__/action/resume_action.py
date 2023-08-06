from dataclasses import dataclass

from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.__spi__.registry import NodeRef


@dataclass
class ResumeAction(Action):
    reference: NodeRef

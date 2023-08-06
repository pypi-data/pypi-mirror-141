from dataclasses import dataclass

from arrow_bpmn.__spi__.action import Action
from arrow_bpmn.__spi__.registry import NodeRef


@dataclass
class CascadeAction(Action):
    parent_reference: NodeRef
    process_id: str
    init_state: dict

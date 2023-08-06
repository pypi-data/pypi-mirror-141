from dataclasses import dataclass
from typing import Optional


@dataclass
class NodeRef:
    """
    The NodeRef class is used to define the node invocation target of an event.
    This implementation can point to a start event, task or intermediate catching event.

    While a start event only has a process id and a node id a task and intermediate catching event
    needs the process instance id and node instance id as well.
    """

    process_id: str
    node_id: str
    process_instance_id: Optional[str] = None
    node_instance_id: Optional[str] = None

    @staticmethod
    def parse(text: str):
        array = text.split(":")
        assert len(array) == 2 or len(array) == 4, "invalid node ref string representation"

        if len(array) == 2:
            return NodeRef(array[0], array[1])
        return NodeRef(array[0], array[1], array[2], array[3])

    def __repr__(self):
        if self.process_instance_id is not None and self.node_instance_id is not None:
            return self.process_id + ":" + self.node_id + ":" + self.process_instance_id + ":" + self.node_instance_id
        return self.process_id + ":" + self.node_id

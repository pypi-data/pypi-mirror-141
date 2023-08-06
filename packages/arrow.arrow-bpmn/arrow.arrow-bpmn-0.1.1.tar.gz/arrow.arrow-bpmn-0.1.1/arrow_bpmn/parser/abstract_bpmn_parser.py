from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

from arrow_bpmn.__spi__.types import BpmnSource
from arrow_bpmn.model.process import Process


@dataclass
class BpmnParser(ABC):

    @abstractmethod
    def parse(self, source: BpmnSource) -> Tuple[str, List[Process]]:
        pass

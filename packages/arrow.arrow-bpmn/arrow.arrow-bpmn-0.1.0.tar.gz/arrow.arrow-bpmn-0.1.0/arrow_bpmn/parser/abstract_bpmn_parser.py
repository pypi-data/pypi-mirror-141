from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from arrow_bpmn.__spi__.execution.script_factory import ScriptFactory
from arrow_bpmn.__spi__.types import ServiceFactory, BusinessRuleFactory
from arrow_bpmn.engine.execution.cacheable_script_factory import CacheableScriptFactory
from arrow_bpmn.model.process import Process
from arrow_dmn.engine.sync_dmn_engine import SyncDmnEngine

DiagramSource = Path


@dataclass
class BpmnParser(ABC):
    service_factory: ServiceFactory = lambda x: []
    script_factory: ScriptFactory = CacheableScriptFactory(128)
    business_rule_engine: BusinessRuleFactory = lambda x, y: SyncDmnEngine()

    @abstractmethod
    def parse(self, source: DiagramSource) -> Tuple[str, List[Process]]:
        pass

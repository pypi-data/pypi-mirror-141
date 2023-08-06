from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Optional, List

from arrow_bpmn.__spi__.execution import State
from arrow_bpmn.__spi__.execution.event_emitter import EventEmitter
from arrow_bpmn.__spi__.execution.incident_handler import IncidentHandler, LoggingIncidentHandler
from arrow_bpmn.__spi__.registry.event import Event
from arrow_bpmn.engine.event.eager_event_emitter import EagerEventEmitter
from arrow_bpmn.engine.listener.abstract_bpmn_engine_listener import BpmnEngineListener
from arrow_bpmn.engine.registry.abstract_event_registry import EventRegistry, ProcessRef
from arrow_bpmn.engine.registry.inmemory_event_registry import InMemoryEventRegistry
from arrow_bpmn.engine.store.abstract_process_store import ProcessStore
from arrow_bpmn.engine.store.inmemory_process_story import InMemoryProcessStore
from arrow_bpmn.parser.abstract_bpmn_parser import BpmnParser
from arrow_bpmn.parser.xml.xml_bpmn_parser import XmlBpmnParser

BpmnSource = Union[Path]


@dataclass
class BpmnEngine:
    parser: BpmnParser = field(default_factory=lambda: XmlBpmnParser())
    event_registry: EventRegistry = field(default_factory=lambda: InMemoryEventRegistry())
    process_store: ProcessStore = field(default_factory=lambda: InMemoryProcessStore())
    listeners: List[BpmnEngineListener] = field(default_factory=lambda: [])
    incident_handler: IncidentHandler = field(default_factory=lambda: LoggingIncidentHandler())
    event_emitter: EventEmitter = field(default_factory=lambda: EagerEventEmitter())

    def deploy(self, source: BpmnSource) -> List[ProcessRef]:
        deployed_processes = []
        definitions_id, processes = self.parser.parse(source)
        for process in processes:
            process_ref = ProcessRef(definitions_id, process.id)
            process.with_event_registry(process_ref, self.event_registry)
            self.process_store.write_process(definitions_id, process)

            deployed_processes.append(process_ref)

        return deployed_processes

    def invoke_by_event(self, event: Event, init_state: Optional[dict] = None) -> List[State]:
        pass

    def resume_by_event(self, event: Event, init_state: Optional[dict] = None) -> List[State]:
        pass

    def invoke_by_id(self, process: ProcessRef, init_state: Optional[dict] = None) -> State:
        pass

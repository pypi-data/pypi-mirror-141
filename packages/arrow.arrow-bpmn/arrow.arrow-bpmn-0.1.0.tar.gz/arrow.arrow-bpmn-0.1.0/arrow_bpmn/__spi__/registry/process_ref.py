from dataclasses import dataclass


@dataclass
class ProcessRef:
    group: str
    process_id: str
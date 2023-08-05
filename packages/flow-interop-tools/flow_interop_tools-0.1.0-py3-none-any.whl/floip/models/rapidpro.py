"""
Steps for flow conversion:
1 - Parse json to RP object
2 - Validate the RP flow for conversion
    2.1 - Are all components compatible?
2 - Convert RP objects to FLOIP objects
    
3 - Serialize back to json
"""
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class RapidProFlow:
    uuid: UUID = field(default_factory=uuid4)
    name: str = ""
    language: str = "base"  # TODO: define default language and configuration
    type: str = "messaging"
    nodes: list = field(default_factory=list)


@dataclass
class RapidProContainer:
    version: str = "13"
    flows: list[RapidProFlow] = field(default_factory=list)


from abc import ABC, abstractmethod
from typing import Union, Tuple

from arrow_bpmn.__spi__.action import Actions
from arrow_bpmn.__spi__.execution import State, Environment
from arrow_bpmn.parser.xml.xml_element import XMLElement


class BpmnNode(ABC):

    def __init__(self, element: Union[XMLElement, dict]):
        self.__dict__ = element.get_attributes() if isinstance(element, XMLElement) else element

    @property
    def name(self) -> str:
        """
        Returns the name of the edge.
        :return: str
        """
        return self.__dict__["name"]

    @property
    def id(self) -> str:
        """
        Returns the id of the edge.
        :return: str
        """
        return self.__dict__["id"]

    @abstractmethod
    def execute(self, state: State, environment: Environment) -> Tuple[State, Actions]:
        pass

    @abstractmethod
    def __repr__(self):
        pass

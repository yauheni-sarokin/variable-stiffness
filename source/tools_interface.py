from abc import ABC, abstractmethod
from typing import List
from enum import Enum, auto


class Entity(ABC):

    def __init__(self, voltage: float, current: float, force: float, displacement: float, time: float,
                 cycle: float) -> None:
        self._voltage = voltage
        self._current = current
        self._force = force
        self._displacement = displacement
        self._time = time
        self._cycle = cycle

    @property
    def voltage(self) -> float:
        return self._voltage

    @property
    def current(self):
        return self._current

    @property
    def force(self):
        return self._force

    @property
    def displacement(self):
        return self._displacement

    @property
    def time(self):
        return self._time

    @property
    def cycle(self):
        return self._cycle


class Content(ABC):

    @abstractmethod
    def __init__(self, content: List[str]) -> None:
        pass

    @abstractmethod
    def get_entities_from_content(self) -> List[Entity]:
        pass


class FileReader(ABC):
    """
    Reads file content from file string
    """

    @abstractmethod
    def __init__(self, file: str) -> None:
        """
        Create file reader ready to read files
        :param file: file to read
        """

        pass

    @abstractmethod
    def parse_file_content(self) -> Content:
        pass

#Enumeration of entity properties
class EntityProperty(Enum):
    VOLTAGE = auto()
    CURRENT = auto()
    FORCE = auto()
    DISPLACEMENT = auto()
    TIME = auto()
    CYCLE = auto()

class EntityGroup(ABC):
    """
    Entities can be divided into many groups,
    this class is abstract and provide already divided
    entities
    """

    def __init__(self, entity_property: EntityProperty) -> None:
        self._entity_property = entity_property
        self._list = []

    @property
    def entities(self) -> List[Entity]:
        return self._list

    def append(self, entity: Entity) -> None:
        self._list.append(entity)

    @property
    def entity_property(self):
        """
        Contains property by which group is formed
        :return: Returns enumeration value
        """
        return self._entity_property

"""
Abstract factory pattern
"""


class EntityGroupCreator(ABC):

    def __init__(self, entities: List[Entity]) -> None:
        self._entities = entities

    @abstractmethod
    def divide_entities_by_voltage(self, voltage_round=1) -> List[EntityGroup]:
        """
        Entities are divided into voltage groups
        :param voltage_round: How many float signs to round
        :return:
        """
        pass

    @abstractmethod
    def divide_entities_by_current(self) -> List[EntityGroup]:
        pass

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List


# Enumeration of entity properties
class EntityProperty(Enum):
    VOLTAGE = {'name': 'voltage', 'units': 'V'}
    CURRENT = {'name': 'current', 'units': 'mA/uA'}
    FORCE = {'name': 'force', 'units': 'uN'}
    DISPLACEMENT = {'name': 'displacement', 'units': 'mm'}
    TIME = {'name': 'time', 'units': 'ms'}
    CYCLE = {'name': 'cycle', 'units': 'cycles'}
    # NO_GROUP = auto()


class Entity(ABC):

    def __init__(self, voltage: float, current: float, force: float, displacement: float,
                 time: float,
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

    def get_property(self, entity_property: EntityProperty) -> float:
        if entity_property == entity_property.VOLTAGE:
            return self._voltage
        elif entity_property == entity_property.CURRENT:
            return self._current
        elif entity_property == entity_property.FORCE:
            return self._force
        elif entity_property == entity_property.DISPLACEMENT:
            return self._displacement
        elif entity_property == entity_property.TIME:
            return self._time
        elif entity_property == entity_property.CYCLE:
            return self._cycle
        else:
            pass


class Content(ABC):

    @abstractmethod
    def __init__(self, content: List[str]) -> None:
        self._content = content

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

        self._file = file

    @abstractmethod
    def parse_file_content(self) -> Content:
        pass


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

    def get_array_of_properties(self, entity_property: EntityProperty) -> List[float]:
        # create list with all possible properties
        properties_list = []

        for entity in self.entities:
            get_property = entity.get_property(entity_property)
            properties_list.append(get_property)

        return properties_list


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

    @abstractmethod
    def divide_entities_by_cycle(self) -> List[EntityGroup]:
        pass


class EntityGroupPlotter(ABC):

    def __init__(self) -> None:
        self._entity_groups: List[EntityGroup] = []

    @property
    def entity_group(self):
        return self._entity_groups

    def add_entity_group(self, entity_group: EntityGroup) -> None:
        """
        add entity group to plot to pool
        :return: None
        """
        self._entity_groups.append(entity_group)

    @abstractmethod
    def plot_group(self, entity_group: EntityGroup,
                   x_axis_property: EntityProperty, y_axis_property: EntityProperty) -> None:
        pass

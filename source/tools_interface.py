from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import List

import Colors


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


class Content(ABC):

    @abstractmethod
    def __init__(self, content: List[str]) -> None:
        self._content = content

    # @abstractmethod
    # def get_entities_from_content(self) -> List[Entity]:
    #     pass

    @abstractmethod
    def get_entity_group_from_content(self) -> EntityGroup:
        pass


# Enumeration of entity properties
class EntityProperty(Enum):
    VOLTAGE = {'name': 'voltage', 'units': 'V', 'has_value': True}
    CURRENT = {'name': 'current', 'units': 'mA/uA', 'has_value': True}
    FORCE = {'name': 'force', 'units': 'uN', 'has_value': True}
    DISPLACEMENT = {'name': 'displacement', 'units': 'mm', 'has_value': True}
    TIME = {'name': 'time', 'units': 'ms', 'has_value': True}
    CYCLE = {'name': 'cycle', 'units': 'cycles', 'has_value': True}

    NO_GROUP = {'name': 'no group', 'units': 'no units', 'has_value': False}

    SLOPE_UP = {'name': 'slope up', 'units': 'no units', 'has_value': False}
    SLOPE_DOWN = {'name': 'slope down', 'units': 'no units', 'has_value': False}


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


"""
Entity groups are represented by composite patter
to allow sub division
"""


class EntityGroup(ABC):
    """
    Entities can be divided into many groups,
    this class is abstract and provide already divided
    entities
    """

    def __init__(self,
                 entity_property: EntityProperty,
                 property_value: float = None,
                 parent: EntityGroup = None,
                 children: List[EntityGroup] = None) -> None:

        self._entity_property = entity_property
        self._property_value = property_value
        # all entities in the group
        self._entities = []

        # #todo new update, if works, delete later
        if parent is not None:
            self._parent: EntityGroup = parent
            # self._has_parent = True
        self._has_parent: bool = parent is not None

        if children is not None:
            self._children: List[EntityGroup] = children
            self._has_children: bool = True
        else:
            self._children: List[EntityGroup] = []
            self._has_children: bool = False

        # default blue line
        self._color_line: Colors.RGBColor = Colors.RGBColor([0, 128, 255])

    @property
    def color_line(self):
        return self._color_line

    @color_line.setter
    def color_line(self, value: Colors.RGBColor):
        self._color_line = value

    @property
    def has_parent(self) -> bool:
        return self._has_parent

    @property
    def parent(self) -> EntityGroup:
        if self._has_parent:
            return self._parent
        else:
            raise NameError('No parent in EntityGroup')

    @parent.setter
    def parent(self, parent: EntityGroup):
        self._has_parent = True
        self._parent = parent

    @property
    def has_children(self) -> bool:
        return self._has_children

    @property
    def children(self) -> List[EntityGroup]:
        if self._has_children:
            return self._children
        else:
            raise NameError('No children in EntityGroup')

    @children.setter
    def children(self, children: List[EntityGroup]):
        self._has_children = True
        self._children = children

    @property
    def entities(self) -> List[Entity]:
        """
        Return all entities in the group, not from children
        :return:
        """
        return self._entities

    def append(self, entity: Entity) -> None:
        """
        Append entity one by one to the group
        :param entity:
        :return:
        """
        self._entities.append(entity)

    @property
    def entity_property(self):
        """
        Contains property by which group is formed
        :return: Returns enumeration value
        """
        return self._entity_property

    @property
    def property_value(self):
        return self._property_value

    def get_array_of_properties(self, entity_property: EntityProperty) -> List[float]:
        # create list with all possible properties for building graphs
        properties_list = []

        for entity in self.entities:
            get_property = entity.get_property(entity_property)
            properties_list.append(get_property)

        return properties_list

    def __str__(self) -> str:
        children_amount: int = len(self.children) if self._has_children else 0

        string = f'============================================================\n' \
                 f'has children: {self._has_children} amount: {children_amount} \n' \
                 f'has parent: {self.has_parent} \n' \
                 f'amount of entities : {len(self._entities)} \n' \
                 f'entity property : {self._entity_property} and value : {self._property_value}\n' \
                 f'============================================================\n'
        return string


"""
Abstract factory pattern
"""


class EntityGroupCreator(ABC):
    """
    Accepts entities as list and divide it into groups
    and return EntityGroup divided by properties
    """

    """
    DEPRECATED
    """

    # def __init__(self, entities: List[Entity]) -> None:
    #     self._entities = entities

    @abstractmethod
    def divide_entities_by_current(self, entity_group: EntityGroup) -> EntityGroup:
        pass

    @abstractmethod
    def divide_entities_by_slope(self,
                                 entity_group: EntityGroup,
                                 entity_property: EntityProperty) \
            -> List[EntityGroup]:
        pass

    """
    NEW
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def divide_entities_by_voltage(self,
                                   entity_group: EntityGroup,
                                   voltage_round=1) -> EntityGroup:
        """
        Entities are divided into voltage groups
        :param entity_group:
        :param voltage_round: How many float signs to round
        :return: the same entity group with children
        """
        pass

    @abstractmethod
    def get_entities_group_without_division(self, entities: List[Entity]) -> EntityGroup:
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

    def add_entity_groups(self, entity_groups: List[EntityGroup]) -> None:
        self._entity_groups.extend(entity_groups)

    @abstractmethod
    def plot_group(self, entity_group: EntityGroup,
                   x_axis_property: EntityProperty,
                   y_axis_property: EntityProperty) -> None:
        pass

    @abstractmethod
    def plot_groups(self,
                    x_axis_property: EntityProperty,
                    y_axis_property: EntityProperty) -> None:
        pass


"""
Entity group decorator
To change children's property
"""


class EntityGroupDecorator(EntityGroup):

    def __init__(self, entity_group: EntityGroup) -> None:

        # entity property
        group_entity_property = entity_group.entity_property

        # property value
        group_property_value = None
        if entity_group.entity_property.value['has_value']:
            group_property_value = entity_group.property_value

        # parent
        group_property_parent = None
        if entity_group.has_parent:
            group_property_parent = entity_group.parent

        # children
        group_property_children = None
        if entity_group.has_parent:
            group_property_children = entity_group.children

        # initialize
        super().__init__(group_entity_property,
                         group_property_value,
                         group_property_parent,
                         group_property_children)

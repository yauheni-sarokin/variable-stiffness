from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class Entity(ABC):

    def __init__(self, voltage: float, current: float, force: float, displacement: float, time: int, cycle: int) -> None:
        self._voltage = voltage
        self._current = current
        self._force = force
        self._displacement = displacement
        self._time = time
        self._cycle = cycle

    @property
    def voltage(self):
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

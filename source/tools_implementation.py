from tools_interface import *


class ConcreteEntity(Entity):
    pass


class ConcreteContent(Content):

    def __init__(self, content: List[str]) -> None:
        content.remove(content[0])
        super().__init__(content)

    def get_entities_from_content(self) -> List[Entity]:
        entities_list: List[Entity] = []

        for line in self._content:
            # line is a string that contains data, so string have to be divided
            data = line.strip().replace(',', '.').split("\t")
            # first row is a voltage, float
            voltage = float(data[0].strip())
            # second row is a current, uA, float
            current = float(data[1].strip())
            # third row is a force sensor data, uN, float
            force = float(data[2].strip())
            # 4th row is a displacement in mm, float
            displacement = float(data[3].strip())
            # 5th row is a time in ms, int
            time = float(data[4].strip())
            # 6th row is a number of cycle, int
            cycle = float(data[5].strip())

            entity = ConcreteEntity(voltage, current, force, displacement, time, cycle)

            entities_list.append(entity)

        return entities_list


class ConcreteFileReader(FileReader):

    def __init__(self, file: str) -> None:
        # todo add exception handler
        super().__init__(file)

    def parse_file_content(self) -> Content:
        # Set file with test data to read, r means read
        file_to_read = open(self._file, "r", encoding="latin-1")

        content = file_to_read.readlines()

        # Close file after reading
        file_to_read.close()

        return ConcreteContent(content)


"""
Разбиение сущностей по группам
"""


class EntityGroupByVoltage(EntityGroup):

    def __init__(self, voltage: float) -> None:
        super().__init__(EntityProperty.VOLTAGE)
        self._voltage = voltage

    @property
    def voltage(self) -> float:
        return self._voltage


class EntityGroupByCurrent(EntityGroup):

    def __init__(self, current: float) -> None:
        super().__init__(EntityProperty.CURRENT)
        self._current = current

    @property
    def current(self) -> float:
        return self.current


class ConcreteEntityGroupCreator(EntityGroupCreator):

    def divide_entities_by_voltage(self, voltage_round=1) -> List[EntityGroup]:
        # All entities from content
        entities = self._entities

        # iterator mechanism

        current_v = round(entities[0].voltage, voltage_round)

        current_entities_group = EntityGroupByVoltage(current_v)
        entities_group_list = [current_entities_group]

        # iterate all entities
        for entity in entities:
            voltage = entity.voltage
            voltage_rounded = round(voltage, voltage_round)
            if current_v == voltage_rounded:
                current_entities_group.append(entity)
            else:
                current_v = voltage_rounded
                current_entities_group = EntityGroupByVoltage(current_v)
                entities_group_list.append(current_entities_group)
                current_entities_group.append(entity)

        return entities_group_list

    def divide_entities_by_current(self) -> List[EntityGroup]:
        # todo
        pass

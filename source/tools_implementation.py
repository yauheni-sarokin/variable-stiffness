import matplotlib.pyplot as plt

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
        super().__init__(EntityProperty.VOLTAGE, voltage)
        self._voltage = voltage

    @property
    def voltage(self) -> float:
        return self._voltage


class EntityGroupByCurrent(EntityGroup):

    def __init__(self, current: float) -> None:
        super().__init__(EntityProperty.CURRENT, current)
        self._current = current

    @property
    def current(self) -> float:
        return self.current


class EntityGroupNoDivision(EntityGroup):

    def __init__(self) -> None:
        super().__init__(EntityProperty.NO_GROUP)


class EntityGroupBySlope(EntityGroup):

    def __init__(self, entity_property: EntityProperty, property_value: float) -> None:
        super().__init__(entity_property)
        self._property_value = property_value
        self._slope_up_list: List[Entity] = []
        self._slope_down_list: List[Entity] = []

    @property
    def property_value(self) -> float:
        return self._property_value

    def append_slope_up(self, entity: Entity):
        self._slope_up_list.append(entity)

    def append_slope_down(self, entity: Entity):
        self._slope_down_list.append(entity)

    @property
    def slope_up(self) -> List[Entity]:
        return self._slope_up_list

    @property
    def slope_down(self) -> List[Entity]:
        return self._slope_down_list


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

    def get_entities_group_without_division(self) -> EntityGroup:
        # All entities from content
        entities = self._entities

        entity_group = EntityGroupNoDivision()

        for entity in entities:
            entity_group.append(entity)

        return entity_group

    def divide_entities_by_slope(self,
                                 entity_property: EntityProperty,
                                 property_value: float,
                                 slope: EntityGroupSlope = EntityGroupSlope.SLOPE_UP) -> List[
        EntityGroup]:
        entities = self._entities

        # Following code from initial program, rewrite in case
        # of bugs

        entities_list: List[EntityGroupBySlope] = []

        # stores value of previous displacement to understand
        # loading unloading curves
        previous_displacement = 0.
        # stores true in case of loading (increasing displacement)
        slope_up = True

        current_entity_group = EntityGroupBySlope(entity_property, property_value)

        for entity in entities:
            # if displacement is higher than the previous one and slope is up
            # then the entities belong to the same group of loading curve
            if entity.displacement > previous_displacement and slope_up:
                # change previous displacement
                previous_displacement = entity.displacement
                current_entity_group.append_slope_up(entity)

                if slope == EntityGroupSlope.SLOPE_UP:
                    current_entity_group.append(entity)

            # if displacement is higher than the previous but the slope is down
            # we start new cycle of loading after unloading
            # here we create a new displacement group and increase iteration
            elif entity.displacement > previous_displacement and not slope_up:
                previous_displacement = entity.displacement
                slope_up = True
                entities_list.append(current_entity_group)

                current_entity_group = EntityGroupBySlope(entity_property, property_value)
                current_entity_group.append_slope_up(entity)

                if slope == EntityGroupSlope.SLOPE_UP:
                    current_entity_group.append(entity)

            # if displacement is lower than the previous one and the slope is
            # up then we are going we start unloading curve
            elif entity.displacement < previous_displacement and slope_up:
                previous_displacement = entity.displacement
                slope_up = False

                current_entity_group.append_slope_down(entity)

                if slope == EntityGroupSlope.SLOPE_DOWN:
                    current_entity_group.append(entity)

            # if displacement is lower than the previous one and the slope is
            # down then the entities belong to the same group of loading curve
            elif entity.displacement < previous_displacement and not slope_up:
                previous_displacement = entity.displacement

                current_entity_group.append_slope_down(entity)

                if slope == EntityGroupSlope.SLOPE_DOWN:
                    current_entity_group.append(entity)

        return entities_list


class ConcreteEntityGroupPlotter(EntityGroupPlotter):

    def plot_group(self, entity_group: EntityGroup,
                   x_axis_property: EntityProperty, y_axis_property: EntityProperty) -> None:
        """
        Plot entity groups from the pool
        :param entity_group:
        :param x_axis_property:
        :param y_axis_property:
        :return:
        """

        # get x, y array
        x = entity_group.get_array_of_properties(x_axis_property)
        y = entity_group.get_array_of_properties(y_axis_property)

        fig, ax = plt.subplots()

        ax.plot(x, y)

        x_units = x_axis_property.value['units']
        x_name = x_axis_property.value['name']
        y_units = y_axis_property.value['units']
        y_name = y_axis_property.value['name']
        title = f"{y_name} - {x_name}"

        ax.set(xlabel=x_units, ylabel=y_units, title=title)

        plt.show()

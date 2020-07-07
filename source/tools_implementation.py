import matplotlib.pyplot as plt
from numpy import polyfit, polyval

from math_tool import *
from tools_interface import *

from scipy.interpolate import *


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

    def parse_entity_groups_from_file(self) -> EntityGroup:
        """
        Reads file by path and uses concrete content to parse
        entity groups from file
        :param file:
        :return:
        """
        file_content = self.parse_file_content()
        group_from_content = file_content.get_entity_group_from_content()

        return group_from_content


class ConcreteContent(Content):

    def __init__(self, content: List[str]) -> None:
        # remove header, does not carry any information
        content.remove(content[0])
        super().__init__(content)

    def get_entity_group_from_content(self) -> EntityGroup:
        # entities_list: List[Entity] = []

        entity_group = EntityGroupNoDivision()

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

            entity = ConcreteFileEntity(voltage, current, force, displacement, time, cycle)

            # entities_list.append(entity)

            entity_group.append_entity(entity)

        return entity_group


class ConcreteFileEntity(Entity):
    """
    Entity that come from file, can contain only
    predefined file properties
    """
    pass


class ConcreteExtendedEntity(Entity):
    """
    Entity that can be created upon file file elaboration
    introduces new properties to the file
    """
    pass


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
    """
    Creates EntityGroup without property and
    parent, used it for creating group from content
    """

    def __init__(self) -> None:
        super().__init__(EntityProperty.NO_GROUP)


class EntityGroupBySlope(EntityGroup):

    def __init__(self, entity_property: EntityProperty) -> None:
        super().__init__(entity_property)

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

    def divide_entities_by_voltage(self,
                                   entity_group: EntityGroup,
                                   voltage_round=1) -> EntityGroup:
        # All entities from content
        entities = entity_group.entities

        # iterator mechanism

        current_v = round(entities[0].voltage, voltage_round)

        current_entities_group = EntityGroupByVoltage(current_v)
        current_entities_group.parent = entity_group
        entities_group_list = [current_entities_group]

        # iterate all entities
        for entity in entities:
            voltage = entity.voltage
            voltage_rounded = round(voltage, voltage_round)
            if current_v == voltage_rounded:
                current_entities_group.append_entity(entity)
            else:
                current_v = voltage_rounded
                current_entities_group = EntityGroupByVoltage(current_v)
                current_entities_group.parent = entity_group
                entities_group_list.append(current_entities_group)
                current_entities_group.append_entity(entity)

        entity_group.children = entities_group_list

        return entity_group

    def divide_entities_by_current(self, entity_group: EntityGroup) -> EntityGroup:
        # todo
        pass

    def get_entities_group_without_division(self, entities: List[Entity]) -> EntityGroup:
        # All entities from content

        entity_group = EntityGroupNoDivision()

        for entity in entities:
            entity_group.append_entity(entity)

        return entity_group

    def divide_entities_by_slope(self,
                                 entity_group: EntityGroup,
                                 entity_property: EntityProperty = EntityProperty.SLOPE_UP) \
            -> EntityGroup:
        """
        Returns the same group but with added children
        :param entity_group:
        :param entity_property:
        :return:
        """
        entities = entity_group.entities

        # Following code from initial program, rewrite in case
        # of bugs

        entities_list: List[EntityGroupBySlope] = []

        # stores value of previous displacement to understand
        # loading unloading curves
        previous_displacement = 0.
        # stores true in case of loading (increasing displacement)
        slope_up = True

        current_entity_group = EntityGroupBySlope(entity_property)

        for entity in entities:
            # if displacement is higher than the previous one and slope is up
            # then the entities belong to the same group of loading curve
            if entity.displacement > previous_displacement and slope_up:
                # change previous displacement
                previous_displacement = entity.displacement
                current_entity_group.append_slope_up(entity)

                if entity_property == EntityProperty.SLOPE_UP:
                    current_entity_group.append_entity(entity)

            # if displacement is higher than the previous but the slope is down
            # we start new cycle of loading after unloading
            # here we create a new displacement group and increase iteration
            elif entity.displacement > previous_displacement and not slope_up:
                previous_displacement = entity.displacement
                slope_up = True
                entities_list.append(current_entity_group)

                current_entity_group = EntityGroupBySlope(entity_property)
                current_entity_group.append_slope_up(entity)

                if entity_property == EntityProperty.SLOPE_UP:
                    current_entity_group.append_entity(entity)

            # if displacement is lower than the previous one and the slope is
            # up then we are going we start unloading curve
            elif entity.displacement < previous_displacement and slope_up:
                previous_displacement = entity.displacement
                slope_up = False

                current_entity_group.append_slope_down(entity)

                if entity_property == EntityProperty.SLOPE_DOWN:
                    current_entity_group.append_entity(entity)

            # if displacement is lower than the previous one and the slope is
            # down then the entities belong to the same group of loading curve
            elif entity.displacement < previous_displacement and not slope_up:
                previous_displacement = entity.displacement

                current_entity_group.append_slope_down(entity)

                if entity_property == EntityProperty.SLOPE_DOWN:
                    current_entity_group.append_entity(entity)

        entity_group.children = entities_list

        return entity_group


class ConcreteEntityGroupPlotter(EntityGroupPlotter):

    def plot_entities_in_group(self, entity_group: EntityGroup,
                               x_axis_property: EntityProperty,
                               y_axis_property: EntityProperty) -> None:
        """
        Plot entity groups from the pool
        :param entity_group:
        :param x_axis_property:
        :param y_axis_property:
        :return:
        """
        # get x, y array
        # print(len(entity_group.entities))
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

    def plot_added_groups(self, x_axis_property: EntityProperty,
                          y_axis_property: EntityProperty) -> None:
        """
        Plot entity groups from the pool
        :param x_axis_property:
        :param y_axis_property:
        :return:
        """

        entity_groups = self._entity_groups

        fig, ax = plt.subplots()

        for entity_group in entity_groups:
            # get x, y array
            x = entity_group.get_array_of_properties(x_axis_property)
            y = entity_group.get_array_of_properties(y_axis_property)
            # hex_color = entity_group.color_line.to_hex().hex
            color_line = entity_group.color_line
            # ax.plot(x, y, color=hex_color)
            ax.plot(x, y, color=color_line)

        x_units = x_axis_property.value['units']
        x_name = x_axis_property.value['name']
        y_units = y_axis_property.value['units']
        y_name = y_axis_property.value['name']
        title = f"{y_name} - {x_name}"

        ax.set(xlabel=x_units, ylabel=y_units, title=title)

        plt.show()

    def plot_added_groups_with_cb(self,
                                  x_axis_property: EntityProperty,
                                  y_axis_property: EntityProperty
                                  ) -> None:

        entity_groups = self._entity_groups

        fig, ax = plt.subplots()

        # todo delete, rewrite 2 following lines
        colors = []
        voltages = []

        for entity_group in entity_groups:
            # get x, y array
            x = entity_group.get_array_of_properties(x_axis_property)
            y = entity_group.get_array_of_properties(y_axis_property)
            # hex_color = entity_group.color_line.to_hex().hex
            color_line = entity_group.color_line
            # ax.plot(x, y, color=hex_color)
            ax.plot(x, y, color=color_line)

            colors.append(entity_group.color_line)
            voltages.append(entity_group.property_value)

        x_units = x_axis_property.value['units']
        x_name = x_axis_property.value['name']
        y_units = y_axis_property.value['units']
        y_name = y_axis_property.value['name']
        title = f"{y_name} - {x_name}"

        ax.set(xlabel=x_units, ylabel=y_units, title=title)

        # adding color bars
        # ====================
        import matplotlib.colors as mcolors
        import matplotlib.cm
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        cmap, norm = mcolors.from_levels_and_colors(
            range(len(colors) + 1),
            colors
        )

        sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)

        cbar = fig.colorbar(sm, cax=cax, ticks=range(len(colors)))
        cbar.ax.set_yticklabels(voltages)
        # ====================
        plt.show()

    def plot_children(self, entity_group_with_children: EntityGroup,
                      x_axis_property: EntityProperty,
                      y_axis_property: EntityProperty) -> None:

        entity_groups = entity_group_with_children.children

        fig, ax = plt.subplots()

        for entity_group in entity_groups:
            # get x, y array
            x = entity_group.get_array_of_properties(x_axis_property)
            y = entity_group.get_array_of_properties(y_axis_property)
            # hex_color = entity_group.color_line.to_hex().hex
            color_line = entity_group.color_line
            # ax.plot(x, y, color=hex_color)
            ax.plot(x, y, color=color_line)

        x_units = x_axis_property.value['units']
        x_name = x_axis_property.value['name']
        y_units = y_axis_property.value['units']
        y_name = y_axis_property.value['name']
        title = f"{y_name} - {x_name}"

        ax.set(xlabel=x_units, ylabel=y_units, title=title)

        plt.show()


"""
Entity group decorator
To change children's property
"""


class ColorEntityGroupDecorator(EntityGroupDecorator):

    def __init__(self,
                 entity_group: EntityGroup,
                 color_gradient: Colors.ColorGradients = Colors.ColorGradients.BY_DESIGN) -> None:
        super().__init__(entity_group)

        children = self.children

        colors = Colors.get_color_gradient_array(len(children), color_gradient)

        for child, color in zip(children, colors):
            child.color_line = color


class CutChildrenEntityGroupDecorator(EntityGroupDecorator):
    """
    Decorator removes some children in the beginning and
    in the end of the list
    """

    # todo does not return a COPY but all the objects are the same instances

    def __init__(self, entity_group: EntityGroup,
                 start_cut: int = 0,
                 end_cut: int = 0) -> None:
        super().__init__(entity_group)

        children = self.children
        # self.color_line = entity_group.color_line

        if start_cut > 0:
            for i in range(start_cut):
                del children[0]

        if end_cut > 0:
            for i in range(end_cut):
                del children[-1]

        # self.children = children


class AveragingEntityGroupDecorator(EntityGroupDecorator):
    """
    Decorator converts entity group with many children into group
    with one child but averaged
    """

    def __init__(self,
                 entity_group: EntityGroup,
                 x_axis: EntityProperty,
                 y_axis: EntityProperty) -> None:
        super().__init__(entity_group)

        tool = MathTool()
        averaging = tool.make_averaging(self.children, x_axis, y_axis)

        # averaging.children = None

        self.entities = averaging.entities


class DerivativeEntityGroupDecorator(EntityGroupDecorator):
    """
    Decorator reads all entities as an array and return new
    entity group where all the entities are derivative
    """

    def __init__(self,
                 entity_group: EntityGroup,
                 x_axis: EntityProperty,
                 y_axis: EntityProperty) -> None:
        super().__init__(entity_group)

        tool = MathTool()

        entity_group_derivative = tool.make_derivative(self, x_axis, y_axis)

        self.entities = entity_group_derivative.entities


class CutEntitiesByXAxisDecorator(EntityGroupDecorator):
    """
    Cut entities within x axis
    """

    def __init__(self,
                 entity_group: EntityGroup,
                 x_axis: EntityProperty,
                 x_start: float,
                 x_end: float) -> None:
        super().__init__(entity_group)

        new_entities: List[Entity] = []

        for entity in self.entities:
            if x_start < entity.get_property(x_axis) < x_end:
                new_entities.append(entity)

        self.entities = new_entities


class LinearInterpolationEntityGroupDecorator(EntityGroupDecorator):
    def __init__(self, entity_group: EntityGroup) -> None:
        super().__init__(entity_group)

        x_axis = self.get_array_of_properties(EntityProperty.DISPLACEMENT)
        y_axis = self.get_array_of_properties(EntityProperty.FORCE)

        p1 = polyfit(x_axis, y_axis, 1)

        y_fitted = polyval(p1, x_axis)

        new_entities: List[Entity] = []

        for x, y in zip(x_axis, y_fitted):
            entity = Entity(0, 0, y, x, 0, 0)
            new_entities.append(entity)

        self.entities = new_entities

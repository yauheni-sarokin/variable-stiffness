from typing import List
from statistics import stdev, mean
from tools_interface import Entity, EntityGroup, EntityProperty
import numpy as np


class MathTool:

    def make_averaging(self,
                       children_groups: List[EntityGroup],
                       x_property: EntityProperty,
                       y_property: EntityProperty) -> EntityGroup:
        """
        take man groups between which we have to find one average
        :param y_property:
        :param x_property:
        :param children_groups:
        :return:
        """

        # for each x value there are many y values
        # 1. we assume that we have many lines with x nd y sets
        # 2. x set can be extended, so we make it in many small spaces
        # 3 we return for each x its onw new y value and fin average between these
        # y values

        # set precision 100
        _precision = 150

        x_sets: List[List[float]] = []
        y_sets: List[List[float]] = []

        for children_group in children_groups:
            x_axis = children_group.get_array_of_properties(x_property)
            y_axis = children_group.get_array_of_properties(y_property)

            x_sets.append(x_axis)
            y_sets.append(y_axis)

        # looking for end from one both sides by x, so that x start
        # later and x that finishes earlier
        # for this we look for x start with max displacement to right
        # and vice verse for end x

        x_start_set: List[float] = []
        x_end_set: List[float] = []

        for x_set in x_sets:
            x_set_minimum = min(x_set)
            x_set_maximum = max(x_set)

            x_start_set.append(x_set_minimum)
            x_end_set.append(x_set_maximum)

        # now define to ends of x axis
        x_starting = max(x_start_set)
        x_ending = min(x_end_set)

        # divide range between them into _precision

        x_set_new: List[float] = np.linspace(x_starting, x_ending, _precision)
        # too delete onw line below
        print(f"length of x after linspace {len(x_set_new)}")

        # for this x range we have to find all possible y's
        # collect many y's

        y_sets_new: List[List[float]] = []

        for x_set, y_set in zip(x_sets, y_sets):
            y_set_new: List[float] = []
            for x in x_set_new:
                y = self.__get_y_from_sets(x_set, y_set, x)
                y_set_new.append(y)
            y_sets_new.append(y_set_new)

        # now we have list of new x's and corresponding list of new y's

        y_set_new: List[float] = []

        for num, x in enumerate(x_set_new):
            # x is always a position
            # y set new is amount of entities, but each contain 150

            # collect y's
            y_set_to_average: List[float] = []
            for y_set in y_sets_new:
                y = y_set[num]
                y_set_to_average.append(y)

            y_avg = mean(y_set_to_average)

            y_set_new.append(y_avg)

        # todo MOCK ENTITY ALWAYS PUT FORCE DISPLACEMET

        entity_group = EntityGroup(EntityProperty.NO_GROUP)

        # print(entity_group)

        # create mock entities
        # entities_list: List[Entity] = []

        for x, y in zip(x_set_new, y_set_new):
            entity = Entity(0., 0., y, x, 0., 0.)
            # entities_list.append(entity)
            entity_group.append_entity(entity)

        return entity_group

    def __get_y_from_sets(self, x_set: List[float], y_set: List[float], x: float) -> float:
        """
        very important function, for any given x returns corresponding
        y value assuming extrapolation
        :param x_set:
        :param y_set:
        :param x:
        :return:
        """
        # y0 = ax0 + b, y1 = ax1 + b
        # a = (y0 - y1)/(x0 - x1)
        # b = y0 - a*x0
        # Вначале определим диапозон
        min_x, max_x, min_y, max_y = min(x_set), max(x_set), min(y_set), max(y_set)
        # y to return
        y: float = None
        # Throw exception if x is out of range
        if x > max_x or x < min_x:
            raise Exception("Your x = {} value is out of [xmin : {}, xmax : {}]"
                            " range".format(x, min_x, max_x))
        else:
            for index, x_from_set in enumerate(x_set):
                if x == x_from_set:
                    y = y_set[index]
                    break
                elif x_set[index] < x < x_set[index + 1]:
                    x0, x1, y0, y1 = x_set[index], x_set[index + 1], y_set[index], y_set[index + 1]
                    a = (y0 - y1) / (x0 - x1)
                    b = y0 - a * x0
                    y = a * x + b
                    break
        return y

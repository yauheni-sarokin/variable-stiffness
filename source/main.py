from tools_implementation import *
from math_tool import *

if __name__ == '__main__':
    file = "../testdata/varstif9/0v_to_-2V_200mV_10mA_5min_step_plain_side.txt"
    file_reader = ConcreteFileReader(file)
    content = file_reader.parse_file_content()
    group_from_content = content.get_entity_group_from_content()

    group_creator = ConcreteEntityGroupCreator()
    group_plotter = ConcreteEntityGroupPlotter()

    group = group_creator.divide_entities_by_voltage(group_from_content)

    # take 1 voltage group
    voltage_group = 6
    group = group.children[voltage_group]

    group = group_creator.divide_entities_by_slope(group)

    group = ColorEntityGroupDecorator(group)

    group_plotter.plot_children(group, EntityProperty.TIME, EntityProperty.CURRENT)

    group = CutChildrenEntityGroupDecorator(group, end_cut=2, start_cut=20)

    group = AveragingEntityGroupDecorator(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    # print(len(group.entities))

    group = CutEntitiesByXAxisDecorator(group, EntityProperty.DISPLACEMENT, x_start=0.03, x_end=0.2)

    # print(len(group.entities))

    # group_plotter.plot_entities_in_group(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    group_plotter.add_entity_group(group)

    derivative1 = DerivativeEntityGroupDecorator(group, EntityProperty.DISPLACEMENT,
                                               EntityProperty.FORCE)

    group = LinearInterpolationEntityGroupDecorator(group)
    group.color_line = Colors.RGBColor([255, 0, 0]).to_hex().hex

    derivative2 = DerivativeEntityGroupDecorator(group, EntityProperty.DISPLACEMENT,
                                               EntityProperty.FORCE)
    derivative2.color_line = Colors.RGBColor([255, 0, 0]).to_hex().hex

    group_plotter.add_entity_group(group)

    plotter = ConcreteEntityGroupPlotter()
    plotter.add_entity_group(derivative1)
    plotter.add_entity_group(derivative2)
    plotter.plot_added_groups(EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    # group_plotter.plot_entities_in_group(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    # group = DerivativeEntityGroupDecorator(group, EntityProperty.DISPLACEMENT,
    #                                            EntityProperty.FORCE)

    # group_plotter.plot_entities_in_group(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    # group_plotter.add_entity_group(group)
    group_plotter.plot_added_groups(EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    import sys

    sys.exit(0)

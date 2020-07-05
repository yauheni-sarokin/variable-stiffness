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
    voltage_group = 1
    group = group.children[1]

    group = group_creator.divide_entities_by_slope(group)

    group = ColorEntityGroupDecorator(group)

    group_plotter.plot_children(group, EntityProperty.TIME, EntityProperty.CURRENT)

    group = CutChildrenEntityGroupDecorator(group, end_cut=2, start_cut=20)

    group = AveragingEntityGroupDecorator(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    group_plotter.plot_entities_in_group(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    import sys

    sys.exit(0)

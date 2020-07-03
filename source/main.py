from tools_implementation import *
from math_tool import *

if __name__ == '__main__':
    file = "../testdata/varstif9/0v_to_-2V_200mV_10mA_5min_step_plain_side.txt"
    file_reader = ConcreteFileReader(file)
    content = file_reader.parse_file_content()
    group_from_content = content.get_entity_group_from_content()

    group_creator = ConcreteEntityGroupCreator()
    group_plotter = ConcreteEntityGroupPlotter()

    # group_plotter.plot_group(group_from_content, EntityProperty.TIME, EntityProperty.VOLTAGE)

    group = group_creator.divide_entities_by_voltage(group_from_content)

    group = ColorEntityGroupDecorator(group)

    group = CutChildrenEntityGroupDecorator(group, end_cut=2, start_cut=1)

    group = group.children[2]

    group = group_creator.divide_entities_by_slope(group)

    group = CutChildrenEntityGroupDecorator(group, start_cut=50)

    group = ColorEntityGroupDecorator(group)

    group = AveragingEntityGroupDecorator(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    print(group)

    group_plotter.plot_group(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    # group_plotter.plot_groups(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

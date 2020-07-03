from tools_implementation import *
from math_tool import *

if __name__ == '__main__':
    file = "../testdata/from_-2V_to_2V_400mV_1mA.txt"
    file_reader = ConcreteFileReader(file)
    content = file_reader.parse_file_content()
    group_from_content = content.get_entity_group_from_content()

    # print(group_from_content)

    entity_group_creator = ConcreteEntityGroupCreator()

    group_from_content = entity_group_creator.divide_entities_by_voltage(group_from_content)

    print(group_from_content)

    content_children = group_from_content.children

    # for i, content_child in enumerate(content_children):
    #     print(f"++++++++++++++++++++++++++++{i}")
    #     print(content_child)

    # take one entity from the list
    to_take = 14
    child_to_take = content_children[to_take]

    # print(child_to_take)

    entity_group_by_slope = entity_group_creator.divide_entities_by_slope(child_to_take)

    # print(entity_group_by_slope)

    # print(entity_group_by_slope.children[11])

    plotter: EntityGroupPlotter = ConcreteEntityGroupPlotter()

    # plotter.add_entity_group(entity_group_by_slope.children[11])

    # plotter.plot_group(entity_group_by_slope.children[12], EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    decorated_group = ColorEntityGroupDecorator(entity_group_by_slope, Colors.ColorGradients.BY_DESIGN)

    # print(decorated_group)

    # plotter.plot_group(decorated_group.children[20], EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    decorated_group = CutChildrenEntityGroupDecorator(decorated_group, 80)

    tool = MathTool()
    averaging = tool.make_averaging(decorated_group.children, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    entities = averaging.entities
    # print()

    plotter.add_entity_groups(decorated_group.children)
    plotter.plot_groups(EntityProperty.TIME, EntityProperty.CURRENT)
    plotter.plot_groups(EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    plotter.plot_group(averaging, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

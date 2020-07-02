from tools_implementation import *

if __name__ == '__main__':
    file = "../testdata/0v_to_-2V_250mV_1mA_1_30min_step_plain_side.txt"
    file_reader = ConcreteFileReader(file)
    content = file_reader.parse_file_content()
    group_from_content = content.get_entity_group_from_content()

    print(group_from_content)

    entity_group_creator = ConcreteEntityGroupCreator()

    group_from_content = entity_group_creator.divide_entities_by_voltage(group_from_content)

    print(group_from_content)

    content_children = group_from_content.children

    #take one entity from the list
    to_take = 3
    child_to_take = content_children[to_take]

    print(child_to_take)


    entity_group_by_slope = entity_group_creator.divide_entities_by_slope(child_to_take)

    print(entity_group_by_slope)

    print(entity_group_by_slope.children[11])

    plotter: EntityGroupPlotter = ConcreteEntityGroupPlotter()

    # plotter.add_entity_group(entity_group_by_slope.children[11])

    # plotter.plot_group(entity_group_by_slope.children[12], EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    color_decorated_group = ColorEntityGroupDecorator(entity_group_by_slope, Colors.ColorGradients.BY_DESIGN)

    cut_group_decorated = CutChildrenEntityGroupDecorator(color_decorated_group, start_cut=10, end_cut=10)

    print(color_decorated_group)

    # plotter.plot_group(decorated_group.children[100], EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    plotter.add_entity_groups(cut_group_decorated.children)
    # plotter.plot_groups(EntityProperty.DISPLACEMENT, EntityProperty.FORCE)
    plotter.plot_groups(EntityProperty.TIME, EntityProperty.CURRENT)

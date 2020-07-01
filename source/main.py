from tools_implementation import *

if __name__ == '__main__':
    print("Hello world, Im created")

    file = "../testdata/0v_to_2V_250mV_1mA_1_30min_step_plain_side.txt"

    file_reader = ConcreteFileReader(file)

    content = file_reader.parse_file_content()

    group_from_content = content.get_entity_group_from_content()

    print(f"Total amount of entities : {len(group_from_content.entities)}")

    entity_group_creator = ConcreteEntityGroupCreator()

    group_from_content = entity_group_creator.divide_entities_by_voltage(group_from_content)

    print(f"Divide this group by voltages \n"
          f"Now this group has children : {group_from_content.has_children} \n"
          f"And how many : {len(group_from_content.children)} \n")

    content_children = group_from_content.children

    for child in content_children:
        print(f"{child.entity_property.value['name']} {child.property_value} "
              f"{len(child.entities)} has parent : {child.has_parent}"
              f" has children : {child.has_children}")

    to_take_group = 2

    print(f" Take child group number {to_take_group} with "
          f"{len(group_from_content.children[to_take_group].entities)}\n"
          f" and voltage {group_from_content.children[to_take_group].property_value}")

    child_group = group_from_content.children[to_take_group]

    group_by_slope = entity_group_creator.divide_entities_by_slope(child_group,
                                                                   EntityProperty.SLOPE_UP)

    print(f"How many sloper are {len(group_by_slope.children)}")

    plotter: EntityGroupPlotter = ConcreteEntityGroupPlotter()
    #
    # plotter.add_entity_group(group_by_slope.children[10])
    # plotter.add_entity_group(group_by_slope.children[20])
    # plotter.add_entity_group(group_by_slope.children[30])

    plotter.add_entity_groups(group_by_slope.children)

    plotter.plot_groups(EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

"""    


    entities_by_voltage = entity_group_creator.divide_entities_by_voltage()

    print(f"How many groups with entities by voltage : {(len(entities_by_voltage))}")

    entity_group = entities_by_voltage[1]

    print(f"How many entities in one group by voltage: {len(entity_group.entities)}")

    entities_group_creator = ConcreteEntityGroupCreator(entity_group.entities)

    entity_property = entity_group.entity_property
    value = entity_group.property_value

    entities_by_slope = entities_group_creator.divide_entities_by_slope(entity_property, value)

    print(f"How many groups by slopes are in one group by voltage: {len(entities_by_slope)}")

    plotter: EntityGroupPlotter = ConcreteEntityGroupPlotter()

    plotter.add_entity_groups(entities_by_slope)

    plotter.plot_groups(EntityProperty.TIME, EntityProperty.CURRENT)
"""

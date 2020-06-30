from tools_implementation import *

if __name__ == '__main__':
    print("Hello world, Im created")

    file = "../testdata/0v_to_2V_250mV_1mA_1_30min_step_plain_side.txt"

    file_reader = ConcreteFileReader(file)

    content = file_reader.parse_file_content()

    entities_from_content = content.get_entities_from_content()

    print(f"Total amount of entities : {len(entities_from_content)}")

    entity_group_creator = ConcreteEntityGroupCreator(entities_from_content)

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

    # plotter.plot_group(entities_by_slope[20], EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    # plotter.add_entity_group(entities_by_slope[10])
    # plotter.add_entity_group(entities_by_slope[11])
    # plotter.add_entity_group(entities_by_slope[12])

    plotter.add_entity_groups(entities_by_slope)

    plotter.plot_groups(EntityProperty.TIME, EntityProperty.CURRENT)

    # plotter.plot_group(entities_by_voltage[3], EntityProperty.TIME, EntityProperty.CURRENT)

    # without_division = entity_group_creator.get_entities_groups_without_division()

    # print(type(entities_by_voltage[3]))
    # print(type(without_division))

    # plotter.plot_group(without_division, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)
    # plotter.plot_group(without_division, EntityProperty.TIME, EntityProperty.CURRENT)

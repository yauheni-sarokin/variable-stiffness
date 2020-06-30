from tools_implementation import *

if __name__ == '__main__':
    print("Hello world, Im created")

    file = "../testdata/0v_to_-2V_250mV_1mA_1_30min_step_plain_side.txt"

    file_reader = ConcreteFileReader(file)

    content = file_reader.parse_file_content()

    entities_from_content = content.get_entities_from_content()

    print(f"Total amount of entities : {len(entities_from_content)}")

    entity_group_creator = ConcreteEntityGroupCreator(entities_from_content)

    entities_by_voltage = entity_group_creator.divide_entities_by_voltage()

    print(f"How many groups with entities by voltage : {(len(entities_by_voltage))}")

    # entities = entities_by_voltage[3].entities


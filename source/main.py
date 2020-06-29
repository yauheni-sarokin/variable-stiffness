from tools_interface import *
from tools_implementation import *

if __name__ == '__main__':
    print("Hello world, Im created")

    file = "../testdata/2v_to_-2V_250mV_1mA_3min_step_plain_side.txt"

    file_reader = ConcreteFileReader(file)

    content = file_reader.parse_file_content()

    entities_from_content = content.get_entities_from_content()

    print(len(entities_from_content))

    print(entities_from_content[0].voltage)

    entity_group_creator = ConcreteEntityGroupCreator(entities_from_content)

    entities_by_voltage = entity_group_creator.divide_entities_by_voltage()

    print(len(entities_by_voltage))

    entities = entities_by_voltage[3].entities
    print(len(entities))

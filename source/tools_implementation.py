from tools_interface import *


class ConcreteEntity(Entity):
    pass


class ConcreteContent(Content):

    def __init__(self, content: List[str]) -> None:
        content.remove(content[0])
        self._content = content

    def get_entities_from_content(self) -> List[Entity]:
        entities_list: List[Entity] = [Entity]

        for line in self._content:
            # line is a string that contains data, so string have to be divided
            data = line.strip().replace(',', '.').split("\t")
            # first row is a voltage, float
            voltage = float(data[0].strip())
            # second row is a current, uA, float
            current = float(data[1].strip())
            # third row is a force sensor data, uN, float
            force = float(data[2].strip())
            # 4th row is a displacement in mm, float
            displacement = float(data[3].strip())
            # 5th row is a time in ms, int
            time = int(data[4].strip())
            # 6th row is a number of cycle, int
            cycle = int(data[5].strip())

            entity = ConcreteEntity(voltage, current, force, displacement, time, cycle)
            entities_list.append(entity)

        return entities_list


class ConcreteFileReader(FileReader):

    def __init__(self, file: str) -> None:
        # todo add exception handler
        self._file = file

    def parse_file_content(self) -> Content:
        # Set file with test data to read, r means read
        file_to_read = open(self._file, "r", encoding="latin-1")

        content = file_to_read.readlines()

        # Close file after reading
        file_to_read.close()
        return ConcreteContent(content)

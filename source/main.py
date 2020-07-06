from tools_implementation import *

if __name__ == '__main__':
    #read file and parse groups
    file = "../testdata/varstif9/0v_to_-2V_200mV_10mA_5min_step_plain_side.txt"
    #create file reader
    group = ConcreteFileReader(file).parse_entity_groups_from_file()
    #create group plotter and creator
    plotter = ConcreteEntityGroupPlotter()
    creator = ConcreteEntityGroupCreator()
    #Plot entities in this group to see current time cure
    # plotter.plot_entities_in_group(group, EntityProperty.TIME, EntityProperty.CURRENT)

    #divede by groups by voltage
    group = creator.divide_entities_by_voltage(group)

    group = CutChildrenEntityGroupDecorator(group, end_cut=3)

    #now we have several groups by voltage
    groups_by_voltage = group.children

    #create groups by slope
    groups: List[EntityGroup] = []
    for group in groups_by_voltage:
        by_slope = creator.divide_entities_by_slope(group)
        #cut some groups where current is very high
        by_slope = CutChildrenEntityGroupDecorator(by_slope, start_cut=20)
        groups.append(by_slope)

    averaged_groups: List[EntityGroup] = []

    #get averaging for each group
    for group in groups:
        group = AveragingEntityGroupDecorator(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)
        group = CutEntitiesByXAxisDecorator(group, EntityProperty.DISPLACEMENT, x_start=0.05, x_end=0.2)
        group = LinearInterpolationEntityGroupDecorator(group)
        group = DerivativeEntityGroupDecorator(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)
        averaged_groups.append(group)


    plotter.add_entity_groups(averaged_groups)
    plotter.plot_added_groups(EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    # plotter.plot_entities_in_group(averaged_groups[3], EntityProperty.DISPLACEMENT, EntityProperty.FORCE)
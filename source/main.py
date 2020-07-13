from tools_implementation import *

if __name__ == '__main__':
    # read file and parse groups
    file = "../testdata/varstif11/0v_to_-2V_250mV_1mA_1_30min_step_plain_side.txt"
    # create file reader
    group = ConcreteFileReader(file).parse_entity_groups_from_file()
    # create group plotter and creator
    plotter = ConcreteEntityGroupPlotter()
    creator = ConcreteEntityGroupCreator()
    # Plot entities in this group to see current time cure
    # plotter.plot_entities_in_group(group, EntityProperty.TIME, EntityProperty.CURRENT)
    # divede by groups by voltage
    group = creator.divide_entities_by_voltage(group)

    # plotter.plot_entities_in_group(group, EntityProperty.TIME, EntityProperty.VOLTAGE)

    group = CutChildrenEntityGroupDecorator(group, end_cut=1)

    group = ColorEntityGroupDecorator(group)

    groups: List[EntityGroup] = []

    for group in group.children:
        group = creator.divide_entities_by_slope(group)
        group = CutChildrenEntityGroupDecorator(group, start_cut=15)

        group = AveragingEntityGroupDecorator(group, EntityProperty.DISPLACEMENT,
                                              EntityProperty.FORCE)

        group = CutEntitiesByXAxisDecorator(group, EntityProperty.DISPLACEMENT, x_start=0,
                                            x_end=0.03)
        group = LinearInterpolationEntityGroupDecorator(group)
        print(group)
        group = EntitiesToZeroAxisDecorator(group, EntityProperty.DISPLACEMENT, EntityProperty.FORCE)
        # group = DerivativeEntityGroupDecorator(group, EntityProperty.DISPLACEMENT,
        #                                        EntityProperty.FORCE)
        groups.append(group)

    # assign to group a new children
    # group.children = groups

    plotter.add_entity_groups(groups)
    # todo plot with colorbar
    # plotter.plot_added_groups_with_cb(EntityProperty.DERIVATIVE_X, EntityProperty.DERIVATIVE_Y)
    plotter.plot_added_groups_with_cb(EntityProperty.DISPLACEMENT, EntityProperty.FORCE)

    import sys

    sys.exit(0)

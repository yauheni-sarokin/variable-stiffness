#####################################################
#The same as tools before but othe aproaches
#####################################################

from enum import Enum
import matplotlib.pyplot as plt
import colorgradients as cg
#import statistic tools
from statistics import stdev, mean
import numpy as np

from scipy.signal import savgol_filter

#Color printing
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_color(message, color = bcolors.WARNING):
    print(color + message + bcolors.ENDC)
# Enumeration of entity data
# from https://docs.python.org/3.4/library/enum.html
Data = Enum('Data', 'voltage, current, force, displacement, time, cycle')

#Define class entity
#In tis class we store information about one row
class Entity:
    #Initiate entity class that contain each cycle data
    def __init__(self, voltage, current, force, displacement, time, cycle):
        self.voltage = voltage
        self.current = current
        self.force = force
        self.displacement = displacement
        self.time = time
        self.cycle = cycle

    def getVoltage(self):
        return self.voltage

    def getCurrent(self):
        return self.current

    def getForce(self):
        return self.force

    def getDisplacement(self):
        return self.displacement

    def getTime(self):
        return self.time

    def getCycle(self):
        return self.cycle

    def getValue(self, dataValue):
        if dataValue == Data.voltage: return self.voltage
        elif dataValue == Data.current: return self.current
        elif dataValue == Data.force: return self.force
        elif dataValue == Data.displacement: return self.displacement
        elif dataValue == Data.time: return self.time
        elif dataValue == Data.cycle: return self.cycle

#get data from line for entity generation
#content is array read from file, line is number of line and data is enum
def get_data(content, line, data):
    row = content[line].strip().replace(',', '.').split("\t")
    # first row is a voltage, float
    if data == Data.voltage:
        return float(row[0].strip())
    # second row is a current, uA, float
    elif data == Data.current:
        return float(row[1].strip())
    # third row is a force sensor data, uN, float
    elif data == Data.force:
        return float(row[2].strip())
    # 4th row is a displacement in mm, float
    elif data == Data.groups_by_displacement:
        return float(row[3].strip())
    # 5th row is a time in ms, int
    elif data == Data.time:
        return int(row[4].strip())
    # 6th row is a number of cycle, int
    elif data == Data.cycle:
        return int(row[5].strip())
#contentrow is 1 row from content
def get_data(contentrow, data):
    row = contentrow.strip().replace(',', '.').split("\t")
    # first row is a voltage, float
    if data == Data.voltage:
        return float(row[0].strip())
    # second row is a current, uA, float
    elif data == Data.current:
        return float(row[1].strip())
    # third row is a force sensor data, uN, float
    elif data == Data.force:
        return float(row[2].strip())
    # 4th row is a displacement in mm, float
    elif data == Data.displacement:
        return float(row[3].strip())
    # 5th row is a time in ms, int
    elif data == Data.time:
        return int(row[4].strip())
    # 6th row is a number of cycle, int
    elif data == Data.cycle:
        return int(row[5].strip())

# Reads file and returns content
def get_content_from_file(file):
    # Set file with test data to read, r means read
    fileToRead = open(file, "r", encoding="latin-1")
    content = fileToRead.readlines()
    # Close file after reading
    fileToRead.close()
    return content

# Create entity that contains set of data
def create_entity(content, line):
    voltage = get_data(content, line, Data.voltage)
    current = get_data(content, line, Data.current)
    force = get_data(content, line, Data.force)
    displacement = get_data(content, line, Data.displacement)
    time = get_data(content, line, Data.time)
    cycle = get_data(content, line, Data.cycle)
    return Entity(voltage, current, force, displacement, time, cycle)

def create_entity(contentrow):
    voltage = get_data(contentrow, Data.voltage)
    current = get_data(contentrow, Data.current)
    force = get_data(contentrow, Data.force)
    displacement = get_data(contentrow, Data.displacement)
    time = get_data(contentrow, Data.time)
    cycle = get_data(contentrow, Data.cycle)
    return Entity(voltage, current, force, displacement, time, cycle)

#function returns list of entities
def get_entities_from_content(content):
    # remove from content header
    header = content[0]
    content.remove(header)
    # create list with all the possible entities
    entities = list()
    for element in content:
        entities.append(create_entity(element))
    return entities

#####################################################
#Entities are divided by groups in entity classes
#So each class by voltage contain voltage information
# and entities of the same voltage
#####################################################
class EntityGroup():
    def __init__(self):
        pass
#####################################################
#Entities group by voltage will be later inheriatant
# of voltage class
#####################################################
class EntityGroupByVoltage():
    '''
    This class contain information of voltage for
    group of entities and the group may be divided
    into displacement, but not intentionaly.
    '''
    def __init__(self, voltage, entities):
        self.voltage = voltage
        self.entities = entities
        pass

    def get_voltage(self):
        return self.voltage

    def get_entities(self):
        return self.entities

    '''
    this method sets to the class list with objects of 
    DisplacementGroupEntities
    '''
    def set_entities_groups_by_displacement(self,
                                            entities_groups_by_displacement):
        self.entities_groups_by_displacement = entities_groups_by_displacement

    def get_entities_groups_by_displacement(self):
        return self.entities_groups_by_displacement


#Each entity have to be devided into smaller groups with the same applied voltage
# voltagesGroups is an array with voltages of the group
# groupOfEntities contains an array with all entities of the same group ov voltages

#This function takes one long list of entities and divede them
#into array with two lists, group with same voltages and group
#of entities that belong to this group of voltage
def get_entities_groups_by_voltage(entities):
    voltagesGroups, groupOfEntities = [], []
    # iterator
    iter = 0
    currentV = round(entities[0].getVoltage(), 1)
    groupOfEntities.append([])
    voltagesGroups.append(currentV)

    for entity in entities:
        voltage = entity.getVoltage()
        # rounded voltage
        rV = round(voltage, 1)
        if rV == currentV:
            groupOfEntities[iter].append(entity)
        else:
            iter += 1
            currentV = rV
            voltagesGroups.append(rV)
            groupOfEntities.append([])
            groupOfEntities[iter].append(entity)

    groups_to_return = []
    for voltage, group in zip(voltagesGroups, groupOfEntities):
        #####################################################
        # Here we a creating groups fof entities and we have
        # to filter by amount of entities, we cant plot
        # if there only one entity, lets filter by 100
        #####################################################
        if len(group) > 100:
            entity_group_by_voltage = EntityGroupByVoltage(voltage, group)
            groups_to_return.append(entity_group_by_voltage)
    return groups_to_return

#Class Displacement entity contains voltage, slope up and slope down
#entities of the same loading cycle
Slope = Enum('Slope', 'up, down')
#####################################################
#This class contains displacement group: its voltage
# slope up and slope down list
#####################################################
class DisplacementGroupEntities:
    '''This class serves to contain only entities
    that belongs to slope up and slope down within
    one cycle'''
    #initialize one displacement entity
    def __init__(self):
        #Voltage from the group of voltages
        #self.voltage = voltage
        #list of entities slope up direction
        self.slopeUp = []
        #list of entities slope down direction
        self.slopeDown = []

    '''def getVoltage(self):
        return self.voltage'''

    def appendSlopeUp(self, entity):
        self.slopeUp.append(entity)

    def appendSlopeDown(self, entity):
        self.slopeDown.append(entity)

    def getSlopeUp(self): return self.slopeUp
    def getSlopeDown(self): return self.slopeDown
    def getSlope(self, slope):
        if slope == Slope.up: return self.slopeUp
        elif slope == Slope.down: return self.slopeDown
#####################################################
#This function accepts list of entities and return
# list divided into slope up entities
#####################################################

def get_entities_groups_by_displacement(entities):
    # List that contains displecements
    # typically - with the same voltage
    # up and down curves
    groups_by_displacement = [DisplacementGroupEntities()]

    iter, prevDisp, slope = 0, 0.0, True
    for entity in entities:
        # if displacement is higher than the previous one and slope is up
        # then the entities belong to the same group of loading curve
        if entity.getDisplacement() > prevDisp and slope:
            # chang prev disp
            prevDisp = entity.getDisplacement()

            groups_by_displacement[iter].appendSlopeUp(entity)
        # if displacement is higher than the previous but the slope is down
        # we start new cycle of loading after unloading
        # here we create a new displacement group and increase iteration
        elif entity.getDisplacement() > prevDisp and not slope:
            # chang prev disp ,iterator increment and slope change
            prevDisp = entity.getDisplacement()
            iter += 1
            slope = True

            dGE = DisplacementGroupEntities()
            dGE.appendSlopeUp(entity)
            groups_by_displacement.append(dGE)
        # if displacement is lower than the previous one and the slope is
        # up then we are going we start unloading curve
        elif entity.getDisplacement() < prevDisp and slope:
            # chang prev disp and slope
            prevDisp = entity.getDisplacement()
            slope = False

            groups_by_displacement[iter].appendSlopeDown(entity)
        # if displacement is lower than the previous one and the slope is
        # down then the entities belong to the same group of loading curve
        elif entity.getDisplacement() < prevDisp and not slope:
            # chang prev disp
            prevDisp = entity.getDisplacement()

            groups_by_displacement[iter].appendSlopeDown(entity)
    #Return list with groups of entities, belong to class DisplacementGroupEntities
    return groups_by_displacement

'''
Here I describe the logic above:
1. get content from file

content = get_content_from_file(file)

2. get list of entities from content

list [Entity] entities = get_entities_from_content(content)

3. get entities group by voltage,
the class contain voltage and list of entities
that belongs to that voltage
list of elements belong to this class: EntityGroupByVoltage

list [EntityGroupByVoltage] groups_by_voltage = 
                            get_entities_groups_by_voltages(entities)

Now we have divided entities into groups by voltage but without
any division by displacement 

4.for Each group of voltage, take entities, divide into displacements, and set
 
for voltage_group in [EntityGroupByVoltage] groups_by_voltage:
    list [Entity] entities = voltage_group.get_entities()
    list [DisplacementGroupEntities] groups_by_displacement = 
                            get_entities_groups_by_displacement(entities)
    
    voltage_group.set_entities_groups_by_displacement(groups_by_displacement)
    
Now we havelist of entities groups by voltage with groups by displacement 

'''

#####################################################
# This function allows as to obtain groups
# of entities with embedded division by voltage
# and by slope
#####################################################

def get_entities_groups_by_voltage_by_displacement_from_entities(entities):
    '''This function takes all the entities and returns
    list with groups by voltage class [EntityGroupByVoltage]
    that contains already list with class [DisplacementGroupEntities]'''

    #list [EntityGroupByVoltage]
    groups_by_voltage = get_entities_groups_by_voltage(entities)
    for group_by_voltage in groups_by_voltage:
        entities = group_by_voltage.get_entities()
        #list [DisplacementGroupEntities]
        group_by_displacement = get_entities_groups_by_displacement(entities)
        group_by_voltage.set_entities_groups_by_displacement(
            group_by_displacement
        )
    #return list [EntityGroupByVoltage]
    return groups_by_voltage
#####################################################
# function returns values of displacement/voltages
# as array
#####################################################

def entities_values_to_array(entities, value):
    valuesArray = []
    for entity in entities:
        get_value = entity.getValue(value)
        valuesArray.append(get_value)
    return valuesArray

#####################################################
# This function assumes that between two points in
# plane exists linear function and return any y for
# any x in range
#####################################################
def line_function_plotter(xset, yset, x):
    #y0 = ax0 + b, y1 = ax1 + b
    #a = (y0 - y1)/(x0 - x1)
    #b = y0 - a*x0
    #Вначале определим диапозон
    min_x, max_x, min_y, max_y = min(xset), max(xset), min(yset), max(yset)
    #y to return
    y = 0
    #Thow exception if x is out of range
    if x > max_x or x < min_x: raise Exception("Your x = {} value is out of [xmin : {}, xmax : {}]"
                                               " range".format(x, min_x, max_x))
    else:
        for index, x_from_set in enumerate(xset):
            if x == x_from_set:
                y = yset[index]
                break
            elif xset[index] < x < xset[index + 1]:
                x0, x1, y0, y1 = xset[index], xset[index+1], yset[index], yset[index+1]
                a = (y0 - y1)/(x0 - x1)
                b = y0 - a*x0
                y = a*x + b
                break
    return y
#####################################################
# This function create a new array with float min,
# max and int steps
#####################################################
def frange(min, max, steps):
    interval = (max - min) / (steps - 1)
    array = [min]
    for i in range(steps - 1):
        array_interval = array[-1] + interval
        array.append(array_interval)

    if array[-1] > max: array[-1] = round(array[-1], 3)

    return array
#####################################################
# This function checks if float belongs to range
# between min and max in array
#####################################################

def belongs_to(x, array):
    return array[0] < x < array[-1]

#####################################################
# This function accepts voltage_group_by_displacement
# - array with displacement group entities,
# steps - amount of intervals, slope - up or down,
# function returns array of x set data and aray with
# corresponding sets of y, eah set of y correspond to
# each x
# Function accept class DisplacementGroupEntities:
# returns x force y displacement
#####################################################

def get_x_y_sets_from_groups_by_displacement(displacement_group_of_entities, steps, slope):
    # First approximation is that we can have average xmin and xmax from all the functions
    x_min_avg_set, x_max_avg_set = [], []
    # Iterate all the gropus with the same voltage that contain entities with slope up
    # /down and saves all the xmin and xmax to arrays
    for group in displacement_group_of_entities:
        # x and y set arrays as displacement and force
        xset_original = entities_values_to_array(group.getSlope(slope), Data.displacement)
        x_min, x_max = xset_original[0], xset_original[-1]
        x_min_avg_set.append(x_min)
        x_max_avg_set.append(x_max)
    # finding average x and y min
    x_min_avg = sum(x_min_avg_set) / len(x_min_avg_set)
    x_max_avg = sum(x_max_avg_set) / len(x_max_avg_set)

    # Now we can build a set that will contain all the possible x in a set
    # within xmin and xmax average
    x_set = frange(x_min_avg, x_max_avg, steps)
    y_set = []
    for x in x_set:
        y_set.append([])

    # Here all y's are added as an arrays list y_set and have one corresponding x_set
    for group in displacement_group_of_entities:
        x_disp_array = entities_values_to_array(group.getSlope(slope), Data.displacement)
        y_force_array = entities_values_to_array(group.getSlope(slope), Data.force)
        for x_from_set, y_array_from_set in zip(x_set, y_set):
            belongs = belongs_to(x_from_set, x_disp_array)
            if belongs:
                y = line_function_plotter(x_disp_array, y_force_array, x_from_set)
                y_array_from_set.append(y)

    return x_set, y_set

#####################################################
# This function calculates accepts array of float and
# returns mean and stdev
#####################################################

def get_mean_and_stdev(array):
    return mean(array), stdev(array)

#####################################################
# stdev, returns list of array ->
# [x, mean y, st dev of y]
#####################################################

def get_x_y_mean_stdev(x_set, y_set_array):
    x_y_stdev = []
    for x, y_array in zip(x_set, y_set_array):
        y_mean = mean(y_array)
        y_stdev = stdev(y_array)
        x_y_stdev.append([x, y_mean, y_stdev])
    return x_y_stdev

#####################################################
# function returns xset, mean yset, stdev yset as 3
# arrays
#####################################################

def get_x_y_mean_stdev_split_array(x_set, y_set_array):
    y_mean_list, y_stdev_list = [], []
    for x, y_array in zip(x_set, y_set_array):
        y_mean = mean(y_array)
        y_stdev = stdev(y_array)
        y_mean_list.append(y_mean)
        y_stdev_list.append(y_stdev)
    return x_set, y_mean_list, y_stdev_list

#####################################################
# function accepts array of DisplacementGroupEntities
# and plot it
# #Precision parameter - how many interval on x - axis
# accepts EntityGroupByVoltage
#####################################################
def plot_force_displacement(entity_groups_by_voltage, gradient ='standard', precision = 100):

    fig, ax = plt.subplots()

    colors = cg.get_color_gradient_array(gradient, len(entity_groups_by_voltage))
    voltages = []
    for voltage_group, color in zip(entity_groups_by_voltage, colors):
        voltage = voltage_group.get_voltage()
        voltages.append(voltage)
        displacement_groups = voltage_group.get_entities_groups_by_displacement()
        x_set, y_set_array = get_x_y_sets_from_groups_by_displacement(
            displacement_groups, precision, Slope.up
        )
        _x, _y, _stdev = get_x_y_mean_stdev_split_array(x_set, y_set_array)
        ax.plot(_x, _y, color=color)

    ax.set(xlabel='mm', ylabel='uN', title='force-displacement')

    # ===test===
    import matplotlib.colors as mcolors
    import matplotlib.cm
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    cmap, norm = mcolors.from_levels_and_colors(range(len(entity_groups_by_voltage) + 1), colors)
    sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cbar = fig.colorbar(sm, cax=cax, ticks=range(len(entity_groups_by_voltage)))
    cbar.ax.set_yticklabels(voltages)

    #plt.legend()
    #fig.savefig("result.pdf")
    plt.show()

#####################################################
# Calculates 2nd moment of inertia, b - beam widht
# h - beam thickness, im mm
#####################################################
def calculate_ii_moment_of_inertia(b, h):
    _i = (b * (h**3))/12
    return _i

#####################################################
# Calculates elastic modulus of the beam, l - length
# where force is applied, w - displacement, 
# f - force, i - 2nd moment of inertia
#####################################################
def calculate_elastic_modulus(l, i, f, w):
    modulus = (2/3)*((l**3)/(i))*(f/w)
    return modulus

#####################################################
# Calculates elastic modulus of the beam knowing
# force - displacement derivative function,
# l - length where force is applied, w - displacement
#, f - force, i - 2nd moment of inertia
#####################################################

def calculate_elastic_modulus_with_derivative(l, i, df_dw):
    modulus = (2/3)*((l**3)/(i))*(df_dw)
    return modulus

#####################################################
# This function accepts x, y set of force
# displacement data, and constants l, i
# x is displacement in mm and y is force in uN
# l is given in mm, i is also in mm 
# retirns modulus in MPa
#####################################################
def force_displacement_to_modulus_displacement(_x, _y, l, i):
    #convert l to m
    l_m = l/1e3
    #convert i to m4
    i_m = i/1e12

    modulus = []

    for x, y in zip(_x, _y):
        #convert un to N
        force_y = y/1e6
        #convert displacement from mm to m
        displacement_x = x/1e3
        
        #calculate modulus f Pa
        #calculate_elastic_modulus(l, i, f, w):
        _E = calculate_elastic_modulus(l_m, i_m, force_y, displacement_x) / 1e6
        #print(_E)

        modulus.append(_E)

    return modulus

#####################################################
# This function accepts x, y - as DERIVATIVE of df/dx
# 
# displacement data, and constants l, i
# x is displacement in mm and y is force in uN
# l is given in mm, i is also in mm 
# retirns modulus in MPa
#####################################################
def force_displacement_to_modulus_displacement_with_derivative(_x, _dy_dx, l, i):
    #convert l to m
    l_m = l/1e3
    #convert i to m4
    i_m = i/1e12

    modulus = []

    for x, derivative in zip(_x, _dy_dx):
        #convert uN/mm to N/m
        der = derivative/1e3
        #convert displacement from mm to m
        #displacement_x = x/1e3
        
        #calculate modulus MPa
        #calculate_elastic_modulus_with_derivative(l, i, df_dw):
        _E = calculate_elastic_modulus_with_derivative(l_m, i_m, der) / 1e6
        #print(_E)

        modulus.append(_E)

    return modulus

#####################################################
# Similar to previous plot function, plot stress
# strain, l, b, h assumed to be in mm
#####################################################
def plot_modulus_displacement(entity_groups_by_voltage, l, b, h, gradient ='standard', precision = 100):

    fig, ax = plt.subplots()

    colors = cg.get_color_gradient_array(gradient, len(entity_groups_by_voltage))
    voltages = []
    for voltage_group, color in zip(entity_groups_by_voltage, colors):
        voltage = voltage_group.get_voltage()
        voltages.append(voltage)
        displacement_groups = voltage_group.get_entities_groups_by_displacement()
        x_set, y_set_array = get_x_y_sets_from_groups_by_displacement(
            displacement_groups, precision, Slope.up
        )
        _x, _y, _stdev = get_x_y_mean_stdev_split_array(x_set, y_set_array)

        #####################################################
        # Calculate 2nd moment of inertia
        #####################################################

        _i = calculate_ii_moment_of_inertia(b, h)

        #####################################################
        # Calculate modulus
        #####################################################
        _E = force_displacement_to_modulus_displacement(_x, _y, l, _i)

        ax.plot(_x, _E, color=color)

    ax.set(xlabel='mm', ylabel='MPa', title='stress-strain')

    # ===test===
    import matplotlib.colors as mcolors
    import matplotlib.cm
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    cmap, norm = mcolors.from_levels_and_colors(range(len(entity_groups_by_voltage) + 1), colors)
    sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cbar = fig.colorbar(sm, cax=cax, ticks=range(len(entity_groups_by_voltage)))
    cbar.ax.set_yticklabels(voltages)

    #plt.legend()
    #fig.savefig("result.pdf")
    plt.show()

#####################################################
# Function returns smoother function from x, y set
#####################################################
def function_smoother(x_set, y_set):

    pass

#####################################################
# Function solves derivative!
# derivative f(x) = dx/dy
# function accepts x set, y set, amount of points for
# smoothening, the higher the amount of points -
# the higher precision + lower smoothness
# my smooth derivative algorithm:
# -> x, y set function divide into n - interval
# each n - interval divide into m intervals and
# find derivative for each m interval and after
# derivative for n is average between m intervals
#####################################################
def function_derivative(x_set, y_set, n_intervals = 30, m_intervals = 10):
    #[y] line_function_plotter(xset, yset, x):
    #range from minim to max x
    x_min, x_max = x_set[0], x_set[-1]
    #divide range into n intervals
    #x_range = x_max - x_min
    #x_points =
    x_n_array = np.linspace(x_min, x_max, n_intervals)

    x_set_to_return = []
    dy_dx_set_to_return = []

    #get derivative between x_0 and x_1
    for n in range(len(x_n_array) - 1):
        x_n_0 = x_n_array[n]
        #print(str(x_n_0))
        x_n_1 = x_n_array[n+1]

        #we can divide this array in m intervals
        x_m_array = np.linspace(x_n_0, x_n_1, m_intervals)

        m_derivaites = []
        #x_points = []
        for m in range(len(x_m_array) - 1):
            x_m_0 = x_m_array[m]
            #print_color('x_m_0 = {}'.format(x_m_0))
            x_m_1 = x_m_array[m + 1]
            #todo BECAUSE OF INTERNAL MATEMATICS SOMEHOW OUT OF RANGE
            # Therefore I'm mulyiplying fuinction to 0.99999999...
            dx = (x_m_1 - x_m_0) * (1 - 1/1e5)
            #check if is not out of range
            if m is 0 and n is 0:
                y_m_1 = line_function_plotter(x_set, y_set, x_m_1)
                y_m_0 = line_function_plotter(x_set, y_set, x_m_0)
                dy = y_m_1 - y_m_0
                y_m_min1 = y_m_0 - dy
                x_m_min1 = x_m_0 - dx
                dy_dx = (y_m_1 - y_m_min1) / (x_m_1 - x_m_min1)
                m_derivaites.append(dy_dx)
            #elif n is len(x_n_array) - 1 and m is len(x_m_array) - 1:
            #    pass
            else:
                x_m_min1 = x_m_0 - dx
                y_m_min1 = line_function_plotter(x_set, y_set, x_m_min1)
                y_m_1 = line_function_plotter(x_set, y_set, x_m_1)

                dy_dx = (y_m_1 - y_m_min1) / (x_m_1 - x_m_min1)
                m_derivaites.append(dy_dx)
                #x_point = (x_m_0 + x_m_1) / 2
                #x_points.append(x_point)

        derivative = mean(m_derivaites) # mean derivative from m derivatives
        dy_dx_set_to_return.append(derivative)
        x_point = x_n_0 + ((x_n_1 - x_n_0) / 2)
        #print_color('x point = {} derivative = {}'.format(x_point, derivative) )
        x_set_to_return.append(x_point)

    return x_set_to_return, dy_dx_set_to_return

def plot_modulus_displacement_mock(entity_groups_by_voltage, l, b, h, gradient ='standard', precision = 100):

    fig, ax = plt.subplots()

    colors = cg.get_color_gradient_array(gradient, len(entity_groups_by_voltage))
    voltages = []
    for voltage_group, color in zip(entity_groups_by_voltage, colors):
        voltage = voltage_group.get_voltage()
        voltages.append(voltage)
        displacement_groups = voltage_group.get_entities_groups_by_displacement()
        x_set, y_set_array = get_x_y_sets_from_groups_by_displacement(
            displacement_groups, precision, Slope.up
        )
        _x, _y, _stdev = get_x_y_mean_stdev_split_array(x_set, y_set_array)

        #####################################################
        # Smoothening
        #####################################################
        #_y_filtered = savgol_filter(_y, 51, 3)

        

        # from scipy.ndimage import gaussian_filter1d
        # sigma = 1
        # _y_filtered = gaussian_filter1d(_y, sigma)
        # print_color(str(len(_y_filtered)))



        #box = np.ones(3)/3
        #_y_filtered = np.convolve(_y, box, mode='same')
        #_y_filtered = smoothList(_y)
        #####################################################
        # Smoothening
        #####################################################


        #####################################################
        # Calculate 2nd moment of inertia
        #####################################################

        _i = calculate_ii_moment_of_inertia(b, h)

        #####################################################
        # Calculate modulus
        #####################################################

        #####################################################
        # Test
        #####################################################
        '''import numpy as np
        _x_np = np.array(_x)
        _y_np = np.array(_y)
        _modulus_np = _x_np / _y_np'''

        _x_np, _dy_dx_np = function_derivative(_x, _y, 100, 50)
        #_y_filter = savgol_filter(_dy_dx_np, 51, 3)
        #box = np.ones(3)/3
        #_y_filtered = np.convolve(_dy_dx_np, box, mode='same')

        #####################################################
        # Test
        #####################################################

        #_E = force_displacement_to_modulus_displacement(_x, _y, l, _i)
        #force_displacement_to_modulus_displacement_with_derivative(_x, _dy_dx, l, i):
        _modulus = force_displacement_to_modulus_displacement_with_derivative(_x_np, _dy_dx_np, l, _i)

        ax.plot(_x_np, _modulus, color=color)

    ax.set(xlabel='mm', ylabel='MPa', title='Modulus-displacement')

    # ===test===
    import matplotlib.colors as mcolors
    import matplotlib.cm
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    cmap, norm = mcolors.from_levels_and_colors(range(len(entity_groups_by_voltage) + 1), colors)
    sm = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)

    cbar = fig.colorbar(sm, cax=cax, ticks=range(len(entity_groups_by_voltage)))
    cbar.ax.set_yticklabels(voltages)

    #plt.legend()
    #fig.savefig("result.pdf")
    plt.show()




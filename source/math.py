from typing import List

"""
Code below taken from old propgram
"""


# todo Искать ошибки и доработать, классы долнжы работать только с примитивами


def __line_function_plotter(x_set: List[float], y_set: List[float], x: float) -> float:
    """
    This function assumes that between two points in
    plane exists linear function and return any y for
    any x in range
    :param y_set:
    :param x:
    :return:
    """
    # y0 = ax0 + b, y1 = ax1 + b
    # a = (y0 - y1)/(x0 - x1)
    # b = y0 - a*x0
    # Вначале определим диапозон
    min_x, max_x, min_y, max_y = min(x_set), max(x_set), min(y_set), max(y_set)
    # y to return
    y = 0
    # Throw exception if x is out of range
    if x > max_x or x < min_x:
        raise Exception("Your x = {} value is out of [xmin : {}, xmax : {}]"
                        " range".format(x, min_x, max_x))
    else:
        for index, x_from_set in enumerate(x_set):
            if x == x_from_set:
                y = y_set[index]
                break
            elif x_set[index] < x < x_set[index + 1]:
                x0, x1, y0, y1 = x_set[index], x_set[index + 1], y_set[index], y_set[index + 1]
                a = (y0 - y1) / (x0 - x1)
                b = y0 - a * x0
                y = a * x + b
                break
    return y


def __f_range(self, minimum: float, maximum: float, steps: int) -> List[float]:
    """
    This function create a new array with float min,
    max and int steps
    :param maximum:
    :param steps:
    :return:
    """
    interval = (maximum - minimum) / (steps - 1)
    array = [minimum]
    for i in range(steps - 1):
        array_interval = array[-1] + interval
        array.append(array_interval)

    if array[-1] > maximum:
        array[-1] = round(array[-1], 3)

    return array


def __belongs_to(x: float, array: List[float]) -> bool:
    """
    This function checks if float belongs to range
    between min and max in array
    :param array:
    :return:
    """
    return array[0] < x < array[-1]

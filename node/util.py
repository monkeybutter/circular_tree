import numpy as np

def origin_remover(bounds):
    new_bounds = []
    init = None

    for bound in bounds:
        if bound[1] == 360.0:
            init = bound[0]
        elif bound[0] == 0.0 and init is not None:
            new_bounds.append([init, bound[1]])
            init = None
        else:
            new_bounds.append(bound)

    return new_bounds


def get_outter(values, bound):
    if bound[1] < values[0] or bound[0] > values[1]:
        return [bound]
    else:
        new_bound = []
        if bound[0] < values[0]:
            new_bound.append([bound[0], values[0]])
        if bound[1] > values[1]:
            new_bound.append([values[1], bound[1]])
        return new_bound

def get_inner(values, bound):

    if not(bound[1] < values[0] or bound[0] > values[1]):
        if bound[0] > values[0]:
            if bound[0] != values[1]:
                return [[bound[0], min(bound[1], values[1])]]
            else:
                return []
        else:
            return [[values[0], min(bound[1], values[1])]]

    else:
        return []


def bound_generator(data, index, bounds, circular=False):

    if circular:
        #First cicular split
        if bounds == [[-np.inf, np.inf]]:
            return [[data[index[1]], data[index[0]]]], [[data[index[0]], data[index[1]]]]
        else:
            for bound in bounds:
                if bound[0] > bound[1]:
                    outter = []
                    inner = []
                    print(data[index[0]], data[index[1]], bound)
                    for split in get_outter((data[index[0]], 360.0), [bound[0], 360.0]):
                        outter.append(split)
                    for split in get_outter((0.0, data[index[1]]), [0.0, bound[1]]):
                        outter.append(split)
                    for split in get_inner((data[index[0]], 360.0), [bound[0], 360.0]):
                        inner.append(split)
                    for split in get_inner((0.0, data[index[1]]), [0.0, bound[1]]):
                        inner.append(split)
                    print(outter, origin_remover(inner))
                    return outter, origin_remover(inner)

                else:
                    outter = []
                    inner = []
                    for split in get_outter((data[index[0]], data[index[1]]), bound):
                        outter.append(split)
                    for split in get_inner((data[index[0]], data[index[1]]), bound):
                        inner.append(split)
                    return outter, inner

    else:
        if not isinstance(index, list):
            return get_outter((-np.inf, data[index]), bounds[0]), get_inner((-np.inf, data[index]), bounds[0])

        else:
            outter = []
            inner = []
            for bound in bounds:
                for split in get_outter((data[index[0]], data[index[1]]), bound):
                    outter.append(split)
                for split in get_inner((data[index[0]], data[index[1]]), bound):
                    inner.append(split)

            return outter, inner



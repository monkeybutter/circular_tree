import numpy as np

def is_in_bounds(value, bound):
    return bound[0] <= value < bound[1]

def is_in_bounds_cir(value, bound):
    if bound[0] < bound[1]:
        return bound[0] <= value < bound[1]

    else:
        return bound[0] <= value <= 360.0 or 0.0 <= value <= bound[1]


def bound_generator_lin(data, split_index, bounds):
    outer = True

    if split_index[0] == 0:
        outer = False

    inner_bounds, outer_bounds = [], []

    split_value1 = data[split_index[0]]
    split_value2 = data[split_index[1]]

    for bound in bounds:

        #nonlocal outer

        if outer:
            if not is_in_bounds(data[split_index[0]], bound) and not is_in_bounds(data[split_index[1]-1], bound):
                #print('{} bounds are before first split'.format(bound))
                outer_bounds.append(bound)

            else:
                if not is_in_bounds(data[split_index[1]-1], bound):
                    #print('{} bounds contain first split but not second split'.format(bound))

                    outer_bounds.append((bound[0], split_value1))
                    inner_bounds.append((split_value1, bound[1]))
                    outer = False

                else:
                    #print('{} bounds contain first & second split'.format(bound))
                    outer_bounds.append((bound[0], split_value1))
                    inner_bounds.append((split_value1, split_value2))
                    outer_bounds.append((split_value2, bound[1]))

        else:

            if not is_in_bounds(data[split_index[1]-1], bound):
                #print('{} bounds are ***'.format(bound))
                inner_bounds.append(bound)

            else:
                if not is_in_bounds(data[split_index[1]], bound):
                    inner_bounds.append(bound)
                else:
                    inner_bounds.append(bound[0], data[split_index[1]-1])
                    outer_bounds.append((data[split_index[1]-1], bound[1]))
                    #print("D: Output bounds", outer_bounds, inner_bounds)

                outer = True

    return outer_bounds, inner_bounds


def bound_generator_cir(data, split_index, bounds):

    inner_bounds, outer_bounds = [], []

    split_value1 = data[split_index[0]]
    split_value2 = data[split_index[1]]

    #print("-----", data, split_index, bounds)


    # First
    if [-np.inf, np.inf] in bounds:
        inner_bounds.append((split_value1, split_value2))
        outer_bounds.append((split_value2, split_value1))

    # Consecutives
    else:
        outer = True

        if split_index[0] == 0:
            outer = False

        for bound in bounds:

            if outer:
                if not is_in_bounds_cir(data[split_index[0]], bound) and not is_in_bounds_cir(data[split_index[1]-1], bound):
                    #print('{} bounds are before first split'.format(bound))
                    outer_bounds.append(bound)

                else:
                    if not is_in_bounds_cir(data[split_index[1]-1], bound):
                        #print('{} bounds contain first split but not second split'.format(bound))
                        outer_bounds.append((bound[0], split_value1))
                        inner_bounds.append((split_value1, bound[1]))
                        outer = False

                    else:
                        #print('{} bounds contain first & second split'.format(bound))

                        # !~~~~ Interesting corner case: Think and Might be implemented in all cases
                        if bound[0] < split_value1:
                            outer_bounds.append((bound[0], split_value1))

                        inner_bounds.append((split_value1, split_value2))

                        outer_bounds.append((split_value2, bound[1]))

            else:

                if not is_in_bounds_cir(data[split_index[1]-1], bound):
                    #print('{} bounds are ***'.format(bound))
                    inner_bounds.append(bound)

                else:
                    if not is_in_bounds_cir(data[split_index[1]], bound):
                        inner_bounds.append(bound)
                    else:
                        inner_bounds.append(bound[0], data[split_index[1]-1])
                        outer_bounds.append((data[split_index[1]-1], bound[1]))
                        #print("D: Output bounds", outer_bounds, inner_bounds)

                    outer = True

    return outer_bounds, inner_bounds


def is_in_bounds(value, bound):
    return bound[0] <= value < bound[1]


def bound_generator(data, split_index, bounds):
    outer = True

    if split_index[0] == 0:
        outer = False

    """
    print("---------")
    print("Input Bounds: ", bounds)
    print("Input Array: ", data)
    print("Input indexes: [{}:{}]".format(split_index[0], split_index[1]))
    print("values in array [{} {})".format(data[split_index[0]], data[split_index[1]]))
    """

    inner_bounds, outer_bounds = [], []

    split_value1 = data[split_index[0]]
    split_value2 = data[split_index[1]]

    for bound in bounds:

        if outer:
            if not is_in_bounds(data[split_index[0]], bound) and not is_in_bounds(data[split_index[1]-1], bound):
                #print('{} bounds are before first split'.format(bound))
                outer_bounds.append(bound)

            else:
                if not is_in_bounds(data[split_index[1]-1], bound):
                    #print('{} bounds contain first split but not second split'.format(bound))
                    global outer
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

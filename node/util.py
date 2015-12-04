def is_in_bounds(value, bound):
    return bound[0] < value < bound[1]


def bound_generator(data, split_index, bounds):

    inner_bounds, outer_bounds = [], []

    outer = True

    print(data, split_index, bounds)

    split_value1 = (data[split_index[0]-1] + data[split_index[0]])/2.0
    split_value2 = (data[split_index[1]-1] + data[split_index[1]])/2.0

    for bound in bounds:

        if outer:
            if not is_in_bounds(data[split_index[0]], bound):
                outer_bounds.append(bound)

            else:
                if not is_in_bounds(data[split_index[1]], bound):
                    outer_bounds.append((bound[0], split_value1))
                    inner_bounds.append((split_value1, bound[1]))
                    outer = False
                else:
                    outer_bounds.append((bound[0], split_value1))
                    inner_bounds.append((split_value1, split_value2))
                    outer_bounds.append((split_value2, bound[1]))

        else: # This part is not tested!
            if not is_in_bounds(data[split_index[1]], bound):
                inner_bounds.append(bound)

            else:
                inner_bounds.append((split_value2, bound[1]))
                outer_bounds.append((bound[0], split_value2))
                outer = True

    return outer_bounds, inner_bounds

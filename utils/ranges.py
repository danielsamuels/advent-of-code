import itertools


def merge_ranges(ranges):
    # Turn a list of ranges into a list of fewer ranges, where possible
    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    new_ranges = []
    base_range = sorted_ranges.pop(0)
    while sorted_ranges:
        range_extension = sorted_ranges.pop(0)
        if range_extension[0] <= base_range[-1]:
            # The ranges overlap, they can be merged - if the new end point is higher!
            if range_extension[-1] > base_range[-1]:
                base_range = range(base_range[0], range_extension[-1] + 1)
        else:
            # The ranges don't overlap, add the first one to the list
            new_ranges.append(base_range)
            base_range = range_extension

    if not new_ranges:
        new_ranges = [base_range]

    return new_ranges

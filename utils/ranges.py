import itertools


def merge_ranges(ranges: list[range]) -> list[range]:
    # Turn a list of ranges into a list of fewer ranges, where possible
    sorted_ranges = sorted(ranges, key=lambda r: (r[0], r[-1]))

    changes_made = False
    new_ranges = []
    base_range = sorted_ranges.pop(0)
    while sorted_ranges:
        range_extension = sorted_ranges.pop(0)

        # Type 1: 8-10 and 7-9 should merge to 7-10
        # Type 2: 9-22 and 10-21 should merge to 9-22

        if (
            range_extension[0] <= base_range[-1]
            and range_extension[-1] >= base_range[-1]
        ):
            # The ranges overlap, they can be merged - if the new end point is higher!
            new_range = range(base_range[0], range_extension[-1] + 1)
            base_range = new_range
            changes_made = True

            # If we're not going to run again, add this range
            if not sorted_ranges:
                new_ranges.append(new_range)

        elif (
            range_extension[0] >= base_range[0]
            and range_extension[-1] <= base_range[-1]
        ):
            # We don't need to do anything here, it's already been taken out of the `sorted_ranges`
            if not sorted_ranges:
                new_ranges.append(base_range)

        else:
            # The ranges don't overlap, add the base to the result
            new_ranges.append(base_range)
            base_range = range_extension

            # If we're not going to run again, add this range
            if not sorted_ranges:
                new_ranges.append(range_extension)

    if not new_ranges:
        new_ranges = [base_range]

    if changes_made and len(new_ranges) > 1:
        return merge_ranges(new_ranges)

    return new_ranges


assert merge_ranges([range(8, 10), range(7, 9)]) == [range(7, 10)]
assert merge_ranges([range(7, 10), range(7, 9)]) == [range(7, 10)]
assert merge_ranges([range(7, 10), range(7, 11)]) == [range(7, 11)]
assert merge_ranges([range(7, 10), range(7, 10)]) == [range(7, 10)]
assert merge_ranges([range(9, 22), range(10, 21)]) == [range(9, 22)]

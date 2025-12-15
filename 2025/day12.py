from aocd import data, submit

test_data = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
""".strip()

TESTING = False


def main() -> None:
    p1_result = 0
    p2_result = 0

    *shape_data, region_data = data.split("\n\n")

    shapes = [shape.count("#") for shape in shape_data]

    regions = [
        (tuple(map(int, bits[0].split("x"))), list(map(int, bits[1].split())))
        for region in region_data.split("\n")
        if (bits := region.split(": "))
    ]

    valid_regions = 0
    for region in regions:
        [width, height], quantities = region
        area = width * height

        shape_space_consumption = 0
        for index, quantity in enumerate(quantities):
            shape_space_consumption += shapes[index] * quantity

        if shape_space_consumption < area:
            valid_regions += 1

    p1_result = valid_regions

    if not TESTING:
        submit(p1_result, part="a")
    # submit(p2_result, part='b')


if __name__ == "__main__":
    main()

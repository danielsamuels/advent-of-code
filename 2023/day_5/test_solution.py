from solution import Day

test_data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 35


def test_run_step_2():
    # seed 82, soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46
    assert Day(test_data).run_step_2() == 46

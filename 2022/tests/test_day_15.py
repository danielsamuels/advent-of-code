from year_2022.day_15 import Day

test_data = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".strip()


def test_parse_input():
    day = Day(test_data)
    assert len(day.sensors) == 14
    assert day.beacons == {
        (-2, 15): True,
        (10, 16): True,
        (15, 3): True,
        (2, 10): True,
        (21, 22): True,
        (25, 17): True,
    }


def test_calculate_distances():
    # Assert that all the sensors have the closest beacon calculated correctly
    day = Day(test_data)
    for sensor, closest_beacon in day.sensors.items():
        closest = min(day.distances[sensor].items(), key=lambda d: d[1])[0]
        assert closest == closest_beacon


def test_invalid_positions_single():
    day = Day('Sensor at x=8, y=7: closest beacon is at x=2, y=10')
    invalid_positions = day.calculate_invalid_positions(7)
    assert len(invalid_positions) == 18


def test_invalid_positions_full():
    day = Day(test_data)
    invalid_positions = day.calculate_invalid_positions(10)
    assert sorted(invalid_positions) == [
        -2, -1, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24
    ]


def test_run_step_1():
    assert Day(test_data).run_step_1(10) == 26


def test_run_step_2():
    assert Day(test_data).run_step_2(20) == 56000011

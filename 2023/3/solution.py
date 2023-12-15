from utils.grid import parse_grid, Direction, relative_points_occupied, all_relative_point_occupation, \
    get_contiguous_value, get_contiguous_numerical_ranges


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.grid = parse_grid(data, mapping=False, ignore_dots=True)

    def run_step_1(self) -> int:
        # Find all of the symbols, determine if there's any numbers around
        valid_values = []

        ranges = get_contiguous_numerical_ranges(self.grid)

        for positions, value in ranges.items():
            has_symbol_nearby = False
            for position in positions:
                occupations = all_relative_point_occupation(self.grid, position)
                nearby_symbols = list(filter(lambda v: not v['value'].isdigit(), occupations.values()))
                if any(nearby_symbols):
                    has_symbol_nearby = nearby_symbols

            if has_symbol_nearby:
                # print(f'(positions={positions}, value={value}) has symbol {has_symbol_nearby} nearby')
                valid_values.append(int(value))

        return sum(valid_values)

    def run_step_2(self) -> int:
        ranges = get_contiguous_numerical_ranges(self.grid)
        results = []

        # Find all stars in the grid
        star_positions = {position for position, value in self.grid.items() if value == '*'}
        for position in star_positions:
            pos_ranges = set()
            occupations = all_relative_point_occupation(self.grid, position)
            for occu in occupations.values():
                for rang in ranges.keys():
                    if occu['position'] in rang:
                        pos_ranges.add(rang)

            if len(pos_ranges) == 2:
                pos_ranges = list(pos_ranges)
                results.append(int(ranges[pos_ranges[0]]) * int(ranges[pos_ranges[1]]))

        return sum(results)

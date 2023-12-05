class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.seeds = []
        self.maps = {}

    def parse_data(self):
        seeds = map(int, self.data.pop(0)[6:].split())
        maps = {}
        current_map = None

        for line in self.data:
            if not line:
                continue

            if 'map:' in line:
                name = line[:-5]
                maps[name] = {}
                current_map = name
                continue

            destination_start, source_start, range_length = map(int, line.split())

            source_range = range(source_start, source_start + range_length)
            destination_range = range(destination_start, destination_start + range_length)

            maps[current_map][source_range] = destination_range

        return seeds, maps

    def get_mapped_value(self, map_name, value):
        map_data = self.maps[map_name]
        for source_range, destination_range in map_data.items():
            try:
                index = source_range.index(value)
                return destination_range[index]
            except ValueError:
                continue

        return value

    def get_mapped_value_flipped(self, map_name, value, fallible=False):
        map_data = self.maps[map_name]
        for source_range, destination_range in map_data.items():
            try:
                index = destination_range.index(value)
                return source_range[index]
            except ValueError:
                continue

        if fallible:
            return None

        return value

    def compute_seeds(self):
        results = {}
        for seed in self.seeds:
            soil = self.get_mapped_value('seed-to-soil', seed)
            fertilizer = self.get_mapped_value('soil-to-fertilizer', soil)
            water = self.get_mapped_value('fertilizer-to-water', fertilizer)
            light = self.get_mapped_value('water-to-light', water)
            temperature = self.get_mapped_value('light-to-temperature', light)
            humidity = self.get_mapped_value('temperature-to-humidity', temperature)
            location = self.get_mapped_value('humidity-to-location', humidity)
            results[seed] = location

        return results

    def compute_location(self, location):
        humidity = self.get_mapped_value_flipped('humidity-to-location', location)
        temperature = self.get_mapped_value_flipped('temperature-to-humidity', humidity)
        light = self.get_mapped_value_flipped('light-to-temperature', temperature)
        water = self.get_mapped_value_flipped('water-to-light', light)
        fertilizer = self.get_mapped_value_flipped('fertilizer-to-water', water)
        soil = self.get_mapped_value_flipped('soil-to-fertilizer', fertilizer)
        seed = self.get_mapped_value_flipped('seed-to-soil', soil)

        if any(seed in s for s in self.seeds):
            return location

    def run_step_1(self) -> int:
        self.seeds, self.maps = self.parse_data()
        computed_seeds = self.compute_seeds()
        return min(computed_seeds.values())

    def run_step_2(self) -> int:
        self.seeds, self.maps = self.parse_data()
        self.seeds = list(self.seeds)

        self.seeds = [
            range(self.seeds[i * 2], self.seeds[i * 2] + self.seeds[(1 * 2) + 1])
            for i in range(len(self.seeds) // 2)
        ]

        for location in range(1, 100_000_000):
            if seed := self.compute_location(location):
                return seed


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    result = Day(read_data).run_step_1()
    print(f'Step 1: {result}')

    result_2 = Day(read_data).run_step_2()
    print(f'Step 2: {result_2}')

from importlib import import_module


def run(year, day, data) -> tuple[int, int]:
    module = import_module(f"{year}.{day}.solution")

    part_1 = module.Day(data).run_step_1()
    part_2 = module.Day(data).run_step_2()

    return part_1, part_2

import pathlib

import aocd


def get_data(filename):
    parts = pathlib.Path(filename).absolute().parts
    day = int(next(p[4:] for p in parts if p.startswith('day_')))
    year = int(next(p[5:] for p in parts if p.startswith('year_')))
    return aocd.get_data(year=year, day=day)

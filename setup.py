from setuptools import setup

setup(
    name="adventofcode",
    entry_points={"adventofcode.user": ["adventofcode = solve:run"]},
)
from pprint import pprint

from aocd import data, submit
from frozendict import frozendict

from utils.graphs import find_all_paths, find_all_paths

test_data = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip()

test_data_2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip()

TESTING = 0
if TESTING == 1:
    data = test_data
if TESTING == 2:
    data = test_data_2


def part_1() -> None:
    paths = find_all_paths(devices, "you", "out", tuple())
    p1_result = len(list(paths))
    print(f"{p1_result=}")

    if not TESTING:
        submit(p1_result, part="a")


def part_2() -> None:
    def test_fn(path):
        return "fft" in path and "dac" in path

    print("Starting the part 2 path-finding extravaganza")
    fft_dac_paths = find_all_paths(devices, "fft", "dac")
    print(f"Found {len(fft_dac_paths)} paths from fft->dac")

    if fft_dac_paths:
        srv_fft_paths = find_all_paths(devices, "svr", "fft")
        # Then we'd have fft_dac_paths
        dac_out_paths = find_all_paths(devices, "dac", "out")
        print(
            f"{len(srv_fft_paths)} paths from src->fft, {len(fft_dac_paths)} paths from fft->dac and {len(dac_out_paths)} paths from dac->out"
        )
        p2_result = len(srv_fft_paths) * len(fft_dac_paths) * len(dac_out_paths)
    else:
        srv_dac_paths = find_all_paths(devices, "svr", "fft")
        dac_fft_paths = find_all_paths(devices, "dac", "fft")
        fft_out_paths = find_all_paths(devices, "fft", "out")
        p2_result = len(srv_dac_paths) * len(fft_dac_paths) * len(fft_out_paths)

    print(f"{p2_result=}")
    if not TESTING:
        submit(p2_result, part="b")


if __name__ == "__main__":
    devices = {}
    for row in data.splitlines():
        key, values = row.split(": ")
        devices[key] = tuple(values.split())

    devices = frozendict(devices)

    if not TESTING or TESTING == 1:
        part_1()

    if not TESTING or TESTING == 2:
        part_2()

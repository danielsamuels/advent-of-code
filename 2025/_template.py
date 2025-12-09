from aocd import data, submit

test_data = """

""".strip()

TESTING = True
if TESTING:
    data = test_data


def main() -> None:
    p1_result = 0
    p2_result = 0

    if not TESTING:
        submit(p1_result, part="a")
    # submit(p2_result, part='b')


if __name__ == "__main__":
    main()

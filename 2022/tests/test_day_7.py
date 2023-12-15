from year_2022.day_7 import run_step_1, run_step_2, construct_filesystem

test_data = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""".strip()


def test_day_7_step_1():
    output = run_step_1(test_data)
    assert output == 95437


def test_day_7_step_2():
    output = run_step_2(test_data)
    assert output == 24933642

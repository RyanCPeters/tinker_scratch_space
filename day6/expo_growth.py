from aoc_2021 import get_raw_data

dummy_source = ["3,4,3,1,2"]

def prep_data(data):
    ret = {}
    for line in data:
        for age in line.split(","):
            age = int(age)
            ret[age] = ret.setdefault(age,0)+1
    return ret

def update(data:dict):
    spawners = data.pop(0,0)
    keys = sorted(tuple(data.keys()))
    for k in keys:
        v = data.pop(k)
        data[k-1] = v
    data[6] = data.setdefault(6,0) + spawners
    data[8] = spawners

def solve_part1(data:dict):
    for _ in range(80):
        update(data)
    num_fish = sum(data.values())
    print(f"solve_part1: {num_fish=}")

def solve_part2(data:dict):
    for _ in range(256-80):
        update(data)
    num_fish = sum(data.values())
    print(f"solve_part2: {num_fish=}")

def main():
    # dummy_data = prep_data(dummy_source)
    # solve_part1(dummy_data)
    input_data = prep_data(get_raw_data(__file__))
    solve_part1(input_data)
    solve_part2(input_data)


if __name__ == '__main__':
    main()
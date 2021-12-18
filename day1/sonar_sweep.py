from pathlib import Path


def get_data():
    here = Path(__file__).parent
    return tuple(map(int, here.joinpath("input.txt").read_text().splitlines()))

def solve_part1(data):
    return sum(v1<v2 for v1,v2 in zip(data,data[1:]))

def solve_part2(data):
    iter1 = (v1+v2+v3 for v1,v2,v3 in zip(data,data[1:],data[2:]))
    iter2 = (v1+v2+v3 for v1,v2,v3 in zip(data[1:],data[2:],data[3:]))
    return sum(v1<v2 for v1,v2 in zip(iter1,iter2))

def main():
    input_data = get_data()
    print(solve_part1(input_data))
    print(solve_part2(input_data))

if __name__ == '__main__':
    main()
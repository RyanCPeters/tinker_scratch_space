from pathlib import Path
import numpy as np

dummy = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]
dummy = np.asarray(tuple(map(lambda s: tuple(int(v) for v in s),map(str.strip, dummy))))

def get_data():
    here = Path(__file__).parent
    ret = np.asarray(tuple(map(lambda s: tuple(int(v) for v in s),map(str.strip, here.joinpath("input.txt").read_text().splitlines()))))

    return ret

def solve_part1(arr:np.ndarray):
    avg_arr = arr.sum(0)/arr.shape[0]
    gamma_avgs = tuple(round(v) for v in avg_arr)
    epsilon_str = "".join(str(1-v) for v in gamma_avgs)
    gamma_str = "".join(str(v) for v in gamma_avgs)
    gamma = int(gamma_str,2)
    epsilon = int(epsilon_str,2)
    print(f"part 1 solution: {gamma=}, {epsilon=}, product={gamma*epsilon}")

def solve_part2(arr):
    o2_view = arr.copy()
    co2_view = arr.copy()
    for pos in range(arr.shape[1]):
        if o2_view.shape[0]>1:
            o2_pos_bits = int(o2_view[:,pos].sum()/o2_view.shape[0]+.5)
            o2_view = o2_view[o2_view[:,pos] == o2_pos_bits,:]
        if co2_view.shape[0]>1:
            co2_pos_bits = 1-int(co2_view[:,pos].sum()/co2_view.shape[0]+.5)
            co2_view = co2_view[co2_view[:,pos] == co2_pos_bits,:]

    o2 = int("".join(str(v) for v in o2_view[0]),2)
    co2 = int("".join(str(v) for v in co2_view[0]),2)
    # dbg_break = 0
    print(f"part 2 solution: {o2_view=}, {o2=}, {co2_view=}, {co2=}, product={o2*co2}")
    dbg_break = 0


def main():
    input_data = get_data()
    solve_part1(input_data)
    solve_part2(input_data)
    # print(solve_part2(input_data))

if __name__ == '__main__':
    main()
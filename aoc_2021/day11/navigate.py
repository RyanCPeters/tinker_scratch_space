from typing import List

import numpy as np
from numba import njit, stencil

from aoc_2021 import get_raw_data
from aoc_2021.day11 import dummy_input


def parse_data(raw:List[str]):
    return np.array(tuple(map(lambda s:list(int(v) for v in s),raw)))

@njit(fastmath=True,nogile=True)
def update(data:np.ndarray):
    @stencil
    def ten_adjacent(a):
        return a[0,0]<10 +   ( a[-1, 0]>9 | a[-1, 1]>9 |a[0, 1]>9 |a[-1, 0]>9 |a[-1, 0]>9 |a[-1, 0]>9 |a[-1, 0]>9 |a[-1, 0]>9)
    data += 1


def solve_part1(data:np.ndarray):


def main():
    input_data = parse_data(dummy_input)
    # input_data = parse_data(get_raw_data(__file__))


if __name__ == '__main__':
    main()
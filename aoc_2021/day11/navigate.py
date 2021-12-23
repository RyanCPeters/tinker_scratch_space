from typing import List

import numpy as np
from numba import njit, prange

from aoc_2021 import get_raw_data
from aoc_2021.day11 import dummy_input, make_ground_truth
import cv2


def display(img, title:str=None,  delay=0, do_init=False, do_destroy=False, wname="window",):
    if do_init:
        cv2.namedWindow(wname, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(wname, 800, 500)
    if title:
        cv2.setWindowTitle(wname,title)
    cv2.imshow(wname, img)
    k = cv2.waitKey(delay)
    if do_destroy:
        cv2.destroyWindow(wname)
    return k


def parse_data(raw: List[str]):
    return np.array(tuple(map(lambda s: list(int(v) for v in s), raw)))


def display_cycle(joined, data, matches, ground_truth, step, num_flashes):

    joined[...,0] += data
    joined[...,1] += ground_truth
    joined[...,2] += matches*9
    display(joined*25, f"{num_flashes:<10}, {step=}",delay=500)
    return step+1


def update(data:np.ndarray):
    data += 1
    h,w = data.shape
    points = list(zip(*np.nonzero(data==10)))
    while points:
        y,x = points.pop()
        ylo = max(0, y - 1)
        yhi = min(h, y + 2)
        xlo = max(0, x - 1)
        xhi = min(w, x + 2)
        data[ylo:yhi,xlo:xhi] += 1
        points.extend(((ylo+_y,xlo+_x) for _y,_x in zip(*np.nonzero(data[ylo:yhi,xlo:xhi]==10))))
    mask = data>9
    data[mask] *= 0
    return mask.sum()


def solve_part1(data: np.ndarray):
    _data = data.copy()
    num_flashes = 0
    for _ in range(100):
        num_flashes += update(_data)
    print(f"solve_part1: {num_flashes=}")

def solve_part2(data:np.ndarray):
    for i in range(1,500):
        num_flash = update(data)
        if num_flash==100:
            print(f"solve_part2: all flash on {i}")
            break

def main():
    # input_data = parse_data(dummy_input).astype(np.uint8)
    input_data = parse_data(get_raw_data(__file__)).astype(np.uint8)
    # solve_part1(input_data)
    solve_part2(input_data)


if __name__ == '__main__':
    main()

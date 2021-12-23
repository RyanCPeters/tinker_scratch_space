from typing import List, Tuple, Optional

import numpy as np
import cv2

from aoc_2021 import get_raw_data
from aoc_2021.day13 import dummy_input

do_display = False

def display(img, title:str=None,  delay=0, do_init=False, do_destroy=False, wname="window",):
    if not do_display:
        return -1
    if img.dtype == bool:
        img = img.astype(np.uint8)*255
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
    coords = []
    instructions = []
    itr = map(str.strip,raw)
    maxx = 0
    maxy = 0
    for i,point in enumerate(itr):
        if point:
            coords.append(tuple(map(int,point.split(","))))
        else:
            maxy = max(coords,key=lambda tpl:tpl[1])[1]+1
            maxx = max(coords,key=lambda tpl:tpl[0])[0]+1

            for fold in itr:
                ax,pos = fold.rpartition(" ")[2].split("=")
                instructions.append((ax,int(pos)))
            break
    points = np.zeros((maxy,maxx),bool)
    for x,y in coords:
        points[y,x] = True
    return points,instructions

def do_instruction(data:np.ndarray,ax,pos):
    dbg_break = 0
    # do instruction specific data access
    if ax == "y":
        flip = data[pos+1:][::-1]
        base = data[:pos]
        diff = flip.shape[0]-base.shape[0]
        padding = (diff,0),(0,0)
    elif ax == "x":
        flip = data[:, pos+1:][:, ::-1]
        base = data[:,:pos]
        diff = flip.shape[1]-base.shape[1]
        padding = (0,0),(diff,0)
    # handle possible alignment problems
    if diff > 0:
        # we need to pad the top edge of top with 0's
        base = np.pad(base, padding, constant_values=0)
    elif diff < 0:
        # we need to pad the top edge of bottom with 0's
        flip = np.pad(flip, padding, constant_values=0)
    # else they're equal, so we don't need to do any special alignment.
    if do_display:
        display(np.concatenate([base, flip], axis=1), do_init=True, wname="base and inverted flip portion")
    flip |= base
    display(flip, do_init=True, wname="or'd together")
    data = flip
    display(data, do_init=True, wname="data after first instruction")
    return data

def solve_part1(data_in:np.ndarray, instructions:List[Tuple[str,int]]):
    data = data_in.copy()
    display(data, wname="data initial state", do_init=True)
    data = do_instruction(data,*instructions[0])
    print(f"solve_part1: {data.sum()}")
    cv2.waitKey(0)
    dbg_break = 0


def solve_part2(data:np.ndarray, instructions):
    global do_display
    for ax,pos in instructions:
        data = do_instruction(data,ax,pos)
    data = np.pad(data,((1,1),(1,1)),constant_values=0)
    do_display = True
    display(data,wname="final part2 output",do_init=True)
    print(f"solve_part2: ")
    dbg_break = 0

def main():
    try:
        # input_data = parse_data(dummy_input)
        input_data = parse_data(get_raw_data(__file__))
        # solve_part1(*input_data)
        solve_part2(*input_data)
    finally:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
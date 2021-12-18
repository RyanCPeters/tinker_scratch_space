from aoc_2021 import get_raw_data
import numpy as np


dummy_source = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]

def visualize_hitmap(hitmap):
    hit_list = hitmap.tolist()
    for lst in hit_list:
        for j,elem in enumerate(lst):
            if elem==0:
                lst[j] = "."
            else:
                lst[j] = str(elem)
        print("".join(lst))
    print(f"{hitmap.shape=}")

def prep_data(data):
    return np.array(tuple(map(lambda s: tuple(tuple(map(int,vv.split(","))) for vv in (v.strip() for v in s.split("->"))),data)))

def solve_part1(point_data:np.ndarray, hitmap:np.ndarray, announce:bool=True):
    hmatch = point_data[:,0,0]==point_data[:,1,0]
    vmatch = point_data[:,0,1]==point_data[:,1,1]
    for (x1,y1),(x2,y2) in point_data[hmatch]:
        y1,y2 = (y1,y2) if y1<y2 else (y2,y1)
        hitmap[y1:y2+1,x1] += 1
    for (x1,y1),(x2,y2) in point_data[vmatch]:
        x1,x2 = (x1,x2) if x1<x2 else (x2,x1)
        hitmap[y1,x1:x2+1] += 1
    danger_points = np.count_nonzero(hitmap>1)
    if hitmap.size < (15 * 15):
        visualize_hitmap(hitmap)
    if announce:
        print(f"solve_part1: {danger_points=}")
    return point_data,hitmap,hmatch,vmatch

def solve_part2(point_data:np.ndarray,hitmap:np.ndarray,hmatch:np.ndarray,vmatch:np.ndarray):
    diags = point_data[~np.logical_or(hmatch,vmatch)]
    for (x1, y1), (x2, y2) in diags:
        xstep = -1*(x1>x2)+(x1<x2)
        ystep = -1*(y1>y2)+(y1<y2)
        ypts = tuple(range(y1,y2+ystep,ystep))
        xpts = tuple(range(x1,x2+xstep,xstep))
        hitmap[ypts,xpts] += 1
    danger_points = np.count_nonzero(hitmap>1)
    if hitmap.size<(15*15):
        visualize_hitmap(hitmap)
    print(f"solve_part2: {danger_points=}")


def main():
    input_dummy = prep_data(dummy_source)
    dh = input_dummy[:,:,1].max()+1
    dw = input_dummy[:,:,0].max()+1
    dummy_hits = np.zeros((dw,dh),np.uint16)
    solve_part2(*solve_part1(input_dummy, dummy_hits))
    input_data = prep_data(get_raw_data(__file__))
    h = input_data[:,:,1].max()+1
    w = input_data[:,:,0].max()+1
    hits = np.zeros((w,h),np.uint16)
    solve_part2(*solve_part1(input_data, hits))

if __name__ == '__main__':
    main()
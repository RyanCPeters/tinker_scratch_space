import numpy as np
from numba import njit, stencil, prange
import cv2
from aoc_2021 import get_raw_data
from aoc_2021.day9 import dummy_input


def prep_data(raw):
    raw = list(v for v in raw if v.strip())
    ret = list(map(lambda line: tuple(map(int,tuple(line))),raw))
    ret = np.pad(np.asarray(ret),((1,1),(1,1)),constant_values=10).astype(np.uint8)
    return ret

def inspect(img:np.ndarray,wname, title=None,delay=0,do_init=True,do_destroy=True):
    if img.dtype==np.float64:
        img = img.astype(np.float32)
    elif img.dtype in (np.int64,np.uint64,np.uint32,np.int32):
        img = ((img.astype(np.float64)/img.max())*(256**2)).astype(np.uint16)
    if do_init:
        cv2.namedWindow(wname,cv2.WINDOW_NORMAL)
    cv2.imshow(wname,img)
    if title is not None:
        cv2.setWindowTitle(wname,title)
    k = cv2.waitKey(delay)
    if do_destroy:
        cv2.destroyWindow(wname)
    return k

def solve_part1(data:np.ndarray):
    @njit(parallel=True,fastmath=True,nogil=True)
    def numba_func(d):
        @stencil
        def get_lowest(pt):
            return pt[0,0]<pt[1,0] and pt[0,0]<pt[1,1] and pt[0,0]<pt[0,1] and pt[0,0]<pt[-1,1] and pt[0,0]<pt[-1,0] and pt[0,0]<pt[-1,-1] and pt[0,0]<pt[0,-1] and pt[0,0]<pt[1,-1]
        return get_lowest(d)
    mask = numba_func(data)
    threat_level = (data[mask]+1).sum()
    print(f"solve_part1: {threat_level=}")
    return mask,data

def solve_part2(min_data:np.ndarray, data:np.ndarray):
    @njit(fastmath=True)
    def parallel_mapper(val,iy,ix,mask:np.ndarray,out:np.ndarray, region_counts:np.ndarray):
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        done = []
        stack = [(iy,ix)]
        h,w = out.shape
        val += 1
        while stack:
            y,x = stack.pop(0)
            if out[y,x]>val:
                out[y,x] = val
                done.append((y,x))
                region_counts[val] += 1
                for dy, dx in directions:
                    _y = y + dy
                    _x = x + dx
                    if 0 <= _y < h and 0 <= _x < w and mask[_y, _x]:
                        mask[_y, _x] *= 0
                        stack.append((_y, _x))
            elif out[y,x]<val:
                region_counts[out[y,x]] += region_counts[val]
                region_counts[val] *= 0
                val = out[y,x]
                for y,x in done:
                    if out[y,x]>val:
                        out[y,x] = val
            n = 0
        m = 0

    @njit(parallel=True,fastmath=True)
    def numba_helper(mask:np.ndarray,out:np.ndarray,nzeros:np.ndarray, region_counts:np.ndarray):
        for i in prange(nzeros.shape[0]):
            iy,ix = nzeros[i]
            parallel_mapper(i,iy,ix,mask,out,region_counts)

    bound_mask = data<9
    nonzeros = np.asarray(np.nonzero(min_data)).T
    bound_map = np.zeros(data.shape,np.uint16)+nonzeros.shape[0]+1
    reg_cts = np.zeros(nonzeros.shape[0]+1, int)
    numba_helper(bound_mask,bound_map,nonzeros,reg_cts)
    bound_map[bound_map == nonzeros.shape[0]+1] *= 0
    args = reg_cts.argsort()
    area = reg_cts[args[-3:]].prod()
    # area = reg_cts
    # inspect(((bound_map.astype(float)/bound_map.max())*255).astype(np.uint8), "check bound map")
    print(f"solve_part2: {area}")
    dbg_break = 0

def main():

    # data = prep_data(dummy_input)
    data = prep_data(get_raw_data(__file__))
    solve_part2(*solve_part1(data))
    dbg_break = 0

if __name__ == '__main__':
    main()

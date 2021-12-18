import os
from time import perf_counter
from multiprocessing.connection import wait as mpWait

from numba import njit, prange
import numpy as np

from aoc_2021 import npsm_create_context, npsm_use_context, multiproc_nested_contexts, mpConn
from aoc_2021 import get_raw_data

def dummy():
    yield "16,1,2,0,4,2,7,1,2,14"


def prep_data(raw):
    data = next(raw)
    return sorted(map(int,data.split(",")))

@njit(cache=True)
def get_relative_distances_p2(hpos:int, crabs:np.ndarray, dists:np.ndarray, spans_by_idx:np.ndarray):
    dists[:] = np.abs(crabs-hpos)
    return hpos,sum(spans_by_idx[:rel_d+1].sum() for rel_d in dists)

def get_relative_distances_p1(hpos:int, crabs:np.ndarray):
    # ret = sum(abs(rel_k-hpos) for rel_k in keys)
    ret = np.abs(crabs-hpos).sum()
    return hpos,ret

def solve_part1(crabs:list[int]):
    minmax_dists = 0xffffffffffffffff
    least_fule_dist = -1
    ftrs = [get_relative_distances_p1( hpos, crabs) for hpos in crabs]
    for k,cumulative_dists in ftrs:
        if cumulative_dists<minmax_dists:
            minmax_dists = cumulative_dists
            least_fule_dist = k
    print(f"solve_part1:\n\tposition for best fule={least_fule_dist}, distance={minmax_dists}")

def solve_part2(crabs:np.ndarray, crabs_sm_name:str, spans_sm_name:str):
    minmax_dists = 0xffffffffffffffff
    least_fule_dist = -1
    nprocs = os.cpu_count()-1
    span_size = (crabs.shape[0]+nprocs-1)//nprocs
    proc_args = tuple((slice(i,i+span_size),crabs_sm_name, spans_sm_name)
                      for i in range(0,(crabs.shape[0]+span_size-1),span_size))
    with multiproc_nested_contexts(nprocs,False,part2_proc_helper,True, proc_args,is_daemon=True) as pipes:
        _pipes = [p for p in pipes]
        while _pipes:
            for i in range(len(_pipes)-1,-1,-1):
                p:mpConn = _pipes[i]
                if p.poll(.01):
                    result = p.recv()
                    if isinstance(result,str):
                        _pipes.pop(i)
                    else:
                        k, cumulative_dist = result
                        if cumulative_dist < minmax_dists:
                            minmax_dists = cumulative_dist
                            least_fule_dist = k
            # for p in mpWait(_pipes):
            #     p:mpConn
            #     result = p.recv()
            #     if isinstance(result, str):
            #         _pipes.remove(p)
            #     else:
            #         k, cumulative_dist = result
            #     if cumulative_dist < minmax_dists:
            #         minmax_dists = cumulative_dist
            #         least_fule_dist = k
    print(f"solve_part2:\n\tposition for best fule={least_fule_dist}, distance={minmax_dists}")

def part2_proc_helper(crabs_slice:slice, crabs_name:str, span_name:str,pwrite:mpConn):
    with pwrite:
        num_computes = 0
        with npsm_use_context(crabs_name) as sm_crabs:
            with npsm_use_context(span_name) as sm_spans:
                for crab_pos in sm_crabs[crabs_slice]:
                    pos_result = get_relative_distances_p2(crab_pos,sm_crabs,sm_spans)
                    pwrite.send(pos_result)
                    num_computes += 1
        pwrite.send(f"completed {num_computes}")

def main():
    # t0 = perf_counter()
    crabs = np.asarray(prep_data(get_raw_data(__file__)))
    crabs_sm_name = "align crabs"
    with npsm_create_context(crabs_sm_name, crabs) as sm_crabs:
        span_sm_name = "precomputed_spans"
        precomputed_spans = np.arange(crabs[-1]+1)
        with npsm_create_context(span_sm_name, precomputed_spans):
            # t1 = perf_counter()
            # solve_part1(crabs)
            t2 = perf_counter()
            solve_part2(sm_crabs, crabs_sm_name, span_sm_name)
            t3 = perf_counter()
    # t4 = perf_counter()
    # print(f"part 1 ellapsed: {t2-t1} seconds")
    print(f"part 2 ellapsed: {t3-t2} seconds")
    # print(f"p1p2 ellapsed: {t3-t1} seconds")
    # print(f"main execution time: {t4-t0} seconds")



if __name__ == '__main__':
    main()
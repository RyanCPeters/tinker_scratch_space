from typing import List, Optional, Tuple
import re
import numpy as np
from aoc_2021 import get_raw_data
from aoc_2021.day10 import dummy_input


# bound_check_re = re.compile("([[({<].*?[])}>])")
chunk_bound_conditions = frozenset((v1+v2 for v1 in ")}]>" for v2 in "({[<"))
closed2open_brackets = { k:v for k,v in zip(")}]>","({[<") }
open2closed_brackets = {v:k for k,v in closed2open_brackets.items()}
bracket_inc_vals = { **{k:1 for k in "({[<"}, **{k:-1 for k in ")}]>"} }

error_cost = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

class CorruptLine(Exception):
    err_bracket: str
    err_pos: int
    cost: int

    def __init__(self, seq, err_char:str, err_pos) -> None:
        super().__init__(seq)
        self.err_bracket = err_char
        self.err_pos = err_pos
        self.cost = error_cost[err_char]

class Chunk:

    def __init__(self, line_number,seq,start,stop=None) -> None:
        self.line_number = line_number
        self.seq = seq
        self.start = start
        self.open_char = seq[start]
        self.close_char = None
        self.is_corrupt = False
        self.stop = self._find_end(stop)

    def _find_end(self,stop:int=None):

        if stop is not None:
            if self.seq[stop] == open2closed_brackets[self.open_char]:
                return stop
        counts = {}
        try:
            for i,c in enumerate(self.seq[self.start+1:],self.start+1):
                k = closed2open_brackets.get(c, c)
                ref = counts[k] = counts.setdefault(k, 0) + bracket_inc_vals[c]
                if ref < 0:
                    err = CorruptLine(self.seq[self.start:i + 1], c, i)
                    raise err
                elif ref == 0:
                    ret.append(find_chunk_bounds(self.seq, i + 1, stop))
                    ret.append(ret[-1][-1] + 1)
                    break
        except CorruptLine as cl:
            self.is_corrupt = True
def find_chunk_bounds(seq,start:int,stop:int)-> List[Tuple[int]]:
    ret = [start]
    counts = {}
    i = start
    while i<stop:
        c = seq[i]
        k = closed2open_brackets.get(c,c)
        ref = counts[k] = counts.setdefault(k,0)+bracket_inc_vals[c]
        if ref<0:
            err = CorruptLine(seq[start:i + 1], c, i)
            raise err
        elif ref==0:
            ret.append(find_chunk_bounds(seq,i+1,stop))
            ret.append(ret[-1][-1]+1)
            break
        i += 1
    else:
        ret.append(i)
    return ret

# class Chunk:
#
#     def __init__(self, line_number:int,input_seq: List[str],start:int = 0, stop:int=None,parent:Optional["Chunk"]=None) -> None:
#         self.line_number = line_number
#         self.seq = input_seq[start:stop]
#         self.expected_second = bracket_pairings.get(self.seq[0],None)
#         self.parent = parent
#         self.children: List["Chunk"] = []
#
#     def find_chunk_bounds(self,stop:int)-> int:
#         ret = stop
#         counts = {}
#         for c in self.seq[:stop]:
#
#             ref = counts[c] = counts.setdefault(c,0)+bracket_inc_vals[c]
#             if ref<0:
#                 err = InvalidLineCase("Yup",)
#                 raise InvalidLineCase
#
#         return ret

def prep_data(raw):
    raw = list(v for v in raw if v.strip())
    ret = list(map(list,raw))
    return ret

def solve_part1(data:List[str]):
    line_results = []
    corrupted_lines = []
    for i,line in enumerate(data):
        split_points = bound_check_re.split(line)
        dbg_break = 0
        # ref = []
        # try:
        #     ref.append(find_chunk_bounds(line,0,len(line)))
        #     endings = ref[-1][-1]
        #     while endings<len(line):
        #         ref.append(find_chunk_bounds(line, endings, len(line)))
        #         endings = ref[-1][-1]
        # except CorruptLine as lic:
        #     corrupted_lines.append((i,lic))
        # else:
        #     line_results.append((i,ref))
    corrupted_score = sum(err.cost for i,err in corrupted_lines)
    print(f"solve_part1: {corrupted_score=}")
    return line_results


def main():
    input_data = prep_data(dummy_input)
    line_results = solve_part1(input_data)
    dbg_break = 0

if __name__ == '__main__':

    main()
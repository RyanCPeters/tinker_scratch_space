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

class IncompleteLine(Exception):
    line_number: int

    def __init__(self, line_number, *args: object) -> None:
        super().__init__(*args)
        self.line_number = line_number


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

    def __init__(self, line_number,seq,start, stop=None, parent:"Chunk"=None) -> None:
        self.parent = parent
        self.child_chunks = []
        self.line_number = line_number
        self.seq = seq
        self.start = start
        self.open_char = seq[start][0]
        self.close_char = ""
        self.is_corrupt = False
        self.is_incomplete = False
        self.stop = self._find_end(stop)

    def _find_end(self,stop:int=None):
        expected_closer = open2closed_brackets[self.open_char]
        if stop is not None:
            if self.seq[stop][0] == expected_closer:
                return stop
        try:
            i = self.start
            while i<len(self.seq):
                c,ref = self.seq[i]
                k = closed2open_brackets.get(c, c)
                if c == k and i!=self.start:
                    child = Chunk(self.line_number,self.seq,i, None,self)
                    self.child_chunks.append(child)
                    if child.is_corrupt:
                        self.is_corrupt = True
                        return None
                    if child.stop is None:
                        child.is_corrupt = True
                        self.is_corrupt = True
                        return None
                    i = child.stop
                elif ref < 0:
                    err = CorruptLine(self.seq[self.start:i + 1], c, i)
                    raise err
                elif ref == 0:
                    if c==expected_closer:
                        return i
                    break
                i += 1
            else:
                self.is_incomplete = True
                return None
        except CorruptLine as cl:
            self.is_corrupt = True
            return None
        return len(self.seq)

    def flat_map_tree(self):
        yield self
        for child in self.child_chunks:
            yield from child.flat_map_tree()

    def __str__(self) -> str:
        seq = "".join(self.seq[self.start:self.stop])
        return f"[{self.line_number}; ({self.start}, {self.stop}) ..{seq}..; {self.is_corrupt}; {self.is_incomplete}]"

    def __repr__(self) -> str:
        child_reprs = " | ".join(repr(child) for child in self.child_chunks)
        return f"Chunk - {str(self)} {{ {child_reprs} }}"


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
    def do_line_chunking(pos):
        chunk = Chunk(i, line, pos)
        if not (chunk.is_corrupt or chunk.is_incomplete):
            if chunk.stop is not None and chunk.stop < len(line):
                do_line_chunking(chunk.stop+1)
        return chunk
    line_results = []
    corrupted_lines = []
    incomplete_lines = []
    chunks_list = []
    for i,line in enumerate(data):

        counts = {}
        count_seq = []
        for k,c in enumerate(line):
            k = closed2open_brackets.get(c, c)
            ref = counts[k] = counts.setdefault(k, 0) + bracket_inc_vals[c]
            count_seq.append(ref)
        line = list(zip(line,count_seq))
        fail_point = None
        root = do_line_chunking(0)
        for j,chunk in enumerate(root.flat_map_tree()):
            if chunk.is_corrupt:
                corrupted_lines.append(chunk)
                fail_point = j

            elif chunk.is_incomplete:
                fail_point = j
                incomplete_lines.append(chunk)
            else:
                chunks_list.append(chunk)

        dbg_break = fail_point
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
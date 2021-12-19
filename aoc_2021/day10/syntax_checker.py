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


def prep_data(raw):
    return list(v for v in raw if v.strip())


def solve_part1(data:List[str]):
    cost = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    corrupted_lines = []
    passing_lines = []
    for i,line in enumerate(data):
        _line = line
        line2 = ""
        while line2 != line:
            line2 = line
            line = line.replace("()","").replace("[]","").replace("{}","").replace("<>", "")
        for c1,c2 in zip(line,line[1:]):
            expected = open2closed_brackets.get(c1,c2)
            if c2 in closed2open_brackets and c2!=expected:
                corrupted_lines.append((cost[c2],(expected,c2),_line))
                break
        else:
            passing_lines.append((_line,line))
    corrupted_score = sum(deets[0] for deets in corrupted_lines)
    print(f"solve_part1: {corrupted_score=}")
    return passing_lines

def solve_part2(data:List[str]):
    costs = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    def compute_score(seq:str):
        ret = 0
        for c in seq:
            ret = ret*5 + costs[c]
        return ret
    solutions = ["".join((open2closed_brackets[v] for v in d[1][::-1])) for d in data]
    if len(solutions)==5:
        failed = [(expected,actual) for expected,actual in zip(("}}]])})]", ")}>]})", "}}>}>))))", "]]}}]}]}>", "])}>"),solutions) if expected!=actual]
        dbg_break = 0

    total_costs = sorted(compute_score(s) for s in solutions)
    print(f"solve_part2: {total_costs[len(total_costs) // 2]}")



def main():
    # input_data = prep_data(dummy_input)
    input_data = prep_data(get_raw_data(__file__))
    solve_part2(solve_part1(input_data))
    dbg_break = 0

if __name__ == '__main__':
    main()
from typing import List, Tuple
from aoc_2021 import get_raw_data
from aoc_2021.day12 import dummy_input

orda = ord('a')
ordz = ord('z')

class CavePath:

    def __init__(self,connections:dict) -> None:
        self.connections = connections
        self.start = connections["start"]
        self.end= connections["end"]

    def dfs(self):
        start_end = {"start","end"}
        stack = [*self.start]
        smalls = set()
        bigs = {}
        solutions = set()
        bread_crumbs = ["start"]
        danger_loops = set()
        while stack:
            seed = stack.pop()
            bread_crumbs = [seed]

            if pos not in start_end:
                if orda<=ord(pos)<=ordz:
                    # small cave
                    if pos not in smalls:
                        bread_crumbs.append(pos)
                        smalls.add(pos)
                        stack.extend(self.connections[pos])
                else:
                    # large cave
                    bread_crumbs.append(pos)
                    if pos in bigs and bigs[pos]>0:
                        if len(bread_crumbs)>2:
                            idx = bread_crumbs.index(pos)
                            maybe_loop = ",".join(bread_crumbs[idx:])
                            if maybe_loop in danger_loops or not any(orda<=_pos<=ordz for _pos in maybe_loop):
                                # with all large caves in this loop, we find ourselves in an
                                # infinit loop
                                danger_loops.add(maybe_loop)
                                bread_crumbs.pop()
                                bigs[pos] -= 1
                                continue
                    stack.extend(self.connections[pos])
                    bigs[pos] = bigs.setdefault(pos,0)+1
            elif pos == "end":
                bread_crumbs.append(pos)
                solutions.add(",".join(bread_crumbs))
                bread_crumbs.pop()










def parse_data(raw: List[str]):
    ret = []
    for line in map(str.strip,raw):
        if ":" in line:
            ret.append([])
        elif line:
            ret[-1].append(line.split('-'))
    return ret

def solve_part1(data:List[Tuple[str,str]]):
    relations = {}
    for a,b in data:
        relations.setdefault(a,set()).add(b)
        relations.setdefault(b,set()).add(a)

    for a,bs in sorted(relations.items(),key=lambda tpl: len(tpl[1])):
        bs: set
        if len(bs)==1:
            if all(ord('a')<=ord(c)<=ord('z') for c in bs.union(set(a))):
                relations.pop(a)
                c = bs.pop()
                ref = relations[c]
                ref.remove(a)
                if not ref:
                    relations.pop(c)

    dbg_break = 0

def main():
    input_data = parse_data(dummy_input)[0]
    # input_data = parse_data(get_raw_data(__file__))
    solve_part1(input_data)
    # solve_part2(input_data)


if __name__ == '__main__':
    main()

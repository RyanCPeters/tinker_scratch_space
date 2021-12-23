from typing import List, Tuple, Optional
from aoc_2021 import get_raw_data
from aoc_2021.day12 import dummy_input

orda = ord('a')
ordz = ord('z')
start_end = {"start","end"}
small_sol = sorted(map(str.strip,"""\
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end""".splitlines()),key=lambda s:(s.count(","),s))
small_sol_p2 = sorted(map(str.strip,"""\
start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end""".splitlines()),key=lambda s:(s.count(","),s))
medium_sol = sorted(map(str.strip,"""\
start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end""".splitlines()),key=lambda s:(s.count(","),s))

class CaveNode:
    connections: dict[str,set[str]]
    label: str

    def __init__(self, label, connections) -> None:
        self.label = label
        self.connections = connections
        self._connection_pos = 0
        if label not in start_end:
            self._exclusive = orda<=ord(label[0])<=ordz
        else:
            self._exclusive = True

    def iter_children(self):
        if not self.label == "end":
            for lbl in self.connections[self.label]:
                if lbl!="start":
                    yield CaveNode(lbl,self.connections)

    def explore_p1(self, path:str):
        if not (self._exclusive and self.label in path):
            if self.label != "start":
                path = path + repr(self)
            yield path
            if self.label!="end":
                for child in self.iter_children():
                    yield from child.explore_p1(path)

    def explore_p2(self, path:str,small_double):
        if (self.label==small_double and path.count(self.label)<2) or not (self._exclusive and self.label in path):

            if self.label != "start":
                path = path + repr(self)
            yield path
            if self.label!="end":
                for child in self.iter_children():
                    yield from child.explore_p2(path, small_double)

    def __str__(self) -> str:
        return self.label

    def __repr__(self) -> str:
        if self.label == "end":
            return f"{self.label}"
        return f"{self.label},"


class CavePath:

    def __init__(self,connections:dict) -> None:
        self.connections = connections
        self.start = CaveNode("start",connections)

    def paths_p1(self):
        given = set()
        for path in self.start.explore_p1(""):
            if path.endswith("end"):
                path = "start,"+path
                if path not in given:
                    yield path
                    given.add(path)

    def paths_p2(self,small_labels):
        given = set()
        for lbl in small_labels:
            for path in self.start.explore_p2("",lbl):
                if path.endswith("end"):
                    path = "start,"+path
                    if path not in given:
                        yield path
                        given.add(path)


def parse_data(raw: List[str]):
    ret = []
    for line in map(str.strip,raw):
        if ":" in line:
            ret.append([])
        elif line:
            ret[-1].append(line.split('-'))
    return ret


def solve_part1(data:List[Tuple[str,str]]):
    if len(data)==7:
        sol = small_sol
    elif len(data)==10:
        sol = medium_sol
    else:
        sol = None
    relations = {}
    for a,b in data:
        relations.setdefault(a,set()).add(b)
        relations.setdefault(b,set()).add(a)

    for a,bs in sorted(relations.items(),key=lambda tpl: len(tpl[1])):
        bs: set
        if len(bs)==1:
            if all(orda<=ord(c[0])<=ordz for c in bs.union(set(a))):
                relations.pop(a)
                c = bs.pop()
                ref = relations[c]
                ref.remove(a)
                if not ref:
                    relations.pop(c)
    cavepaths = CavePath(relations)
    print(f"solve_part1:")
    solution = sorted(cavepaths.paths_p1(), key=lambda s:(s.count(","), s))
    if sol is None:
        for path  in solution:
            print(f"\t{path}")
    else:
        longest = len(max(solution,key=lambda s:len(s)))
        all_equal = True
        for p1, p2 in zip(solution,sol):
            check = p1==p2
            all_equal &= check
            equality = "==" if check else "!="
            print(f"\t{p1:>{longest}} {equality} {p2}")
        print(f"{all_equal=}")
    print(f"solve_part1: {len(solution)}")
    dbg_break = 0


def solve_part2(data:List[Tuple[str,str]]):
    if len(data)==7:
        sol = small_sol_p2
    else:
        sol = None
    relations = {}
    small_caves = set()
    for a,b in data:
        relations.setdefault(a,set()).add(b)
        relations.setdefault(b,set()).add(a)
        if a not in start_end and orda<=ord(a[0])<=ordz:
            small_caves.add(a)
        if b not in start_end and orda<=ord(b[0])<=ordz:
            small_caves.add(b)
    small_caves = list(small_caves)
    cavepaths = CavePath(relations)
    solution = sorted(cavepaths.paths_p2(small_caves), key=lambda s:(s.count(","), s))
    if sol is None:
        for path  in solution:
            # print(f"\t{path}")
            pass
    else:
        longest = len(max(solution,key=lambda s:len(s)))
        all_equal = True
        for p1, p2 in zip(solution,sol):
            check = p1==p2
            all_equal &= check
            # equality = "==" if check else "!="
            # print(f"\t{p1:>{longest}} {equality} {p2}")
        print(f"{all_equal=}")
    print(f"solve_part2: {len(solution)}")
    dbg_break = 0

def main():
    # input_data = parse_data(dummy_input)[0]
    # # solve_part1(input_data)
    # solve_part2(input_data)
    # input_data = parse_data(dummy_input)[1]
    # # solve_part1(input_data)
    # solve_part2(input_data)
    # input_data = parse_data(dummy_input)[2]
    # solve_part1(input_data)
    # solve_part2(input_data)
    input_data = parse_data([":",*get_raw_data(__file__)])[0]
    solve_part1(input_data)
    solve_part2(input_data)


if __name__ == '__main__':
    main()

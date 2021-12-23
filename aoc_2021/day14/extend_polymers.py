from typing import List, Tuple, Optional
from aoc_2021 import get_raw_data

dummy_input = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".splitlines()


def parse_data(raw: List[str])->Tuple[str,dict[str,dict[str,str]]]:
    mapping_rules = {}
    seed = raw[0]
    for line in map(str.strip,raw[2:]):
            (a,b),result = line.split(' -> ')
            mapping_rules.setdefault(a,{}).setdefault(b,result)
    return seed,mapping_rules

def apply_rules(n:int,seed:str,rules:dict[str,dict[str,str]])->str:
    def generate_inserts(src,depth):
        result = ((c1,rules[c1].get(c2,"")) for c1,c2 in src)
        if depth < n:
            return generate_inserts(result,depth+1)
        return result
    ret = tuple(c for c1c2 in generate_inserts(zip(seed+"0",seed[1:]),0) for c in c1c2)
    return ret

def solve_part1(seed:str,rules:dict[str,dict[str,str]]):
    counts = {}
    results = apply_rules(10,seed,rules)
    for c in results:
        counts[c] = counts.setdefault(c,0)+1
    most = max(counts.items(),key=lambda tpl:tpl[1])
    least = min(counts.items(),key=lambda tpl:tpl[1])
    solution = most[1]-least[1]
    print(f"solve_part1: {solution}")
    dbg_break = 0


def solve_part2(seed:str,rules:dict[str,dict[str,str]]):
    counts = {}
    results = apply_rules(40, seed, rules)
    for c in results:
        counts[c] = counts.setdefault(c, 0) + 1
    most = max(counts.items(), key=lambda tpl: tpl[1])
    least = min(counts.items(), key=lambda tpl: tpl[1])
    solution = most[1] - least[1]
    print(f"solve_part2: {solution}")
    dbg_break = 0

def main():
    input_data = parse_data(dummy_input)
    # input_data = parse_data(list(get_raw_data(__file__)))
    solve_part1(*input_data)
    # solve_part2(*input_data)


if __name__ == '__main__':
    main()

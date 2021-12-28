from typing import List, Tuple
from aoc_2021 import get_raw_data
import concurrent.futures as cf
from multiprocessing import current_process

import logging

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
    unique_chars = set(seed)
    for line in map(str.strip,raw[2:]):
            (a,b),result = line.split(' -> ')
            mapping_rules.setdefault(a,{}).setdefault(b,result)
            unique_chars.add(a)
            unique_chars.add(b)
            unique_chars.add(result)
    return seed,mapping_rules

def proc_applicator(n,edge_num,seed,rules):
    def build(c1,c2,depth):
        if depth==0:
            yield c1
        if depth<n:
            result = rules[c1][c2]
            yield from build(c1,result,depth+1)
            yield result
            yield from build(result,c2,depth+1)
        if depth==0:
            yield c2

    logger = logging.getLogger("extend-polymers")
    logger.setLevel(logging.NOTSET)
    handler = logging.StreamHandler()
    handler.setLevel(logging.NOTSET)
    logger.addHandler(handler)
    pname = current_process().name
    logger.warning(f"{pname}:  begin for idx: {edge_num}")
    output = "".join(build(seed[edge_num],seed[edge_num+1],0))
    logger.info(f"{pname}:  finished for idx: {edge_num}")
    return {k:output.count(k) for k in rules}
    
    

def apply_rules(n:int,seed:str,rules:dict[str,dict[str,str]]):
    with cf.ProcessPoolExecutor() as ppe:
        ftrs = [ppe.submit(proc_applicator,n,i,seed,rules) for i in range(len(seed)-1)]
        results = {}
        for ftr in cf.as_completed(ftrs):
            result = ftr.result()
            for k,v in result.items():
                results[k] = results.setdefault(k,0) + v
    return results


def solve_part1(seed:str,rules:dict[str,dict[str,str]]):
    print(seed)
    counts = apply_rules(10,seed,rules)
    most = max(counts.items(),key=lambda tpl:tpl[1])
    least = min(counts.items(),key=lambda tpl:tpl[1])
    solution = most[1]-least[1]
    print(f"solve_part1: {solution}")
    dbg_break = 0


def solve_part2(seed:str,rules:dict[str,dict[str,str]]):
    counts = apply_rules(40, seed, rules)
    most = max(counts.items(), key=lambda tpl: tpl[1])
    least = min(counts.items(), key=lambda tpl: tpl[1])
    solution = most[1] - least[1]
    print(f"solve_part2: {solution}")
    dbg_break = 0


def main():
    input_data = parse_data(dummy_input)
    # input_data = parse_data(list(get_raw_data(__file__)))
    # solve_part1(*input_data)
    solve_part2(*input_data)
 

if __name__ == '__main__':
    main()

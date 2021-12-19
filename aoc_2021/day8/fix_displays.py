

from aoc_2021 import get_raw_data
from aoc_2021.day8 import dummy_data


"""

0: 6    1: 2    2: 5    3: 5    4: 4
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5: 5    6: 6    7: 3    8: 7    9: 6   
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
 
digits by length
2: 1
3: 7
4: 4
5: 2, 3, 5
6: 0, 6, 9
7: 8   
 
digits identified by seq len
 1:         4:           7:         8:  
 ....        ....       aaaa       aaaa 
.    c      b    c     .    c     b    c
.    c      b    c     .    c     b    c
 ....        dddd       ....       dddd 
.    f      .    f     .    f     e    f
.    f      .    f     .    f     e    f
 ....        ....       ....       gggg 
 
 
 digits that contain complement parts to 1,4, and 7
 Notes: 
    * once these are identified we can single out digit 2 by its length
    * with 2 gone, we can identify 0 from 6 because 0 is a superset of 7
    * by elimination, this leaves 6
 0: 6        2: 5        6: 6
 aaaa        aaaa       aaaa 
b    c      .    c     b    .
b    c      .    c     b    .
 ....        dddd       dddd 
e    f      e    .     e    f
e    f      e    .     e    f
 gggg        gggg       gggg 
 
All we need to identify next is 3, and 5
Notes:
   * Because 3 and 5 take signals c, and b (respectively), we can identify them by 
     comparing them to 2.
  * 3 shares 4 segments with 2
  * 5 shares 3 segments with 2
  * thus, we measure the intersection of their sets.
3: 6          5: 5
 aaaa        aaaa 
.    c      b    .
.    c      b    .
 dddd        dddd 
.    f      .    f
.    f      .    f
 gggg        gggg 
"""

#                    0 1 2 3 4 5 6 7 8 9
segments_per_digit = 6,2,5,5,4,5,6,3,7,6
unique_pattern_lens = {
    2:1,
    4:4,
    3:7,
    7:8,
}

sort_map = {}

class SignalSetV2:

    def __init__(self,signals,outputs) -> None:
        self.signals = signals
        self.outputs = outputs
        self.output_lens = tuple(len(self.signals[k]) for k in self.outputs)
        self.length_matches = sum(k in unique_pattern_lens for k in self.output_lens)
        self.solved = {}

        self.output_int = 0
        self.output_str = None

    def translate(self):
        length_based = {}
        for k in self.signals:
            lk = len(k)
            length_based.setdefault(lk,[]).append(k)
        digit_map = {
            0: None,
            1: length_based[2][0],
            2: None,
            3: None,
            4: length_based[4][0],
            5: None,
            6: None,
            7: length_based[3][0],
            8: length_based[7][0],
            9: None,
        }
        _026 = list(set("abcdefg")-set(_v for v in (val for val in digit_map.values() if val is not None and len(val)!=7) for _v in v))
        for fs in self.signals:
            if len(fs)<7 and all(s in fs for s in _026):
                if len(fs) == 5:
                    # 2
                    digit_map[2] = fs
                elif all(s in fs for s in digit_map[1]):
                    # 0
                    digit_map[0] = fs
                else:
                    # 6
                    digit_map[6] = fs
        solved_set = set(v for v in digit_map.values() if v is not None)
        for fs in self.signals:
            if fs not in solved_set:
                if len(fs)==6:
                    digit_map[9] = fs
                elif len(fs)==5:
                    # 3 or 5
                    if sum(v in digit_map[2] for v in fs)==4:
                        # 3
                        digit_map[3] = fs
                    else:
                        # 5
                        digit_map[5] = fs
        dbg_break = 0
        self.solved["digit2str"] = digit_map
        self.solved["str2digit"] = {
            v:k for k,v in digit_map.items()
        }
        self.solved["output"] = [
            self.solved["str2digit"][self.signals[k]] for k in self.outputs
        ]
        self.output_str = "".join((str(d) for d in self.solved["output"]))
        self.output_int = int(self.output_str)
        return self



def prep_data(raw):
    ret = []
    for line in raw:
        line = line.strip()
        if line:
            s1,s2 = map(str.strip,line.split("|"))
            s1 = tuple(map(frozenset,s1.split()))
            s2 = tuple(s1.index(frozenset(v)) for v in s2.split())
            ret.append(SignalSetV2(s1,s2))
    return ret

def solve_part1(data:list[SignalSetV2]):
    simple_matches = sum(sig.translate().length_matches for sig in data)
    print(f"solve_part1: {simple_matches=}")
    return data

def solve_part2(data:list[SignalSetV2]):
    output_sums = sum(sig.output_int for sig in data)
    print(f"solve_part2: {output_sums=}")


def main():
    # input_data = prep_data(dummy_data)
    input_data = prep_data(get_raw_data(__file__))
    solve_part2(solve_part1(input_data))

if __name__ == '__main__':
    main()
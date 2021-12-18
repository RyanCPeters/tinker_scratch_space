from pathlib import Path
import numpy as np

dummy_boards = [
    [
        [22, 13, 17, 11, 0],
        [8, 2, 23, 4, 24],
        [21, 9, 14, 16, 7],
        [6, 10, 3, 18, 5],
        [1, 12, 20, 15, 19],
    ],

    [
        [3, 15, 0, 2, 22],
        [9, 18, 13, 17, 5],
        [19, 8, 7, 25, 23],
        [20, 11, 10, 24, 4],
        [14, 21, 16, 12, 6],
    ],

    [
        [14, 21, 17, 24, 4],
        [10, 16, 15, 9, 19],
        [18, 8, 23, 26, 20],
        [22, 11, 13, 6, 5],
        [2, 0, 12, 3, 7],
    ]
]

dummy = [
    [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1],
    np.asarray(dummy_boards, int)
]


def get_data():
    here = Path(__file__).parent
    lines = map(str.strip, here.joinpath("input.txt").read_text().splitlines())
    draws = tuple(map(int, next(lines).split(",")))
    boards = []
    for line in lines:
        if not line:
            boards.append([])
        else:
            boards[-1].append(tuple(map(int, line.split())))
    ret = np.asarray(boards)
    return draws, ret


def solve_part1(draws:list[int], boards: np.ndarray, announce:bool=True):
    mask = np.zeros_like(boards, dtype=bool)
    pos = 0
    for num in draws:
        mask |= boards == num
        column_check = mask.all(axis=1,keepdims=True)
        row_check = mask.all(axis=2,keepdims=True)
        if row_check.any(axis=0, keepdims=True).any():
            nonzeros = tuple(a[0] for a in np.nonzero(row_check))
            break
        if column_check.any(axis=0, keepdims=True).any():
            nonzeros = tuple(a[0] for a in np.nonzero(column_check))
            break
        pos += 1
    final_draw = draws[pos]
    winner_sum = boards[nonzeros[0]][~mask[nonzeros[0]]].sum()
    if announce:
        print(f"part 1 solution: {winner_sum=}, {final_draw=}, product={winner_sum*final_draw}")
    return pos,nonzeros[0],winner_sum,final_draw

def solve_part2(draws:list[int], boards:np.ndarray):
    for _ in range(boards.shape[0]-1):
        _,drop,_,_ = solve_part1(draws,boards,False)
        boards[drop] *= -1
    _,_,winner_sum,final_draw = solve_part1(draws, boards, False)
    print(f"part 2 solution: {winner_sum=}, {final_draw=}, product={winner_sum*final_draw}")
    dbg_break = 0


def main():
    input_data = get_data()
    solve_part1(*input_data)
    solve_part2(*input_data)
    # print(solve_part2(input_data))


if __name__ == '__main__':
    main()

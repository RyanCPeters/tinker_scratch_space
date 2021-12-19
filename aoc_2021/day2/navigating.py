from pathlib import Path

class Position:

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.mapping = {
            "forward":self.forward,
            "up":self.up,
            "down":self.down
        }
        self.instructions = []

    def forward(self,val):
        self.x += val

    def up(self,val):
        self.y -= val

    def down(self,val):
        self.y += val

    def update(self,inpt_str):
        func,val = inpt_str.strip().split()
        val = int(val)
        self.mapping[func](val)
        self.instructions.append((func,val))

    def follow_instructions(self,data):
        for line in data:
            self.update(line.strip())

    def compute_travel_area(self):
        return self.x*self.y

class Position2(Position):
    def __init__(self, data=None) -> None:
        super().__init__()
        self.aim = 0
        if data:
            for f,v in data:
                self.mapping[f](v)

    def up(self,val):
        self.aim -= val

    def down(self,val):
        self.aim += val

    def forward(self,val):
        super(Position2, self).forward(val)
        self.y += self.aim*val

def get_data():
    here = Path(__file__).parent
    return map(str.strip, here.joinpath("input.txt").read_text().splitlines())

def solve_part1(pos,data):
    pos.follow_instructions(data)
    print(f"part 1 solution: {pos.compute_travel_area()}")

def solve_part2(pos):
    pos2 = Position2(pos.instructions)
    print(f"part 2 solution: {pos2.compute_travel_area()}")

# def solve_part2(data):
#     iter1 = (v1+v2+v3 for v1,v2,v3 in zip(data,data[1:],data[2:]))
#     iter2 = (v1+v2+v3 for v1,v2,v3 in zip(data[1:],data[2:],data[3:]))
#     return sum(v1<v2 for v1,v2 in zip(iter1,iter2))

def main():
    input_data = get_data()
    position = Position()
    solve_part1(position,input_data)
    solve_part2(position)
    # print(solve_part2(input_data))

if __name__ == '__main__':
    main()
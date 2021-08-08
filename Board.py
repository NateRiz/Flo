import os


class Point:
    def __init__(self, x, y, id_):
        self.id = id_
        self.coord = (y, x)
        self.pair = None

    def assign_pair(self, point):
        self.pair = point

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)


class Board:
    def __init__(self, file_name):
        self.board = []
        self.pairs = {}
        self.load_board_from_file(file_name)
        self.ids = list(self.pairs.keys())

    def solve_board(self):
        char = self.ids.pop()
        point = self.pairs[char][0]
        self.solve_pair(point)
        self.ids.append(char)

    def solve_pair(self, point):
        self._solve_pair(point, point.pair, point.coord)

    def _solve_pair(self, src, dst, coord):
        print(self)
        dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for i, j in dirs:
            y = coord[0] + j
            x = coord[1] + i
            if 0 <= x < len(self.board) and 0 <= y < len(self.board):
                if (y, x) == dst.coord:
                    self.solve_board()
                elif self.board[y][x] is None:
                    error = False
                    for n, m in dirs:
                        a, b = y + m, x + n
                        if a < 0 or a >= len(self.board) or b < 0 or b >= len(self.board):
                            continue
                        if self.board[a][b] == src.id and (a, b) != coord and (a, b) != dst.coord:
                            error = True
                            break

                    if error:
                        continue
                    self.board[y][x] = src.id
                    self._solve_pair(src, dst, (y, x))
                    self.board[y][x] = None

    def load_board_from_file(self, file_name):
        path = os.path.join(os.getcwd(), "Boards", file_name)
        with open(path, "r") as file:
            for y, line in enumerate(file):
                line = [x.lower() for x in line.strip()]
                self.board.append(list())
                for x, char in enumerate(line):
                    if char == "o":
                        self.board[-1].append(None)
                    else:
                        point = Point(x, y, char)
                        self.board[-1].append(point)
                        if char not in self.pairs:
                            self.pairs[char] = []
                        self.pairs[char].append(point)
        self.validate_board()
        for points in self.pairs.values():
            a, b = points
            a.assign_pair(b)
            b.assign_pair(a)

    def validate_board(self):
        length = len(self.board)
        for i in self.board:
            assert len(i) == length, f"Board must be a square. Found {length} x {len(i)}"
        for key, points in self.pairs.items():
            assert len(points) == 2, f"Board needs exactly two of each dot. Found {len(points)} with ID {key}"

    def __str__(self):
        res = ""
        for row in self.board:
            res += " ".join([str(i) if i else "_" for i in row]) + "\n"
        return res

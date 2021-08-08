from BoardImporter import BoardImporter


class Board:
    def __init__(self, file_name):
        self.board, self.pairs = BoardImporter.load_board_from_file(file_name)
        self.ids = sorted(list(self.pairs.keys()), key=lambda p: self.pairs[p][0].distance, reverse=True)
        self.neighbors = self._construct_neighbors()

    def solve_board(self):
        char = self.ids.pop()
        point = self.pairs[char][0]
        self._solve_pair(point)
        self.ids.append(char)

    def _solve_pair(self, point):
        self._solve_pair_helper(point, point.pair, point.coord)

    def _solve_pair_helper(self, src, dst, coord):
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
                    for a, b in dirs:
                        ya, xb = y + a, x + b
                        if 0 <= ya < len(self.board) and 0 <= xb < len(self.board):
                            self.neighbors[ya][xb] -= 1
                            assert self.neighbors[ya][xb] >= 0
                    self._solve_pair_helper(src, dst, (y, x))
                    self.board[y][x] = None
                    for a, b in dirs:
                        ya, xb = y + a, x + b
                        if 0 <= ya < len(self.board) and 0 <= xb < len(self.board):
                            self.neighbors[ya][xb] += 1
                            assert self.neighbors[ya][xb] <= 4

    def _construct_neighbors(self):
        res = [[4] * len(self.board) for _ in range(len(self.board))]
        dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for i in range(len(res)):
            for j in range(len(res[i])):
                specials = sum([i == 0, j == 0, i == (len(self.board) - 1), j == (len(self.board) - 1)])
                if specials == 1:
                    res[j][i] = 3
                if specials == 2:
                    res[j][i] = 2

        for a, b in self.pairs.values():
            ay, ax = a.coord
            by, bx = b.coord
            for i, j in dirs:
                if 0 <= ay + i < len(self.board) and 0 <= ax + j < len(self.board):
                    res[ay + i][ax + j] -= 1
                if 0 <= by + i < len(self.board) and 0 <= bx + j < len(self.board):
                    res[by + i][bx + j] -= 1

        return res

    def __str__(self):
        res = ""
        for row in self.board:
            res += " ".join([str(i).lower() if i else "_" for i in row]) + "\n"
        print()
        [print(i) for i in self.neighbors]
        print()
        return res

from BoardImporter import BoardImporter


class Board:
    def __init__(self, file_name):
        self.board, self.pairs = BoardImporter.load_board_from_file(file_name)
        self.ids = set(self.pairs.keys())

    def solve_board(self):
        for char in self.ids:
            point = self.pairs[char][0]
            self.solve_pair(point.coord)

    def solve_pair(self, coord):
        print(self)
        dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for i, j in dirs:
            y = coord[0] + j
            x = coord[1] + i
            if 0 <= x < len(self.board) and 0 <= y < len(self.board):
                if self.board[y][x] is None:
                    self.board[y][x] = self.board[coord[0]][coord[1]]
                    self.solve_pair((y, x))
                    self.board[y][x] = None

    def __str__(self):
        res = ""
        for row in self.board:
            res += "".join([str(i) if i else "_" for i in row]) + "\n"
        return res

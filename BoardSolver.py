from time import time


class BoardSolver:
    def __init__(self, board):
        self.start = time()
        self.board = board
        self.ids = list(board.pairs.keys())

    def solve(self):
        if not self.ids:
            duration = time() - self.start
            print(self.board)
            print(F"Finished in {duration} seconds")
            exit(0)

        char = self.ids.pop()
        point = self.board.pairs[char][0]
        self._solve_pair(point)
        self.ids.append(char)

    def _solve_pair(self, point):
        print(point)
        print(self.board)

        for n in point.get_available_moves():  # type: Point
            if point.is_matching_pair(n):
                self.set_all_colors_connected(point.id, True)
                self.solve()
                self.set_all_colors_connected(point.id, False)
                return
            n.take_space(point)
            self._solve_pair(n)
            n.clear_space()

    def set_all_colors_connected(self, id_, is_connected):
        return
        for row in self.board:
            for point in row:
                if point.id == id_:
                    point.is_connected = is_connected


class BoardSolver:
    def __init__(self, board):
        self.board = board
        self.ids = sorted(list(board.pairs.keys()), key=lambda p: board.pairs[p][0].distance, reverse=True)

    def solve(self):
        char = self.ids.pop()
        point = self.board.pairs[char][0]
        self._solve_pair(point)
        self.ids.append(char)

    def _solve_pair(self, point):
        print(self.board)

        for n in point.get_neighbors():
            if point.is_matching_pair(n):
                self.solve()
                return
            elif n.is_empty():
                n.take_space(point)
                self._solve_pair(n)
                n.clear_space()
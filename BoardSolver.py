from time import time


class BoardSolver:
    def __init__(self, board):
        self.start = time()
        self.board = board
        self.ids = sorted(list(board.pairs.keys()), key=lambda p: board.pairs[p][0].distance, reverse=True)

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
        #print(self.board)

        for n in point.get_neighbors():
            if point.is_matching_pair(n):
                self.solve()
                return
            elif n.is_empty():
                valid = n.try_take_space(point)
                if valid:
                    self._solve_pair(n)
                    n.clear_space()
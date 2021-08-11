from Board import Board
from BoardSolver import BoardSolver


def main():
    board8x8 = Board("8x8.flo")
    board7x7 = Board("7x7.png")
    board13x13 = Board("13x13.png")
    solver = BoardSolver(board13x13)
    solver.solve()


if __name__ == '__main__':
    main()
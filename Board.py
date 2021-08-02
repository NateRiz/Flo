import os


class Point:
    def __init__(self, x, y, id):
        self.id = id
        self.coord = (y, x)


class Board:
    def __init__(self, file_name):
        self.board = []
        path = os.path.join(os.getcwd(), "Boards", file_name)
        with open(path, "r") as file:
            for line in file:
                line = [x.lower() for x in line.strip()]
                self.board.append(list(line))



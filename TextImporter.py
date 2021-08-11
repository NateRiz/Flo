from ImportableType import ImportableType
from Point import Point


class TextImporter(ImportableType):
    def __init__(self):
        super().__init__()

    def load(self, file_name):
        with open(file_name, "r") as file:
            for y, line in enumerate(file):
                line = [x.lower() for x in line.strip()]
                self.board.append(list())
                for x, char in enumerate(line):
                    if char == "o":
                        self.board[-1].append(Point(x, y, None))
                    else:
                        point = Point(x, y, char)
                        self.board[-1].append(point)
                        if char not in self.pairs:
                            self.pairs[char] = []
                        self.pairs[char].append(point)

        self._populate_point_info()
        return self.board, self.pairs

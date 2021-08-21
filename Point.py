class Point:
    def __init__(self, x, y, id_):
        self.id = id_
        self.coord = (y, x)
        self.pair = None
        self.distance = -1
        self.N = None
        self.E = None
        self.S = None
        self.W = None
        self.source = None
        self.is_connected = False

    @property
    def num_neighbors(self):
        return sum((bool(self.N and self.N.id), bool(self.E and self.E.id), bool(self.S and self.S.id),
                    bool(self.W and self.W.id)))

    def num_empty_neighbors(self):
        return sum((bool(self.N and not self.N.id), bool(self.E and not self.E.id), bool(self.S and not self.S.id),
                    bool(self.W and not self.W.id)))

    def is_empty(self):
        return self.id is None

    def take_space(self, point):
        assert self.id is None

        self.source = point.source
        self.pair = point.pair
        self.id = point.id
        return True

    def clear_space(self):
        assert self.id is not None
        self.source = None
        self.pair = None
        self.id = None

    def is_matching_pair(self, point):
        assert point is not None
        return self.pair == point.source

    def populate_info(self, board):
        self.source = self
        self.pair = self._find_pair_in_board(board)
        assert self.pair is not None
        self.distance = abs(self.pair.coord[0] - self.coord[0]) + abs(self.pair.coord[1] - self.coord[1])

        y, x = self.coord
        if y - 1 >= 0:
            self.N = board[y - 1][x]
        if x - 1 >= 0:
            self.W = board[y][x - 1]
        if y + 1 < len(board):
            self.S = board[y + 1][x]
        if x + 1 < len(board):
            self.E = board[y][x + 1]

    def get_neighbors(self):
        if self.N:
            yield self.N
        if self.E:
            yield self.E
        if self.S:
            yield self.S
        if self.W:
            yield self.W

    def get_available_moves(self):
        available = []
        for n in self.get_neighbors():  # type: Point
            valid = True
            # Can't move to a taken space unless its the destination
            if not n.is_empty():
                if self.is_matching_pair(n):
                    return [n]  # Must move to destination if you are able to
                else:
                    continue
            """
            empty_neighbors = n.num_empty_neighbors()

            # Probably not possible, but don't go into dead end.
            if empty_neighbors == 0:
                break

            elif empty_neighbors == 1:
                #  One empty neighbor means we must go down that path.
                if n.get_neighbors() == 0:
                    return [n]
                #  Unless it's touching a Dot. Then we cannot move there.
                else:
                    continue
            """

            #  Neighbor's neighbors
            for point in n.get_neighbors():  # type: Point
                # Don't move to neighbor spots that touch the same color
                if point is not self and self.source == point.source:
                    valid = False
                    break

            if not valid:
                continue

            available.append(n)
        return available

    def _find_pair_in_board(self, board):
        for row in board:
            for i in row:
                if i.id == self.id and i.coord != self.coord:
                    return i
        return None

    def __str__(self):
        return self.id if self.id else "_"

    def __repr__(self):
        return F"{self.id} {self.coord}"

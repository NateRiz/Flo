class Point:
    def __init__(self, x, y, id_):
        self.id = id_
        self.coord = (y, x)
        self.pair = None
        self.distance = -1

    def assign_pair(self, point):
        self.pair = point
        self.distance = abs(point.coord[0] - self.coord[0]) + abs(point.coord[1] - self.coord[1])

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)

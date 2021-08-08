class Point:
    def __init__(self, x, y, id_):
        self.id = id_
        self.coord = (y, x)
        self.pair = None

    def assign_pair(self, point):
        self.pair = point

    def __str__(self):
        return self.id

    def __repr__(self):
        return str(self)

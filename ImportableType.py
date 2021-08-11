from abc import abstractmethod, ABC


class ImportableType(ABC):
    def __init__(self):
        self.board = []
        self.pairs = {}

    @abstractmethod
    def load(self, file_name):
        pass

    def _populate_point_info(self):
        for row in self.board:
            for point in row:
                point.populate_info(self.board)



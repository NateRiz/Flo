from BoardImporter import BoardImporter


class Board:
    def __init__(self, file_name):
        self.board, self.pairs = BoardImporter.load_board_from_file(file_name)

    def __str__(self):
        res = ""
        for row in self.board:
            res += "  ".join([str(i).lower() if i else "_" for i in row]) + "\n"

        """
        print()
        for row in self.board:
            for i in row:
                print(i.num_neighbors, end=" ")
            print()
        print()
        """
        return res

from PictureImporter import PictureImporter
from TextImporter import TextImporter
import os
debug = 0


class BoardImporter:

    @staticmethod
    def load_board_from_file(file_name):
        path = os.path.join(os.getcwd(), "Boards", file_name)
        file_name = file_name.lower()
        if file_name.endswith(".flo") or file_name.endswith(".txt"):
            importer = TextImporter()
        elif file_name.endswith(".png"):
            importer = PictureImporter()
        else:
            raise RuntimeError("Can't import non flo/txt/png")

        board, pairs = importer.load(path)
        BoardImporter._validate_board(board, pairs)
        return board, pairs

    @staticmethod
    def _validate_board(board, pairs):
        length = len(board)
        for i in board:
            assert len(i) == length, f"Board must be a square. Found {length} x {len(i)}"
        for key, points in pairs.items():
            assert len(points) == 2, f"Board needs exactly two of each dot. Found {len(points)} with ID {key}"

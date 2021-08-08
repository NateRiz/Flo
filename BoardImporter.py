from Point import Point
from PIL import Image
import os
from queue import Queue
debug = 0


class BoardImporter:
    debug_img = None

    @staticmethod
    def load_board_from_file(file_name):
        path = os.path.join(os.getcwd(), "Boards", file_name)
        if file_name.endswith(".flo") or file_name.endswith(".txt"):
            return BoardImporter._load_board_from_txt(path)
        elif file_name.endswith(".png"):
            return BoardImporter._load_board_from_png(path)
        else:
            raise RuntimeError("Can't import non flo/txt/png")

    @staticmethod
    def _load_board_from_png(file_name):
        img = Image.open(file_name).convert("RGB")
        if debug:
            BoardImporter.debug_img = img.copy()
        width, height = img.size
        y = height // 2
        grid_pixel = -1
        while y > 0:
            rgb = img.getpixel((width//2, y))
            if rgb_is_bright(rgb):
                left = img.getpixel((width//4, y))
                right = img.getpixel(((3 * width) // 4, y))
                if rgb_almost_equals(rgb, left) and rgb_almost_equals(rgb, right):
                    grid_pixel = y
                    break
            y -= 1

        if grid_pixel == -1:
            raise RuntimeError("Couldn't find grid in image.")

        cols, rows = BoardImporter._bfs_grid(img, y)
        sq_size = cols[1] - cols[0]
        cols.append(cols[-1] + sq_size)
        rows.append(rows[-1] + sq_size)
        cols.insert(0, cols[0] - sq_size)
        rows.insert(0, rows[0] - sq_size)

        board = [[None]*(len(cols)-1) for _ in range(len(rows)-1)]
        circles = {}
        pairs = {}

        dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for c in range(len(cols)-1):
            for r in range(len(rows) - 1):
                x = (cols[c] + cols[c + 1]) // 2
                y = (rows[r] + rows[r + 1]) // 2
                avg_rgb = list(img.getpixel((x, y)))
                for i, j in dirs:
                    if debug:
                        BoardImporter.debug_img.putpixel((x+i, y+j), (255, 255, 255))
                    rgb = img.getpixel((x+i, y+j))
                    for idx in range(len(rgb)):
                        avg_rgb[idx] += rgb[idx] // (len(dirs) + 1)

                if rgb_is_bright(avg_rgb):
                    is_pair = False
                    for k, v in circles.items():
                        if rgb_almost_equals(v, avg_rgb):
                            pairs[k].append(Point(c, r, k))
                            is_pair = True
                            board[r][c] = k
                            break
                    if not is_pair:
                        id_ = chr(len(pairs) + 65)
                        circles[id_] = avg_rgb
                        pairs[id_] = [Point(c, r, id_)]
                        board[r][c] = id_

        if debug:
            [print(i) for i in board]
            BoardImporter.debug_img.show()

        BoardImporter._validate_board(board, pairs)
        BoardImporter._create_pairs(pairs)

        return board, pairs

    @staticmethod
    def _bfs_grid(img, y):
        x = img.size[0]//2
        queue = Queue()
        queue.put((x, y))
        seen = set()
        seen.add((x, y))
        intersections = set()
        while queue.qsize():
            x, y = queue.get()
            is_intersection = True
            original_rgb = img.getpixel((x, y))
            if debug:
                BoardImporter.debug_img.putpixel((x, y), (0, 255, 0))
            dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
            for i, j in dirs:
                xi = x + i
                yj = y + j
                if 0 <= xi < img.size[0] and 0 <= yj < img.size[1]:
                    rgb = img.getpixel((xi, yj))
                    if rgb_almost_equals(original_rgb, rgb) and (xi, yj) not in seen:
                        seen.add((xi, yj))
                        queue.put((xi, yj))
                xi = x + i * 10
                yj = y + j * 10
                if is_intersection:
                    if not (0 <= xi < img.size[0] and 0 <= yj < img.size[1]):
                        is_intersection = False
                    else:
                        rgb = img.getpixel((xi, yj))
                        if not rgb_almost_equals(original_rgb, rgb):
                            is_intersection = False
            if is_intersection:
                if debug:
                    BoardImporter.debug_img.putpixel((x, y), (255, 0, 0))
                intersections.add((x, y))

        return BoardImporter._get_lines_far_apart(intersections)

    @staticmethod
    def _get_lines_far_apart(nums):
        def helper(_nums):
            start = 0
            res = []
            for i in range(1, len(_nums)):
                if _nums[i] != _nums[i - 1] + 1:
                    res.append((_nums[start] + _nums[i - 1]) // 2)
                    start = i
            res.append((_nums[start] + _nums[-1]) // 2)
            return res
        x = sorted(list(set([i[0] for i in nums])))
        y = sorted(list(set([i[1] for i in nums])))

        return helper(x), helper(y)

    @staticmethod
    def _load_board_from_txt(file_name):
        board = []
        pairs = {}
        with open(file_name, "r") as file:
            for y, line in enumerate(file):
                line = [x.lower() for x in line.strip()]
                board.append(list())
                for x, char in enumerate(line):
                    if char == "o":
                        board[-1].append(None)
                    else:
                        point = Point(x, y, char)
                        board[-1].append(point)
                        if char not in pairs:
                            pairs[char] = []
                        pairs[char].append(point)

        BoardImporter._validate_board(board, pairs)
        BoardImporter._create_pairs(pairs)

        return board, pairs

    @staticmethod
    def _create_pairs(pairs):
        for points in pairs.values():
            a, b = points
            a.assign_pair(b)
            b.assign_pair(a)

    @staticmethod
    def _validate_board(board, pairs):
        length = len(board)
        for i in board:
            assert len(i) == length, f"Board must be a square. Found {length} x {len(i)}"
        for key, points in pairs.items():
            assert len(points) == 2, f"Board needs exactly two of each dot. Found {len(points)} with ID {key}"


def rgb_almost_equals(a, b):
    for i, j in zip(a, b):
        if abs(i - j) > 20:
            return False
    return True


def rgb_is_bright(rgb):
    white = 255 * 3
    return sum(rgb) > white * 0.2

from ImportableType import ImportableType
from RGBUtils import *
from Point import Point
from PIL import Image
from queue import Queue


class PictureImporter(ImportableType):
    def __init__(self):
        super().__init__()
        self.debug = 0
        self.debug_img = None

    def load(self, file_name):
        img = Image.open(file_name).convert("RGB")
        if self.debug:
            self.debug_img = img.copy()
        width, height = img.size
        y = height // 2
        grid_pixel = -1
        while y > 0:
            rgb = img.getpixel((width // 2, y))
            if rgb_is_bright(rgb):
                left = img.getpixel((width // 4, y))
                right = img.getpixel(((3 * width) // 4, y))
                if rgb_almost_equals(rgb, left) and rgb_almost_equals(rgb, right):
                    grid_pixel = y
                    break
            y -= 1

        if grid_pixel == -1:
            raise RuntimeError("Couldn't find grid in image.")

        cols, rows = self._bfs_grid(img, y)
        sq_size = cols[1] - cols[0]
        cols.append(cols[-1] + sq_size)
        rows.append(rows[-1] + sq_size)
        cols.insert(0, cols[0] - sq_size)
        rows.insert(0, rows[0] - sq_size)

        self.board = [[None] * (len(cols) - 1) for _ in range(len(rows) - 1)]
        circles = {}

        dirs = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for c in range(len(cols) - 1):
            for r in range(len(rows) - 1):
                x = (cols[c] + cols[c + 1]) // 2
                y = (rows[r] + rows[r + 1]) // 2
                avg_rgb = list(img.getpixel((x, y)))
                for i, j in dirs:
                    if self.debug:
                        self.debug_img.putpixel((x + i, y + j), (255, 255, 255))
                    rgb = img.getpixel((x + i, y + j))
                    for idx in range(len(rgb)):
                        avg_rgb[idx] += rgb[idx] // (len(dirs) + 1)

                point = Point(c, r, None)
                if rgb_is_bright(avg_rgb):
                    is_pair = False
                    for k, v in circles.items():
                        if rgb_almost_equals(v, avg_rgb):
                            point = Point(c, r, k)
                            self.pairs[k].append(point)
                            is_pair = True
                            break

                    if not is_pair:
                        id_ = chr(len(self.pairs) + 65)
                        circles[id_] = avg_rgb
                        point = Point(c, r, id_)
                        self.pairs[id_] = [point]

                self.board[r][c] = point


        if self.debug:
            [print(i) for i in self.board]
            self.debug_img.show()

        self._populate_point_info()
        return self.board, self.pairs

    def _bfs_grid(self, img, y):
        x = img.size[0] // 2
        queue = Queue()
        queue.put((x, y))
        seen = set()
        seen.add((x, y))
        intersections = set()
        while queue.qsize():
            x, y = queue.get()
            is_intersection = True
            original_rgb = img.getpixel((x, y))
            if self.debug:
                self.debug_img.putpixel((x, y), (0, 255, 0))
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
                if self.debug:
                    self.debug_img.putpixel((x, y), (255, 0, 0))
                intersections.add((x, y))

        return self._get_lines_far_apart(intersections)

    def _get_lines_far_apart(self, nums):
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


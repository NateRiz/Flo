def rgb_almost_equals(a, b):
    for i, j in zip(a, b):
        if abs(i - j) > 20:
            return False
    return True


def rgb_is_bright(rgb):
    white = 255 * 3
    return sum(rgb) > white * 0.2
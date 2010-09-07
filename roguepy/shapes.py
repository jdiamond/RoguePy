# http://en.wikipedia.org/wiki/Bresenham's_line_algorithm
def line(start, stop):
    x0, y0 = start
    x1, y1 = stop
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x1 - x0 > 0 else -1
    sy = 1 if y1 - y0 > 0 else -1
    steep = False
    if dy > dx:
        x0, y0 = y0, x0
        dx, dy = dy, dx
        sx, sy = sy, sx
        steep = True
    error = dx // 2
    i = 0
    while i < dx:
        yield (y0, x0) if steep else (x0, y0)
        error -= dy
        if error < 0:
            y0 += sy
            error += dx
        x0 += sx
        i += 1
    yield (x1, y1)


# http://en.wikipedia.org/wiki/Midpoint_circle_algorithm
def circle(center, radius):
    x0, y0 = center
    f = 1 - radius
    sx = 1
    sy = -2 * radius
    x = 0
    y = radius

    yield (x0, y0 + radius)
    yield (x0, y0 - radius)
    yield (x0 + radius, y0)
    yield (x0 - radius, y0)

    while x < y:
        if f >= 0:
            y -= 1
            sy += 2
            f += sy
        x += 1
        sx += 2
        f += sx
        yield (x0 + x, y0 + y)
        yield (x0 - x, y0 + y)
        yield (x0 + x, y0 - y)
        yield (x0 - x, y0 - y)
        yield (x0 + y, y0 + x)
        yield (x0 - y, y0 + x)
        yield (x0 + y, y0 - x)
        yield (x0 - y, y0 - x)

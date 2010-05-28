class Grid:
    def __init__(self, width, height, default=None):
        self.width = width
        self.height = height
        self.rows = [[default for _ in range(width)] for _ in range(height)]

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)

    def __getitem__(self, point):
        x, y = point
        return self.rows[y][x]

    def __setitem__(self, point, value):
        x, y = point
        self.rows[y][x] = value

    def fill(self, value):
        for row in self.rows:
            for i in range(len(row)):
                row[i] = value

    def set_points(self, points, value):
        for point in points:
            self[point] = value


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
    ddF_x = 1
    ddF_y = -2 * radius
    x = 0
    y = radius

    yield (x0, y0 + radius)
    yield (x0, y0 - radius)
    yield (x0 + radius, y0)
    yield (x0 - radius, y0)

    while x < y:
        if f >= 0:
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x
        yield (x0 + x, y0 + y)
        yield (x0 - x, y0 + y)
        yield (x0 + x, y0 - y)
        yield (x0 - x, y0 - y)
        yield (x0 + y, y0 + x)
        yield (x0 - y, y0 + x)
        yield (x0 + y, y0 - x)
        yield (x0 - y, y0 - x)


def cast_rays(grid, origin, radius):
    for i in range(grid.width):
        cast_ray(origin, (i, 0), radius)
        cast_ray(origin, (i, grid.height - 1), radius)
    for i in range(1, grid.height - 1):
        cast_ray(origin, (0, i), radius)
        cast_ray(origin, (grid.width - 1, i), radius)

def cast_ray(start, end, radius):
    points = line(start, end)
    for point in points:
        if not in_circle(start, radius, point):
            break
        tile = grid[point]
        if tile == '#':
            break
        elif tile != '@':
            grid[point] = '.'

def in_circle(center, radius, point):
    center_x, center_y = center
    x, y = point
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


if __name__ == '__main__':
    grid = Grid(20, 20, ' ')
    player = (9, 10)
    grid[player] = '@'
    grid[10, 10] = '#'
    #grid.set_points(circle(player, 5), '*')
    cast_rays(grid, player, 5.5)
    print(grid)


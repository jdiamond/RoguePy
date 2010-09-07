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

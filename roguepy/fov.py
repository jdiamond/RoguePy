from roguepy.grid import *
from roguepy.shapes import *


def cast_rays(grid, origin, radius):
    if radius and radius == int(radius):
        # The circles are jagged if you don't adjust them like this.
        radius += 0.5
    for i in range(grid.width):
        cast_ray(origin, (i, 0), radius)
        cast_ray(origin, (i, grid.height - 1), radius)
    for i in range(1, grid.height - 1):
        cast_ray(origin, (0, i), radius)
        cast_ray(origin, (grid.width - 1, i), radius)


def cast_ray(start, end, radius):
    points = line(start, end)
    for point in points:
        if radius and not in_circle(start, radius, point):
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
    cast_rays(grid, player, 5)
    print(grid)

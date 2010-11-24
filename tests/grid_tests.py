import unittest
import test_helper
from roguepy.grid import Grid

class GridTests(unittest.TestCase):

    def test_it_sets_width_and_height_properties(self):
        width, height = 1, 2
        grid = Grid(width, height)

        self.assertEqual(grid.width, width)
        self.assertEqual(grid.height, height)

    def test_it_sets_all_cells_to_None_if_no_value_is_specified(self):
        width, height = 1, 2
        grid = Grid(width, height)

        self._assert_all_cells_equal(grid, None)

    def test_it_sets_all_cells_to_the_specified_value(self):
        width, height = 1, 2
        value = 'foo'
        grid = Grid(width, height, value)

        self._assert_all_cells_equal(grid, value)

    def test_it_lets_you_set_and_get_values_like_a_list(self):
        grid = Grid(2, 2)

        x, y = 0, 1
        value = 'foo'
        grid[x, y] = value

        self.assertEqual(grid[x, y], value)

    def test_it_can_represent_itself_as_a_string(self):
        grid = Grid(2, 2)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'
        grid[0, 1] = 'c'; grid[1, 1] = 'd'

        s = str(grid)

        self.assertEqual(s, "ab\ncd")

    def test_it_converts_None_to_spaces_in_the_string_representation(self):
        grid = Grid(2, 2)
        grid[0, 0] = 'a';  grid[1, 0] = None
        grid[0, 1] = None; grid[1, 1] = 'd'

        s = str(grid)

        self.assertEqual(s, "a \n d")

    def test_it_lets_you_fill_the_whole_grid_with_a_value(self):
        grid = Grid(2, 2)
        value = 'foo'

        grid.fill(value)

        self._assert_all_cells_equal(grid, value)

    def test_it_returns_no_neighbors_for_a_1x1_grid(self):
        grid = Grid(1, 1)

        neighbors = grid.get_neighbors((0, 0))

        self.assertEqual(neighbors, [])

    def test_it_returns_1_neighbor_for_a_2x1_grid_for_cell_0_0(self):
        grid = Grid(2, 1)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'

        neighbors = grid.get_neighbors((0, 0))

        self.assertEqual(neighbors, ['b'])

    def test_it_returns_2_neighbors_for_a_2x2_grid_for_cell_0_0(self):
        grid = Grid(2, 2)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'
        grid[0, 1] = 'c'; grid[1, 1] = 'd'

        neighbors = grid.get_neighbors((0, 0))

        self.assertEqual(neighbors, ['b', 'c'])

    def test_it_returns_2_neighbors_for_a_2x2_grid_for_cell_1_0(self):
        grid = Grid(2, 2)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'
        grid[0, 1] = 'c'; grid[1, 1] = 'd'

        neighbors = grid.get_neighbors((1, 0))

        self.assertEqual(neighbors, ['a', 'd'])

    def test_it_returns_2_neighbors_for_a_2x2_grid_for_cell_0_1(self):
        grid = Grid(2, 2)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'
        grid[0, 1] = 'c'; grid[1, 1] = 'd'

        neighbors = grid.get_neighbors((0, 1))

        self.assertEqual(neighbors, ['a', 'd'])

    def test_it_returns_2_neighbors_for_a_2x2_grid_for_cell_1_1(self):
        grid = Grid(2, 2)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'
        grid[0, 1] = 'c'; grid[1, 1] = 'd'

        neighbors = grid.get_neighbors((1, 1))

        self.assertEqual(neighbors, ['b', 'c'])

    def test_it_returns_3_neighbors_for_a_3x3_grid_for_cell_1_0(self):
        grid = Grid(3, 3)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'; grid[2, 0] = 'c'
        grid[0, 1] = 'd'; grid[1, 1] = 'e'; grid[2, 1] = 'f'
        grid[0, 2] = 'g'; grid[1, 2] = 'h'; grid[2, 2] = 'i'

        neighbors = grid.get_neighbors((1, 0))

        self.assertEqual(neighbors, ['a', 'c', 'e'])

    def test_it_returns_4_neighbors_for_a_3x3_grid_for_cell_1_1(self):
        grid = Grid(3, 3)
        grid[0, 0] = 'a'; grid[1, 0] = 'b'; grid[2, 0] = 'c'
        grid[0, 1] = 'd'; grid[1, 1] = 'e'; grid[2, 1] = 'f'
        grid[0, 2] = 'g'; grid[1, 2] = 'h'; grid[2, 2] = 'i'

        neighbors = grid.get_neighbors((1, 1))

        self.assertEqual(neighbors, ['b', 'd', 'f', 'h'])

    def _assert_all_cells_equal(self, grid, expected):
        for y in range(grid.height):
            for x in range(grid.width):
                self.assertEqual(grid[x, y], expected)

if __name__ == '__main__':
    unittest.main()

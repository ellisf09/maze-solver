import unittest

from main import Cell, Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_single_cell(self):
        m1 = Maze(0, 0, 1, 1, 10, 10)
        self.assertEqual(len(m1._Maze__cells), 1)
        self.assertEqual(len(m1._Maze__cells[0]), 1)

    def test_maze_create_cells_more_cols_than_rows(self):
        num_cols = 15
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        for column in m1._Maze__cells:
            self.assertEqual(len(column), num_rows)

    def test_maze_create_cells_more_rows_than_cols(self):
        num_cols = 4
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        for column in m1._Maze__cells:
            self.assertEqual(len(column), num_rows)

    def test_maze_create_cells_large(self):
        num_cols = 30
        num_rows = 20
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._Maze__cells), num_cols)
        self.assertEqual(
            sum(len(column) for column in m1._Maze__cells),
            num_cols * num_rows,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 7
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m1._Maze__cells[0][0].has_top_wall)
        self.assertFalse(
            m1._Maze__cells[num_cols - 1][num_rows - 1].has_bottom_wall
        )
        self.assertTrue(m1._Maze__cells[0][0].has_left_wall)
        self.assertTrue(
            m1._Maze__cells[num_cols - 1][num_rows - 1].has_right_wall
        )

    def test_cell_visited_starts_false(self):
        cell = Cell()
        self.assertFalse(cell.visited)

    def test_maze_reset_cells_visited(self):
        num_cols = 6
        num_rows = 4
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, seed=0)
        for column in m1._Maze__cells:
            for cell in column:
                self.assertFalse(cell.visited)

        for column in m1._Maze__cells:
            for cell in column:
                cell.visited = True

        m1._Maze__reset_cells_visited()

        for column in m1._Maze__cells:
            for cell in column:
                self.assertFalse(cell.visited)

    def test_maze_solve(self):
        m1 = Maze(0, 0, 8, 8, 10, 10, seed=0)
        self.assertTrue(m1.solve())

    def test_maze_solve_single_cell(self):
        m1 = Maze(0, 0, 1, 1, 10, 10, seed=0)
        self.assertTrue(m1.solve())

    def test_maze_same_seed_produces_same_walls(self):
        def wall_state(maze):
            state = []
            for column in maze._Maze__cells:
                for cell in column:
                    state.append((
                        cell.has_left_wall,
                        cell.has_right_wall,
                        cell.has_top_wall,
                        cell.has_bottom_wall,
                    ))
            return state

        m1 = Maze(0, 0, 6, 6, 10, 10, seed=0)
        m2 = Maze(0, 0, 6, 6, 10, 10, seed=0)
        m3 = Maze(0, 0, 6, 6, 10, 10, seed=1)
        self.assertEqual(wall_state(m1), wall_state(m2))
        self.assertNotEqual(wall_state(m1), wall_state(m3))

if __name__ == "__main__":
    unittest.main()

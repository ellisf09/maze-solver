from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y,
            fill=fill_color, width=2
        )

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("My Window")

        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)

        self.running = False

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Cell:
    def __init__(self, win: Window = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1.0
        self.__x2 = -1.0
        self.__y1 = -1.0
        self.__y2 = -1.0
        self.__win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.__win is None:
            return

        self.__win.draw_line(
            Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)),
            "black" if self.has_left_wall else "#d9d9d9"
        )
        self.__win.draw_line(
            Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)),
            "black" if self.has_right_wall else "#d9d9d9"
        )
        self.__win.draw_line(
            Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)),
            "black" if self.has_top_wall else "#d9d9d9"
        )
        self.__win.draw_line(
            Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)),
            "black" if self.has_bottom_wall else "#d9d9d9"
        )

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        self_center_x = (self.__x1 + self.__x2) / 2
        self_center_y = (self.__y1 + self.__y2) / 2
        to_center_x = (to_cell.__x1 + to_cell.__x2) / 2
        to_center_y = (to_cell.__y1 + to_cell.__y2) / 2
        fill_color = "gray" if undo else "red"
        if self.__win is None:
            return
        self.__win.draw_line(
            Line(
                Point(self_center_x, self_center_y),
                Point(to_center_x, to_center_y)
            ),
            fill_color
        )

class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: float,
        cell_size_y: float,
        win: Window = None,
        seed: int = None,
    ) -> None:
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        if seed is not None:
            random.seed(seed)
        self.__cells = []
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.__num_cols):
            column = []
            for j in range(self.__num_rows):
                column.append(Cell(self.__win))
            self.__cells.append(column)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            neighbors = []
            if i > 0 and not self.__cells[i - 1][j].visited:
                neighbors.append((i - 1, j))
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                neighbors.append((i + 1, j))
            if j > 0 and not self.__cells[i][j - 1].visited:
                neighbors.append((i, j - 1))
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                neighbors.append((i, j + 1))

            if len(neighbors) == 0:
                self.__draw_cell(i, j)
                return

            next_i, next_j = random.choice(neighbors)
            if next_i == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[next_i][next_j].has_right_wall = False
            elif next_i == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[next_i][next_j].has_left_wall = False
            elif next_j == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[next_i][next_j].has_bottom_wall = False
            elif next_j == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[next_i][next_j].has_top_wall = False

            self.__break_walls_r(next_i, next_j)

    def __reset_cells_visited(self):
        for column in self.__cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        return self.__solve_r(0, 0)

    def __solve_r(self, i, j):
        self.__animate()
        self.__cells[i][j].visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        if (
            i > 0
            and not self.__cells[i][j].has_left_wall
            and not self.__cells[i - 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self.__solve_r(i - 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i - 1][j], undo=True)

        if (
            i < self.__num_cols - 1
            and not self.__cells[i][j].has_right_wall
            and not self.__cells[i + 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self.__solve_r(i + 1, j):
                return True
            self.__cells[i][j].draw_move(self.__cells[i + 1][j], undo=True)

        if (
            j > 0
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self.__solve_r(i, j - 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j - 1], undo=True)

        if (
            j < self.__num_rows - 1
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self.__solve_r(i, j + 1):
                return True
            self.__cells[i][j].draw_move(self.__cells[i][j + 1], undo=True)

        return False

    def __draw_cell(self, i, j):
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        sleep(0.05)

def main():
    win = Window(800, 600)
    maze = Maze(50, 50, 3, 3, 100, 100, win)
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()

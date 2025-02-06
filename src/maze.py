import random
import time
from cell import Cell


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_width, cell_height, win=None, seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_width = cell_width
        self.cell_height = cell_height
        self._win = win
        self._cells = []

        if seed:
            random.seed(seed)

        self._create_cells()

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        def solve_move_to(n, m):
            self._cells[i][j].draw_move(self._cells[n][m])
            if self._solve_r(n, m):
                return True
            else:
                print("aqui")
                self._cells[i][j].draw_move(self._cells[n][m], True)

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        if (
            i + 1 < self.num_rows
            and not self._cells[i + 1][j].visited
            and not self._cells[i + 1][j].has_top_wall
        ):
            if solve_move_to(i + 1, j):
                return True

        if (
            j + 1 < self.num_cols
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j + 1].has_left_wall
        ):
            if solve_move_to(i, j + 1):
                return True

        if (
            i - 1 >= 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i - 1][j].has_bottom_wall
        ):
            if solve_move_to(i - 1, j):
                return True

        if (
            j - 1 >= 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j - 1].has_right_wall
        ):
            if solve_move_to(i, j - 1):
                return True

        return False

    def _create_cells(self):
        for i in range(self.num_rows):
            column = []
            for j in range(self.num_cols):
                x1 = self.x1 + j * self.cell_width
                x2 = x1 + self.cell_width
                y1 = self.y1 + i * self.cell_height
                y2 = y1 + self.cell_height
                cell = Cell(x1, x2, y1, y2, self._win)
                column.append(cell)
            self._cells.append(column)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        self._cells[i][j].draw()
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._draw_cell(0, 0)
        self._cells[self.num_rows - 1][self.num_cols - 1].has_right_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.015)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        while True:
            to_visit = []
            possible_neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

            for row, col in possible_neighbors:
                if 0 <= row < len(self._cells):
                    if 0 <= col < len(self._cells[row]):
                        if self._cells[row][col].visited is False:
                            to_visit.append((row, col))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            visiting = to_visit[random.randrange(len(to_visit))]

            if visiting == (i - 1, j):
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
            elif visiting == (i + 1, j):
                self._cells[i][j].has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
            elif visiting == (i, j - 1):
                self._cells[i][j].has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
            elif visiting == (i, j + 1):
                self._cells[i][j].has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False

            self._break_walls_r(visiting[0], visiting[1])

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

from UI.line import Line
from UI.point import Point


class Cell:
    def __init__(self, x1, x2, y1, y2, window=None):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._window = window
        self.visited = False
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self):
        if self._window is None:
            return
        self._window.draw_line(
            Line(Point(self._x1, self._y1), Point(self._x1, self._y2)),
            "purple" if self.has_left_wall else "white",
        )
        self._window.draw_line(
            Line(Point(self._x2, self._y1), Point(self._x2, self._y2)),
            "purple" if self.has_right_wall else "white",
        )
        self._window.draw_line(
            Line(Point(self._x1, self._y1), Point(self._x2, self._y1)),
            "purple" if self.has_top_wall else "white",
        )
        self._window.draw_line(
            Line(Point(self._x1, self._y2), Point(self._x2, self._y2)),
            "purple" if self.has_bottom_wall else "white",
        )

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"

        from_center = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        to_center = Point(
            (to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2
        )
        line = Line(from_center, to_center)

        self._window.draw_line(line, color)

from UI.window import Window
from maze import Maze


def main():
    win = Window(1280, 720)
    maze = Maze(390, 110, 10, 10, 50, 50, win)
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()

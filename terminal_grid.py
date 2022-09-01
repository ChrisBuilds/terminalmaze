import curses


class TermGrid:
    def __init__(self, screen: curses.window, height, width, fill=" "):
        self.screen = screen
        self.height = height
        self.width = width
        self.cells = {}  # (x,y) : value
        for y in range(height):
            for x in range(width):
                self.cells[(y, x)] = fill
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def show(self):
        max_y, max_x = self.screen.getmaxyx()
        self.screen.clear()
        for cell, value in self.cells.items():
            cell_y = cell[0]
            cell_x = cell[1]
            if cell_y <= max_y - 2 and cell_x <= max_x:
                self.screen.addch(cell_y, cell_x, value)
        self.screen.refresh()

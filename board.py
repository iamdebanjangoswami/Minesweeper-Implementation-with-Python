from cell import Cell
from constants import *
from functools import reduce
import random
import time
import _thread

# random.seed(0)


class Board:
    def __init__(self, w, h, num_mines, surface):
        self.width = h
        self.height = w
        self.gameover = False
        self.num_mines = min(num_mines, (self.width - 1) * (self.height - 1))
        self.num_flag = self.num_mines
        self.num_not_opened = w * h
        self.board = [[Cell(i, j) for i in range(self.width)] for j in range(self.height)]
        self.mines = random.sample(self.flat_board(), self.num_mines)
        self.surface = surface
        self.setup_mines()
        self.setup_neighbors()

    def flat_board(self):
        """Flatten 2-D board to 1-D array"""
        return reduce(lambda x, y: x + y, self.board)

    def setup_mines(self):
        """Set randomly chosen mines"""
        for cell in self.flat_board():
            if cell in self.mines:
                cell.set_mine(True)

    def check_win(self):
        """check for win"""
        return self.num_not_opened == self.num_mines

    def setup_neighbors(self):
        """Setup neighbor count for each cell"""
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col].is_mine():
                    # If the cell is_mine, then set neighbor count to -1
                    self.board[row][col].set_neighbors(-1)
                else:
                    # Not a mine, so count neighboring mines
                    total = 0
                    for row_off in [-1, 0, 1]:
                        y = row + row_off
                        for col_off in [-1, 0, 1]:
                            x = col + col_off
                            if 0 <= x < self.width and 0 <= y < self.height:
                                if self.board[y][x].is_mine():
                                    total += 1
                    self.board[row][col].set_neighbors(total)

    def render_frame(self):
        """render current frame"""
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col].draw(self.surface)

    def update_board(self, x, y, mousebutton):
        """
        change state of cells after each key event
        :param mousebutton: 1 = left, 3 = right
        :param x: mouseX
        :param y: mouseY
        """
        for col in range(self.width):
            for row in range(self.height):
                if self.board[row][col].clicked(x, y):
                    print(f"Clicked on cell: ({row},{col})")
                    if mousebutton == 1:
                        if self.board[row][col].is_mine():
                            self.gameover = True
                        # start flood fill in different thread so that we can have animation !
                        _thread.start_new_thread(self.flood_fill, (row, col))
                        if not self.board[row][col].is_revealed():
                            self.num_not_opened -= 1
                        self.board[row][col].toggle_state()
                        self.check_win()
                        return True
                    elif mousebutton == 3:
                        print(f"Flagging cell: ({row},{col})")
                        # flag mine!
                        if self.board[row][col].flagged:
                            # un-flag
                            self.board[row][col].flagged = False
                            self.num_flag += 1
                        elif self.num_flag > 0:
                            # flag mine
                            self.board[row][col].flagged = True
                            self.num_flag -= 1
                        return True
        return False

    def flood_fill(self, x, y):
        """flood fill to reveal nearby minefield"""
        for xoff in [-1, 0, 1]:
            i = x + xoff
            if i < 0 or i >= self.height:
                continue
            for yoff in [-1, 0, 1]:
                j = y + yoff
                if j < 0 or j >= self.width:
                    continue
                if not self.board[i][j].is_mine() and not self.board[i][j].is_revealed():
                    self.board[i][j].toggle_state()
                    self.num_not_opened -= 1
                    time.sleep(REVEAL_DELAY)
                    if self.board[i][j].get_neighbors() == 0:
                        self.flood_fill(i, j)

    def show(self):
        """print board to console"""
        for row in range(self.height):
            print("".join(map(str, self.board[row])), end='\n')

if __name__ == "__main__":
    b = Board(15, 15, 20, None)
    b.show()

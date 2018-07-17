from constants import *
import pygame_sdl2
pygame_sdl2.import_as_pygame()


class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self._name = '–'
        self._neighbors = 0
        self._mine = False     # cell is mine      :- boolean
        self._state = False    # cell is revealed  :- boolean
        self.flagged = False  # cell is flagged
        self.xPos = PADDING + (SEPARATION + TILE_DIMENSION) * i
        self.yPos = PADDING + (SEPARATION + TILE_DIMENSION) * j
        self.rect = pygame_sdl2.Rect(self.xPos, self.yPos, TILE_DIMENSION, TILE_DIMENSION)
        self.font = pygame_sdl2.font.SysFont("Arial", 20)

    def is_mine(self):
        return self._mine

    def is_revealed(self):
        return self._state

    def get_neighbors(self):
        return self._neighbors

    def toggle_state(self):
        self._state = True

    def draw(self, surface):
        """draw cell on board"""
        if self._state:
            # revealed
            if not self.is_mine():
                # number
                number = str(self._neighbors) if self.get_neighbors() > 0 else ' '
                pygame_sdl2.draw.rect(surface, CELL_COLOR_ACTIVE, self.rect)
                surface.blit(self.font.render(number, True, TEXT_COLOR), (self.xPos + TEXT_X_OFF, self.yPos + TEXT_Y_OFF
                                                                          ))
            else:
                # game over !
                pygame_sdl2.gfxdraw.filled_circle(surface, self.xPos + MINE_OFFSET, self.yPos + MINE_OFFSET,
                                                  MINE_RADIUS, CELL_COLOR_MINE)
                pygame_sdl2.gfxdraw.aacircle(surface, self.xPos + MINE_OFFSET, self.yPos + MINE_OFFSET, MINE_RADIUS,
                                             CELL_COLOR_MINE)
        else:
            # not revealed
            if self.flagged:
                # draw flag at cell !
                pass
            pygame_sdl2.draw.rect(surface, CELL_COLOR, self.rect)

    def clicked(self, x, y) -> bool:
        """return true if cell is clicked"""
        return self.rect.collidepoint(x, y)

    def set_mine(self, value):
        self._name = '●'
        self._mine = value

    def set_neighbors(self, num):
        self._name = str(num)
        self._neighbors = num

    def get_loc(self):
        return self.i, self.j

    def __repr__(self):
        return "{:3d}".format(self._neighbors)

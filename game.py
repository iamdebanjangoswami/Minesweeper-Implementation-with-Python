from board import Board
from constants import *
import os
import pygame_sdl2
import sys
import _thread


class Game(object):
    def __init__(self):
        # Placeholder variables
        self.width = None
        self.height = None
        self.window = None
        self.board = None
        self.center = None
        self.reload_button_image = None
        self.rect = None
        self.font = None
        self.audio_mine = None
        self.audio_tile = None

        # Setup !
        self.setup()

    def setup(self):
        # Main variables
        self.width = BOARD_WIDTH * (TILE_DIMENSION + SEPARATION) + 2 * PADDING
        self.height = BOARD_HEIGHT * (TILE_DIMENSION + SEPARATION) + 2 * PADDING

        pygame_sdl2.init()
        pygame_sdl2.mixer.init()
        self.window = pygame_sdl2.display.set_mode((self.height, self.width), pygame_sdl2.WINDOW_ALLOW_HIGHDPI)
        pygame_sdl2.display.set_caption(APP_NAME)

        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT, NUMBER_OF_MINES, self.window)
        self.center = (self.width // 2, self.height // 2)

        self.reload_button_image = pygame_sdl2.transform.smoothscale(pygame_sdl2.image.load(os.path.join("assets",
                                                                                                   "reload.png")), (24,
                                                                                                                    24))
        self.rect = self.reload_button_image.get_rect().move(SEPARATION, SEPARATION)
        self.font = pygame_sdl2.font.SysFont("Arial", 40)

        self.audio_mine = pygame_sdl2.mixer.Sound(os.path.join("assets", "audio", "mine.wav"))
        self.audio_tile = pygame_sdl2.mixer.Sound(os.path.join("assets", "audio", "tile.wav"))

        self.main_func()

    def main_func(self):
        while True:
            self.window.fill(BOARD_COLOR)

            # Event Tasking
            # Add all your event tasking things here
            for event in pygame_sdl2.event.get():
                if event.type == pygame_sdl2.QUIT:
                    sys.exit(0)
                if event.type == pygame_sdl2.KEYDOWN and event.key == pygame_sdl2.K_ESCAPE:
                    sys.exit(0)
                if event.type == pygame_sdl2.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame_sdl2.mouse.get_pos()
                    # print(f"Clicked at ({mouseX},{mouseY})")
                    if self.board.update_board(mouseX, mouseY, event.button):
                        if not self.board.gameover:
                            _thread.start_new_thread(self.audio_tile.play, ())

            # Add things like player updates here
            # Also things like score updates or drawing additional items
            # Remember things on top get done first so they will update in the order yours is set at
            self.board.render_frame()

            # Remember to update your clock and display at the end
            pygame_sdl2.display.update()
            pygame_sdl2.time.Clock().tick(60)

            if self.board.gameover:
                _thread.start_new_thread(self.audio_mine.play, ())
                print("Game over !")
                self.gameover()
                break

            if self.board.check_win():
                print("Game won!")
                self.gamewon()
                break

        # If you need to reset variables here
        # This includes things like score resets
    # After your main loop throw in extra things such as a main menu or a pause menu
    # Make sure you throw them in your main loop somewhere where they can be activated by the user

    def gameover(self):
        text = "Game Over !"
        while True:
            self.window.fill(BOARD_COLOR)
            x, y = self.window.get_rect().centerx + GAMEOVER_X_OFF, self.window.get_rect().centery + GAMEOVER_Y_OFF
            self.window.blit(self.font.render(text, True, CELL_COLOR), (x, y))
            self.window.blit(self.reload_button_image, self.rect)

            # Event Tasking
            # Add all your event tasking things here
            for event in pygame_sdl2.event.get():
                if event.type == pygame_sdl2.QUIT:
                    sys.exit(0)
                if event.type == pygame_sdl2.KEYDOWN and event.key == pygame_sdl2.K_ESCAPE:
                    sys.exit(0)
                if (event.type == pygame_sdl2.MOUSEBUTTONDOWN and event.button == 1) or \
                        (event.type == pygame_sdl2.KEYDOWN and event.key == pygame_sdl2.K_r):
                    if self.rect.collidepoint(pygame_sdl2.mouse.get_pos()):
                        self.setup()
                        print("RELOAD !")

            # Remember to update your clock and display at the end
            pygame_sdl2.display.update()
            pygame_sdl2.time.Clock().tick(60)

    def gamewon(self):
        text = "You Won !"
        while True:
            self.window.fill(BOARD_COLOR)
            x, y = self.window.get_rect().centerx + GAMEWON_X_OFF, self.window.get_rect().centery + GAMEWON_Y_OFF
            self.window.blit(self.font.render(text, True, CELL_COLOR), (x, y))
            self.window.blit(self.reload_button_image, self.rect)

            # Event Tasking
            # Add all your event tasking things here
            for event in pygame_sdl2.event.get():
                if event.type == pygame_sdl2.QUIT:
                    sys.exit(0)
                if event.type == pygame_sdl2.KEYDOWN and event.key == pygame_sdl2.K_ESCAPE:
                    sys.exit(0)
                if (event.type == pygame_sdl2.MOUSEBUTTONDOWN and event.button == 1) or \
                        (event.type == pygame_sdl2.KEYDOWN and event.key == pygame_sdl2.K_r):
                    if self.rect.collidepoint(pygame_sdl2.mouse.get_pos()):
                        self.setup()
                        print("RELOAD !")

            # Remember to update your clock and display at the end
            pygame_sdl2.display.update()
            pygame_sdl2.time.Clock().tick(60)


if __name__ == "__main__":
    Game()

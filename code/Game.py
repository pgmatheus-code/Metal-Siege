import sys
import pygame

from code.Const import WINDOW_SIZE, MENU_OPTION
from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=WINDOW_SIZE)

    def run(self, ):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            # if menu_return in [MAIN_MENU_OPT[0], MAIN_MENU_OPT[1], MAIN_MENU_OPT[2]]:  # new game
            #     player_score = [0, 0]  # [player1, player2]
            #
            #     # city 1
            #     level = Level(self.window, 'city1', menu_return, player_score)
            #     level_return = level.run(player_score)
            #
            #     if level_return:  # city 2
            #         level = Level(self.window, 'city2', menu_return, player_score)
            #         level_return = level.run(player_score)
            #
            #         if level_return:  # city 3
            #             level = Level(self.window, 'city3', menu_return, player_score)
            #             level_return = level.run(player_score)
            #
            #             if level_return:  # city 4
            #                 level = Level(self.window, 'city4', menu_return, player_score)
            #                 level_return = level.run(player_score)
            #
            #                 if level_return:  # end game
            #                     scoreboard.save(menu_return, player_score)
            #
            if menu_return == MENU_OPTION[2]:  # construction
                print('construction not implemented')
            if menu_return == MENU_OPTION[3]:  # quit game
                pygame.quit()
                sys.exit()

import sys
import pygame

from code.Const import WINDOW_SIZE, MENU_OPTION
from code.Controls import Controls
from code.Stage import Stage
from code.Menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=WINDOW_SIZE)

    def run(self, ):
        while True:
            key_bindings = Controls(self.window)
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in [MENU_OPTION[0], MENU_OPTION[1]]:  # new game
                player_score = [0, 0]  # [player1, player2]

                # stage 1
                stage1 = Stage(self.window, 'stage1', menu_return, player_score)
                stage_return = stage1.run(player_score)

                if stage_return:  # stage 2
                    stage2 = Stage(self.window, 'stage2', menu_return, player_score)
                    stage_return = stage2.run(player_score)

                    if stage_return:  # stage 3
                        stage3 = Stage(self.window, 'stage3', menu_return, player_score)
                        stage_return = stage3.run(player_score)

                        if stage_return:  # stage 4
                            level4 = Stage(self.window, 'stage4', menu_return, player_score)
                            stage_return = level4.run(player_score)

                            # if stage_return:  # end game
                            #     scoreboard.save(menu_return, player_score)

            if menu_return == MENU_OPTION[2]: # controls
                key_bindings.show()

            if menu_return == MENU_OPTION[3]:  # quit game
                pygame.quit()
                sys.exit()

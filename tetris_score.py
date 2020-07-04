import pygame
import sys
import json

class Scoreboard:
    def __init__(self, file, x, y, sx, sy):

        self.file = file
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy

        with open(self.file) as sb:
            self.scoreboard = json.load(sb)

        self.names = []
        self.scores = []
        self.players = []
        self.s_players = []

    def drawScoreboard(self, screen, font, font_size):

        self.names = []
        self.scores = []
        self.players = []
        self.s_players = []

        for name, score in self.scoreboard.items():
            p = (name, score)
            self.players.append(p)

        self.s_players = sorted(self.players, key=lambda players: int(players[1]), reverse=True)

        self.font = pygame.font.SysFont(font, font_size)

        for index in range(7):
            try:
                name = self.s_players[index][0]
                score = str(self.s_players[index][1])
            except:
                name = " "
                score = " "

            score_rect = pygame.Rect(self.x, self.y + 40 * index, self.sx, self.sy)
            render_score = self.font.render(score, True, (255, 255, 255), None)
            render_score_rect = render_score.get_rect()
            render_score_rect.midright = score_rect.midright
            render_score_rect = render_score_rect.move((-5,0))

            name_rect = pygame.Rect(self.x, self.y + 40 * index, self.sx, self.sy)
            render_name = self.font.render(name, True, (255, 255, 255), None)
            render_name_rect = render_name.get_rect()
            render_name_rect.midleft = name_rect.midleft
            render_name_rect = render_name_rect.move((5, 0))

            rect_surface = pygame.Surface((self.sx, self.sy))
            rect_surface.fill((50, 50, 50))

            screen.blit(rect_surface, score_rect)
            screen.blit(render_score, render_score_rect)
            screen.blit(render_name, render_name_rect)

    def drawMarginScoreboard(self):
        pass

    def addScoreboard(self, screen, score, button_name, the_buttons, board, font, font_size):

        button_yes = the_buttons[0]
        button_no = the_buttons[1]

        stillWriting = True
        pressedEnter = False
        name = ""

        mousePressed = False
        mouseLift = False

        while stillWriting:

            screen.fill((0,0,0))
            board.draw(screen)

            if not pressedEnter:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            name = name + "Q"
                        if event.key == pygame.K_w:
                            name = name + "W"
                        if event.key == pygame.K_e:
                            name = name + "E"
                        if event.key == pygame.K_r:
                            name = name + "R"
                        if event.key == pygame.K_t:
                            name = name + "T"
                        if event.key == pygame.K_y:
                            name = name + "Y"
                        if event.key == pygame.K_u:
                            name = name + "U"
                        if event.key == pygame.K_i:
                            name = name + "I"
                        if event.key == pygame.K_o:
                            name = name + "O"
                        if event.key == pygame.K_p:
                            name = name + "P"
                        if event.key == pygame.K_a:
                            name = name + "A"
                        if event.key == pygame.K_s:
                            name = name + "S"
                        if event.key == pygame.K_d:
                            name = name + "D"
                        if event.key == pygame.K_f:
                            name = name + "F"
                        if event.key == pygame.K_g:
                            name = name + "G"
                        if event.key == pygame.K_h:
                            name = name + "H"
                        if event.key == pygame.K_j:
                            name = name + "J"
                        if event.key == pygame.K_k:
                            name = name + "K"
                        if event.key == pygame.K_l:
                            name = name + "L"
                        if event.key == pygame.K_z:
                            name = name + "Z"
                        if event.key == pygame.K_x:
                            name = name + "X"
                        if event.key == pygame.K_c:
                            name = name + "C"
                        if event.key == pygame.K_v:
                            name = name + "V"
                        if event.key == pygame.K_b:
                            name = name + "B"
                        if event.key == pygame.K_n:
                            name = name + "N"
                        if event.key == pygame.K_m:
                            name = name + "M"
                        if event.key == pygame.K_SPACE:
                            name = name + "_"

                        if event.key == pygame.K_BACKSPACE and len(name) >= 1:
                            name = name[:-1]
                        if event.key == pygame.K_RETURN:
                            pressedEnter = True
                button_name.draw(screen, name, " ", (0, 0, 0), (255, 255, 255), font, font_size)
                button_name.drawText(screen, 200, 90, "GIVE ME YOUR NAME:", (255, 255, 255), font, font_size)

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            stillWriting = False
                        elif event.key == pygame.K_BACKSPACE:
                            pressedEnter = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mousePressed = True

                    elif event.type == pygame.MOUSEBUTTONUP:
                        mousePressed = False
                        mouseLift = True

                button_name.draw(screen, name," ", (0, 0, 0), (255, 255, 255), font, font_size)
                button_name.drawText(screen, 200, 90, "YOU'RE", (255, 255, 255), font, font_size)
                button_name.drawText(screen, 200, 130, "THEN?", (255, 255, 255), font, font_size)

                if mousePressed or mouseLift:
                    if button_no.mousePress(pygame.mouse.get_pos(), mouseLift):
                        pressedEnter = False
                    if button_yes.mousePress(pygame.mouse.get_pos(), mouseLift):
                        stillWriting = False
                    mouseLift = False

                button_no.draw(screen, "NO", "MY BAD", (50, 50, 50), (255, 255, 255), font, font_size)
                button_yes.draw(screen, "SI", "PLZ", (50, 50, 50), (255, 255, 255), font, font_size)

            pygame.display.flip()

        check = self.scoreboard.get(name)

        if check is not None:
            previous_score = self.scoreboard[name]
            if previous_score >= score:
                print("YOU'VE DONE BETTER")
            else:
                print("YOU OUTDID YOURSELF BY " + str(score - previous_score))
                self.scoreboard.update({name: score})
                with open(self.file, "w") as sb:
                    json.dump(self.scoreboard, sb)
        else:
            self.scoreboard.update({name : score})
            with open(self.file, "w") as sb:
                json.dump(self.scoreboard, sb)




    def writeDummy(self):

        pass

        new_scoreboard = {" ": 0}

        with open(self.file, "w") as sb:
            json.dump(new_scoreboard, sb)

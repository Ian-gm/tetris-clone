import pygame
import sys
import random
import json

from tetris_player import Player
from tetris_board import Board
from tetris_button import Button
from tetris_score import Scoreboard

x = 0

# Necesito el init para abrir las fonts
pygame.init()

# Todas las combinaciones de tetraminos
TETRAMINOS = [

    # cada número representa un bloque en una grilla de 2x4
    #
    #                   0 - 1
    #                   2 - 3
    #                   4 - 5
    #                   6 - 7

                (0, 2, 1, 4),  # L
                (0, 1, 3, 5),  # J
                (0, 2, 4, 6),  # I
                (1, 3, 2, 4),  # S
                (0, 2, 3, 5),  # Z
                (0, 2, 3, 4),  # T
                (0, 1, 2, 3),  # O
]

# Lista de colores de cada tetramino
COLORS = [
    (255, 50,  50),
    (150, 0,   50),
    (150, 150, 255),
    (50,  0,   150),
    (50,  50,  255),
    (0,   255, 255),
    (0,   100, 100),
    (255, 255, 255)
]

# Valores globales
block_size = 20
board_x = 12
board_y = 24
board_offset = 4
size = width, height = (board_x + (board_offset*2)) * block_size, 24 * block_size

# Elementos de pygame
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Menu
all_the_fonts = pygame.font.get_fonts()
font = all_the_fonts[297]
font_size = 10

# Buttons
button_size_x = 200
button_size_y = 20
button_x = 100
button_y = 80
button_gameOn = Button(button_x, button_y + block_size*1, button_size_x, button_size_y)
button_scoreOn = Button(button_x, button_y + block_size*3, button_size_x, button_size_y)
button_backtoMenu = Button(button_x+241, button_y+1 + block_size*18, block_size*2-1, button_size_y-1)
button_resetGame = Button(block_size+1, button_y+1 + block_size*18, block_size*2-1, button_size_y-1)

button_yes = Button(button_x, button_y + block_size*3, button_size_x/2 - block_size, button_size_y)
button_no = Button(button_x + block_size*6, button_y + block_size*3, button_size_x/2 - block_size, button_size_y)
button_check = Button(button_x + block_size + 1, button_y+1 + block_size*1, button_size_x - block_size*2 - 1, button_size_y-1)

the_buttons = [button_yes, button_no, button_check]

button_name = Button(button_x, button_y + block_size*1, button_size_x, button_size_y)

# Un delay hard-coded para definir el ritmo con el que se mueve a la siguiente fila el bloque en juego
hard_tick = 0
hard_tick_max = 10

# El objeto Board evalúa las coliciones de la pieza en juego, guarda las piezas que terminaron de caer y el puntaje
board = Board(board_x, board_y, block_size, COLORS, font, font_size, board_offset)
board.resetBoard()

# El objeto Scoreboard internaliza el .json para mostrarlo y editarlo
scoreboard = Scoreboard("tetris_scoreboard.json", 100, 100, 200, 20)

# Todas las flags que voy a necesitar
rotate = False
move_value = 0
valid_move = True
dx_left = 0
dx_right = 0
dy = 0
new_block = True
release = False
#WINDOWS
scoreOn = False
newScore = False
gameOn = False
#FLAG
playingOn = True
checkReset = False
checkMenu = False
#MOUSE FLAGS
mousePressed = False
mouseLift = False

# La primer pieza
p_indices = list(range(len(TETRAMINOS)))
piece = random.choice(p_indices)

def drawBackground(board):

    colour = (20, 20, 20)
    # for x in range(13):
    #     pygame.draw.line(screen, colour, (board.left_border + (x * board.block_size), 0),
    #                      (board.left_border + (x * board.block_size), board.block_size * board.board_y), 1)
    # for y in range(25):
    #     pygame.draw.line(screen, colour, (board.left_border, block_size * y),
    #                      (board.right_border, block_size * y), 1)
    for x in range(20):
        pygame.draw.line(screen, colour, (x * board.block_size, 0),
                         (x * board.block_size, board.block_size * board.board_y), 1)
    for y in range(25):
        pygame.draw.line(screen, colour, (0, block_size * y),
                         (24 * block_size, block_size * y), 1)

def resetGame(board):
    board.resetBoard()
    #Va a subir la flag "new_block" para resetear la pieza
    return True

# GAME LOOP
while True:

    # Los fps
    clock.tick(30)
    screen.fill((0, 0, 0))

# EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if gameOn:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotate = True
                elif event.key == pygame.K_RIGHT:
                    dx_right = block_size
                    move = True
                elif event.key == pygame.K_LEFT:
                    dx_left = -block_size
                    move = True
                elif event.key == pygame.K_DOWN:
                    dy = block_size
                elif event.key == pygame.K_SPACE:
                    release = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    rotate = False
                elif event.key == pygame.K_RIGHT:
                    dx_right = 0
                elif event.key == pygame.K_LEFT:
                    dx_left = 0
                elif event.key == pygame.K_DOWN:
                    dy = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            mousePressed = False
            mouseLift = True


    if gameOn:
        drawBackground(board)

        if playingOn:
            if mousePressed or mouseLift:
                if button_backtoMenu.mousePress(pygame.mouse.get_pos(), mouseLift):
                    checkMenu = True
                    playingOn = False
                elif button_resetGame.mousePress(pygame.mouse.get_pos(), mouseLift):
                    checkReset = True
                    playingOn = False
                mouseLift = False

            # El valor máximo de los hard_ticks aumenta en función del puntaje
            hard_tick_max = max(10 - round(board.points / 2000), 1)

            # Hago correr los hard_ticks que mueven el bloque en juego a la siguiente fila
            if hard_tick > hard_tick_max:
                hard_tick = 0
            else:
                hard_tick += 1

        # PLAYER
            # Una flag para saber si hace falta construir un bloque
            if new_block:
                # Se elige el valor del siguiente bloque
                pieces_index = p_indices.copy()
                pieces_index.pop(piece)
                next_piece = random.choice(pieces_index)
                # Se construye el bloque con el valor que estaba guardado de la ultima vez y el que acabamos de hacer
                player = Player(piece, COLORS[piece], next_piece, COLORS[next_piece])
                # Se construyen las listas de rects correspondientes
                player.createBlocks(TETRAMINOS, block_size, board)
                # Se baja la bandera
                new_block = False
                # Se guarda el valor del siguiente bloque
                piece = next_piece

            if rotate:
                player.rotate(board)
                rotate = False

            if move_value == 1:
                player.move(dx_left + dx_right, 0, block_size, board_x, board)

            # El delay del movimiento de la pieza (sutil pero clave)
            if move_value >= 1:
                move_value = 0
            else:
                move_value += 1

            # El movimiento hacia abajo se hace a parte (no tiene delay)
            player.move(0, dy, block_size, board_x, board)

            # La caida del bloque no solo lo desplaza, sino que devuelve un boolean para decidir si hacer un bloque nuevo o no
            if hard_tick == hard_tick_max:
                new_block = player.movedown(block_size, board)

            # Si apretaron la barra espaciadora la pieza se reemplaza por la shadow_piece y la hago colicionar con el movedown
            if release:
                player.releaseBlock()
                new_block = player.movedown(block_size, board)
                release = False

        # BOARD
            # Se evalúa si alguna fila está completa
            board.clearRow(board_x, board_y, block_size, clock)
            if not board.keep_playing:
                scoreboard.addScoreboard(screen, board.points, button_name, the_buttons, board, font, font_size)
                gameOn = False
                scoreOn = True

    # DRAW

        player.draw(screen)
        board.draw(screen)
        button_backtoMenu.draw(screen, "BACK", "MENU", (0, 0, 0), (55, 55, 55), font, font_size)
        button_resetGame.draw(screen, "RESET", "GAME", (0, 0, 0), (55, 55, 55), font, font_size)

        if not playingOn:
            if mousePressed or mouseLift:
                if button_no.mousePress(pygame.mouse.get_pos(), mouseLift):
                    playingOn = True
                    checkReset = False
                    checkMenu = False
                if button_yes.mousePress(pygame.mouse.get_pos(), mouseLift):
                    if checkReset:
                        new_block = resetGame(board)
                        checkReset = False
                        playingOn = True
                    elif checkMenu:
                        new_block = resetGame(board)
                        checkMenu = False
                        playingOn = True
                        gameOn = False
                mouseLift = False
            if checkReset:
                button_check.draw(screen, "WANT TO START OVER?", " ", (0,0,0), (255,255,255), font, font_size)
            elif checkMenu:
                button_check.draw(screen, "BACK TO MENU?", " ", (0,0,0), (255,255,255), font, font_size)
            button_no.draw(screen, "NO", "MY BAD", (50, 50, 50), (255, 255, 255), font, font_size)
            button_yes.draw(screen, "SI", "PLZ", (50, 50, 50), (255, 255, 255), font, font_size)

#SCOREBOARD WINDOW
    elif scoreOn:
        drawBackground(board)
        if mousePressed or mouseLift:
            scoreOn = not button_backtoMenu.mousePress(pygame.mouse.get_pos(), mouseLift)
            mouseLift = False

        scoreboard.drawScoreboard(screen, font, font_size)

        button_backtoMenu.draw(screen, "BACK", "MENU", (50, 50, 50), (255, 255, 255), font, font_size)

#MENU WINDOW
    else:
        new_block = resetGame(board)
        if mousePressed or mouseLift:
            gameOn = button_gameOn.mousePress(pygame.mouse.get_pos(), mouseLift)
            scoreOn = button_scoreOn.mousePress(pygame.mouse.get_pos(), mouseLift)
            mouseLift = False

        drawBackground(board)

        button_gameOn.draw(screen, "START", "LET'S GO", (50, 50, 50), (255, 255, 255), font, font_size)
        button_scoreOn.draw(screen, "SCOREBOARD", "WHO DID BEST?", (50, 50, 50), (255, 255, 255), font, font_size)


    pygame.display.flip()

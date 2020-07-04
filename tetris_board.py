import pygame

class Board:
    def __init__(self, board_x, board_y, block_size, colors, font, font_size, board_offset):
        self.board_x = board_x
        self.board_y = board_y
        self.block_size = block_size

        self.right_border = (self.board_x + 4) * self.block_size
        self.left_border =  board_offset * self.block_size
        self.board_offset = board_offset

        self.board_blocks = []
        self.board_colors = []
        self.color_blocks = []

        self.colors = colors
        self.keep_playing = True
        self.points = 0

        # Y los textos
        # print(pygame.font.get_fonts())
        self.font = pygame.font.SysFont(font, font_size)

        self.animate = 10
        self.animation = self.animate

    def resetBoard(self):

        self.board_blocks = []
        self.board_colors = []
        self.color_blocks = []

        # Se construye el array de dos dimensiones, con un "None" en cada posicion"
        for i in range(self.board_y+1):
            if i < self.board_y:
                self.board_blocks.append([None] * self.board_x)
                self.board_colors.append([None] * self.board_x)
            # PERO el ultimo array (de alli el +1) es una lista de rectangulos, y nunca se van a reemplazar
            else:
                for x in range(self.board_x):
                    rect = pygame.Rect((x + 4) * self.block_size, self.board_y * self.block_size,
                                       self.block_size, self.block_size)
                    self.board_blocks.append([rect] * self.board_x)
                    self.board_colors.append([0] * self.board_x)

        # Y se hace un array de todas las srf necesarias para dibujar los 7 colores
        for i in range(len(self.colors)):
            sprite = pygame.Surface((self.block_size, self.block_size))
            sprite.fill(self.colors[i], pygame.Rect(0, 0, self.block_size, self.block_size))
            self.color_blocks.append(sprite)

        # Se crean las flags necesarias
        self.keep_playing = True
        self.points = 0



    # TEXT
        #Next piece
        self.next_piece = self.font.render('NEXT PIECE', True, (255, 255, 255), None)
        self.next_piece_r = self.next_piece.get_rect()
        self.next_piece_r.center = (360, 20)

        #Point
        self.points_text = self.font.render('POINTS', True, (255, 255, 255), None)
        self.points_text_r = self.points_text.get_rect()
        self.points_text_r.center = (360, 160)

        self.board_history = []
        self.board_history_color = []

    def insertBlock(self, blocks, color):
        for i in range(4):
            rect = blocks[i]

            # Las coordenadas se convierten en los indices del array bidimensional
            x = int(rect.x/self.block_size) - 4
            y = int(rect.y/self.block_size)

            self.board_blocks[y][x] = rect
            self.board_colors[y][x] = color

            # Si alguno de esos bloques esta por arriba del 0 se baja la bandera
            if rect.y < 0:
                self.keep_playing = False

        self.board_history.append(self.board_blocks)
        self.board_history_color.append(self.board_colors)

# Para checkear la lista de bloques en vivo
        # an_array = []
        # for i in range(self.board_y):
        #     an_array = []
        #     for rect in self.board_blocks[i]:
        #         if rect is not None:
        #             an_array.append("X")
        #         else:
        #             an_array.append(" ")
        #     print(str(an_array))
        # print(" ")

    def clearRow(self, board_x, board_y, block_size, clock):
        # Construyo un array para cada fila
        clear_row = [True] * board_y
        clear_amount = 0
        last_row = None
        for index, row in enumerate(self.board_blocks):
            for rect in row:
                if rect is None:
                    # Si alguno de los bloques en esta fila no es un rectangulo, bajo la bandera
                    clear_row[index] = False

        # Cuento al cantidad total de filas que hay que borrar
        for i in range(board_y):
            if clear_row[i]:
                clear_amount += 1
                last_row = i

        # Si hay que borrar filas
        if clear_amount > 0:
            # Hago un array de "abajo hacia arriba"

            while self.animation > 0:
                clock.tick(30)
                self.animation -= 1
                print("animating")

            self.animation = self.animate

            for count in range(last_row - clear_amount + 1):
                # Esta es la fila que hay que borrar
                empty_row = last_row - count
                # Esta es la fila que va a reemplazarla
                replacting_row = empty_row-clear_amount
                # Desplazo todos los cuadrados de la fila que tiene que bajar
                for j in range(board_x):
                    rect = self.board_blocks[replacting_row][j]
                    if rect is not None:
                        self.board_blocks[replacting_row][j] = self.board_blocks[replacting_row][j].move((0, block_size*clear_amount))
                # Hago el reemplazo
                self.board_blocks[empty_row] = self.board_blocks[replacting_row].copy()
                # Y la fila que desplace la vacio
                self.board_blocks[replacting_row] = [None] * board_x

                # Mismo con los colores
                self.board_colors[empty_row] = self.board_colors[replacting_row]
                self.board_colors[replacting_row] = [None] * board_x

        # Cuento la cantidad de puntos
        factor = 0
        for i in range(clear_amount):
            factor += i+1
        self.points += factor * 100

    def draw(self, screen):
        for i in range(len(self.board_blocks)):
            for j in range(len(self.board_blocks[i])):
                rect = self.board_blocks[i][j]
                if rect is not None:
                    n = self.board_colors[i][j]
                    screen.blit(self.color_blocks[n], rect)

        pygame.draw.line(screen, (255, 255, 255), (self.right_border, 0),
                         (self.right_border, self.block_size * self.board_y), 1)
        pygame.draw.line(screen, (255, 255, 255), (self.left_border, 0),
                         (self.left_border, self.block_size * self.board_y), 1)
        # Text
        screen.blit(self.next_piece, self.next_piece_r)
        screen.blit(self.points_text, self.points_text_r)

        points_num = self.font.render(str(self.points), True, (255, 255, 255), (0, 0, 0))
        points_num_r = points_num.get_rect()
        points_num_r.center = (360, 180)
        screen.blit(points_num, points_num_r)

# Para checkear la gama de colores
        # for index, sprite in enumerate(self.color_blocks):
        #     rect = pygame.Rect(270, index*20 + 240, 20, 20)
        #     screen.blit(sprite, rect)
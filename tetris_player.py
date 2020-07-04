import pygame

class Player:
    def __init__(self, piece, colour, next_piece, next_colour):
        # Se guardan los indices de las piezas
        self.piece = piece
        self.next_piece = next_piece
        # Los colores de las piezas
        self.colour = colour
        self.next_colour = next_colour
        # Se construyen los arrays vacios que van a contener los rects
        self.blocks = []
        self.block_sprite = 0
        self.next_blocks = []
        self.next_block_sprite = 0
        # Esta es la lista de rectangulos para la pieza que representan la posicion final
        self.shadow_blocks = []

        # Y defino las flags necesarias
        self.valid_move = True
        self.valid_rotation = True


    def createBlocks(self, TETRAMINOS, block_size, board):
        a = TETRAMINOS[self.piece]

        # Los bloques se hacen en funcion a si el numero de la grilla de 2x4 que contenga el tuple
        for i in range(4):
            n = a[i]
            # ...es par o impar (para el eje X)
            x = (n % 2) * block_size
            # Centrado
            x += round(board.board_x/2) * block_size + (block_size*2)
            # ...y que multiplo de 2 es (para el eje Y)
            if n%2 == 1:
                y = ((n / 2) - 0.5) * block_size
            else:
                y = (n / 2) * block_size
            # Afuera de la pantalla
            y -= block_size*4
            block = pygame.Rect(x, y, block_size, block_size)
            self.blocks.append(block)

        # Lo mismo para la next_piece
        a = TETRAMINOS[self.next_piece]
        for i in range(4):
            n = a[i]
            x = (n % 2) * block_size
            if n % 2 == 1:
                y = ((n / 2) - 0.5) * block_size
            else:
                y = (n / 2) * block_size
            if self.next_piece == 2:
                #block = pygame.Rect(x + 340 + block_size/2, y + 40, block_size, block_size)
                block = pygame.Rect(x + 340, y + 40, block_size, block_size)
            else:
                block = pygame.Rect(x + 340, y + 40, block_size, block_size)
            self.next_blocks.append(block)

        self.block_sprite = pygame.Surface((block_size, block_size))
        self.block_sprite.fill(self.colour, pygame.Rect(0, 0, block_size, block_size))

        self.next_block_sprite = pygame.Surface((block_size, block_size))
        self.next_block_sprite.fill(self.next_colour, pygame.Rect(0, 0, block_size, block_size))

        self.shadow_sprite_outer = pygame.Surface((block_size, block_size))
        self.shadow_sprite_outer.fill((255, 255, 255), pygame.Rect(0, 0, block_size, block_size))

        self.shadow_sprite_inner = pygame.Surface((block_size-2, block_size-2))
        self.shadow_sprite_inner.fill((0, 0, 0), pygame.Rect(0, 0, block_size, block_size))

        self.shadowPiece(board)

    def rotate(self, board):
        # Se levanta la flag
        self.valid_rotation = True

        # Solo se permite rotar si la pieza en juego no es un cuadrado
        if self.piece != 6:
            # Se hace una copia de la pieza
            move_blocks = []
            for i in range(4):
                move_blocks.append(self.blocks[i].copy())

            # Este procedimiento lo robe de internet, es impecable
            for i in range(4):
                # Se van a medir coordenadas a partir de 1 de los 4 bloques, el "r"
                r = move_blocks[1]
                block = move_blocks[i]
                # Se traza el vector, y se lo "cruza" (intercambiando las coordenadas)
                x = block.y - r.y
                y = block.x - r.x
                # Y una de la dos coordenas se restan (eso determina la direccion de la rotacion)
                move_blocks[i].x = r.x - x
                move_blocks[i].y = r.y + y

                # Aca se evalua si la copia no esta chocando contra los extremos o contra los bloques del board
                for y in range(len(board.board_blocks)):
                    for x in range(len(board.board_blocks[y])):
                        rect = board.board_blocks[y][x]
                        if rect is not None:
                            if move_blocks[i].colliderect(board.board_blocks[y][x]):
                                self.valid_rotation = False
                        elif move_blocks[i].x < board.block_size*4 or move_blocks[i].x > ((board.board_x+3) * board.block_size):
                                self.valid_rotation = False

            # Si la flag no se bajo, la lista original se reemplaza por la copia rotada y se construye la shadow_piece
            if self.valid_rotation:
                self.blocks = move_blocks

                self.shadowPiece(board)


    def move(self, dx, dy, block_size, board_x, board):
        # Se levanta la flag
        self.valid_move = True

        # Se hace una copia de la pieza en juego
        move_blocks = []
        for i in range(4):
            move_blocks.append(self.blocks[i].copy())

        # Se desplazan los rectangulos y se evalua si la copia esta chocando con los extremos o con las piezas del board
        for i in range(4):
            move_blocks[i].x += dx
            move_blocks[i].y += dy
            if move_blocks[i].x < block_size*4 or move_blocks[i].x > (board_x-1) * block_size + block_size*4:
                self.valid_move = False
            for y in range(len(board.board_blocks)):
                for rect in board.board_blocks[y]:
                    if rect is not None:
                        if move_blocks[i].colliderect(rect):
                            self.valid_move = False

        # Si no se bajo la flag la lista original se reemplaza por la copia desplazada
        if self.valid_move:
            self.blocks = move_blocks

            self.shadowPiece(board)

    def movedown(self, block_size, board):
        # Se hace una copia de la pieza en juego
        move_blocks = []
        for i in range(4):
            move_blocks.append(self.blocks[i].copy())

        # Se mueve a la siguiente fila
        for i in range(4):
            move_blocks[i].y += block_size
            for y in range(len(board.board_blocks)):
                for rect in board.board_blocks[y]:
                    if rect is not None:
                        # Si esta copia colisiona con el board se inserta la pieza original al board
                        if move_blocks[i].colliderect(rect):
                            board.insertBlock(self.blocks, self.piece)
                            # Aca se "avisa" que hay que hacer un bloque nuevo
                            return True
        # Si no hubo colision el bloque original es reemplazado por la copia desplazada
        self.blocks = move_blocks
        # Aca se "avisa" que hay que este bloque sigue en juego
        return False

    def shadowPiece(self, board):
        # La shadow piece primero es identica a la pieza
        self.shadow_blocks = self.blocks.copy()
        # Se hace una copia de la shadow piece
        move_blocks = self.shadow_blocks.copy()
        # Y se crea la flag que interrumpe el loop
        break_flag = False
        # Se empieza un loop tan largo como la cantidad total de filas (considerando las que estan fuera de la pantalla)
        for y in range(board.board_y + 4):
            # La shadow piece es identica a la ultima posicion de la copia desplazada
            self.shadow_blocks = move_blocks.copy()
            for i in range(4):
                # Se desplazan los rectangulos de la copia
                move_blocks[i] = move_blocks[i].move(0, board.block_size)
                for index, row in enumerate(board.board_blocks):
                    for rect in row:
                        if rect is not None:
                            # Si al copia colisiona se levanta la flag
                            if move_blocks[i].colliderect(rect):
                                break_flag = True
            # La flag detiene el loop principal
            if break_flag:
                break

    def releaseBlock(self):
        self.blocks = self.shadow_blocks.copy()

    def draw(self, screen):
        for i in range(4):
            screen.blit(self.shadow_sprite_outer, self.shadow_blocks[i])
            screen.blit(self.shadow_sprite_inner, self.shadow_blocks[i].move(1, 1))
            screen.blit(self.block_sprite, self.blocks[i])
            screen.blit(self.next_block_sprite, self.next_blocks[i])
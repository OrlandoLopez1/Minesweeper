import pygame
import random


class Board:

    def __init__(self, window, rows, cols, difficulty):
        self.window = window
        self.rows = rows
        self.cols = cols
        self.board = [[Tile() for j in range(cols)] for i in range(rows)]
        self.num_mines = 0
        self.remaining_tiles = rows * cols
        self.counter = 0
        self.difficulty = difficulty
        self.easy = pygame.image.load("Assets/Easy.png")
        self.medium = pygame.image.load("Assets/Medium.png")
        self.hard = pygame.image.load("Assets/Hard.png")
        self.face = pygame.image.load("Assets/face_happy.png")

        bottom = (self.rows * 32)
        right = (self.cols * 32) - 64
        self.easy_rect = self.easy.get_rect(topleft=(right, bottom))
        self.medium_rect = self.medium.get_rect(topleft=(right, bottom + 32))
        self.hard_rect = self.hard.get_rect(topleft=(right, bottom + 64))
        middle = (self.cols * 32) // 2 - 32
        bottom = (self.rows * 32)
        self.face_rect = self.face.get_rect(topleft=(middle, bottom))
        self.can_click_board = True

    def load_all_board_info(self):
        self.initialize_board()
        self.load_mines()
        self.draw_board()
        self.draw_stuff_under_board()
        self.draw_current_difficulty()
        self.update_counter()
        pygame.display.flip()

    def reset_board(self, rows, cols, difficulty):
        pygame.display.quit()
        self.rows = rows
        self.cols = cols
        self.window = pygame.display.set_mode((cols * 32, (rows * 32) + 96))
        self.board = [[Tile() for j in range(cols)] for i in range(rows)]
        self.num_mines = 0
        self.remaining_tiles = rows * cols
        self.counter = 0
        self.difficulty = difficulty
        self.face = pygame.image.load("Assets/face_happy.png")
        bottom = (self.rows * 32)
        right = (self.cols * 32) - 64
        self.easy_rect = self.easy.get_rect(topleft=(right, bottom))
        self.medium_rect = self.medium.get_rect(topleft=(right, bottom + 32))
        self.hard_rect = self.hard.get_rect(topleft=(right, bottom + 64))
        middle = (self.cols * 32) // 2 - 32
        bottom = (self.rows * 32)
        self.face_rect = self.face.get_rect(topleft=(middle, bottom))
        self.can_click_board = True

    def initialize_board(self):
        # code reused from Path Finding Visualizer Project todo add github link

        # board[row][col]
        # TL corner
        self.board[0][0].right = self.board[0][1]
        self.board[0][0].down = self.board[1][0]
        self.board[0][0].left = None
        self.board[0][0].up = None
        # TR corner
        self.board[0][self.cols - 1].left = self.board[0][self.cols - 2]
        self.board[0][self.cols - 1].down = self.board[1][self.cols - 1]
        self.board[0][self.cols - 1].right = None
        self.board[0][self.cols - 1].up = None
        # BL corner
        self.board[self.rows - 1][0].right = self.board[self.rows - 1][1]
        self.board[self.rows - 1][0].up = self.board[self.rows - 2][0]
        self.board[self.rows - 1][0].left = None
        self.board[self.rows - 1][0].down = None
        # BR corner
        self.board[self.rows - 1][self.cols - 1].left = self.board[self.rows - 1][self.cols - 2]
        self.board[self.rows - 1][self.cols - 1].up = self.board[self.rows - 2][self.cols - 1]
        self.board[self.rows - 1][self.cols - 1].right = None
        self.board[self.rows - 1][self.cols - 1].down = None
        # LEFT side
        for i in range(1, self.rows - 1):
            self.board[i][0].right = self.board[i][1]
            self.board[i][0].up = self.board[i - 1][0]
            self.board[i][0].down = self.board[i + 1][0]
            self.board[i][0].left = None
        # RIGHT side
        for i in range(1, self.rows - 1):
            self.board[i][self.cols - 1].left = self.board[i][self.cols - 2]  # changed from right to left
            self.board[i][self.cols - 1].up = self.board[i - 1][self.cols - 1]
            self.board[i][self.cols - 1].down = self.board[i + 1][self.cols - 1]
            self.board[i][self.cols - 1].right = None
        # TOP side
        for i in range(1, self.cols - 1):
            self.board[0][i].left = self.board[0][i - 1]
            self.board[0][i].right = self.board[0][i + 1]
            self.board[0][i].down = self.board[1][i]
            self.board[0][i].up = None

        # BOTTOM side
        for i in range(1, self.cols - 1):
            self.board[self.rows - 1][i].left = self.board[self.rows - 1][i - 1]
            self.board[self.rows - 1][i].right = self.board[self.rows - 1][i + 1]
            self.board[self.rows - 1][i].up = self.board[self.rows - 2][i]
            self.board[self.rows - 1][i].down = None

        # MIDDLE
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                self.board[i][j].left = self.board[i][j - 1]
                self.board[i][j].right = self.board[i][j + 1]
                self.board[i][j].up = self.board[i - 1][j]
                self.board[i][j].down = self.board[i + 1][j]

        # TL corner
        self.board[0][0].down_right = self.board[0][0].down.right
        # TR corner
        self.board[0][self.cols - 1].down_left = self.board[0][self.cols - 1].down.left
        # BL corner
        self.board[self.rows - 1][0].up_right = self.board[self.rows - 1][0].up.right
        # BR corner
        self.board[self.rows - 1][self.cols - 1].up_left = self.board[self.rows - 1][self.cols - 1].up.left
        # LEFT side
        for i in range(1, self.rows - 1):
            self.board[i][0].up_right = self.board[i][0].up.right
            self.board[i][0].down.right = self.board[i][0].down.right
        # RIGHT side
        for i in range(1, self.rows - 1):
            self.board[i][self.cols - 1].up_left = self.board[i][self.cols - 1].up.left
            self.board[i][self.cols - 1].down_left = self.board[i][self.cols - 1].down.left
        # TOP side
        for i in range(1, self.cols - 1):
            self.board[0][i].down_left = self.board[0][i].down.left
            self.board[0][i].down_right = self.board[0][i].down.right
        # BOTTOM side
        for i in range(1, self.cols - 1):
            self.board[self.rows - 1][i].up_left = self.board[self.rows - 1][i].up.left
            self.board[self.rows - 1][i].up_right = self.board[self.rows - 1][i].up.right
        # MIDDLE
        for i in range(1, self.rows - 1):
            for j in range(1, self.cols - 1):
                self.board[i][j].up_left = self.board[i][j].up.left
                self.board[i][j].up_right = self.board[i][j].up.right
                self.board[i][j].down_left = self.board[i][j].down.left
                self.board[i][j].down_right = self.board[i][j].down.right

        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].image_rect = self.board[i][j].image.get_rect(topleft=(j * 32, i * 32))

    def load_mines(self):
        if self.difficulty == 1:
            self.num_mines = 10
            self.counter = 10
        elif self.difficulty == 2:
            self.num_mines = 40
            self.counter = 40
        elif self.difficulty == 3:
            self.num_mines = 99
            self.counter = 99
        else:
            self.num_mines = -1
            self.counter = -1

        mine_locations = set()
        count = 0
        max = self.rows * self.cols
        while len(mine_locations) < self.num_mines:
            mine_locations.add(random.randrange(0, max))
            count += 1
            print(count)

        for mine in mine_locations:
            self.board[mine // self.cols][mine % self.cols].has_mine = True
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j].count_adj_mines()

        # // cols = row
        # % cols = col

    def draw_board(self):

        for i in range(self.rows):
            for j in range(self.cols):
                self.window.blit(self.board[i][j].image, self.board[i][j].image_rect)

    def draw_stuff_under_board(self):
        self.window.blit(self.face, self.face_rect)
        self.window.blit(self.easy, self.easy_rect)
        self.window.blit(self.medium, self.medium_rect)
        self.window.blit(self.hard, self.hard_rect)
        pygame.display.flip()

    def draw_current_difficulty(self):
        bottom = (self.rows * 32) + 64
        if self.difficulty == 1:
            self.window.blit(self.easy, (0, bottom))
        elif self.difficulty == 2:
            self.window.blit(self.medium, (0, bottom))
        elif self.difficulty == 3:
            self.window.blit(self.hard, (0, bottom))
        else:
            print("Wtf happened")

        pygame.display.update()

    # todo timer
    def update_tile(self, tile):
        if not tile.revealed:
            tile.image = pygame.image.load("Assets/tile_revealed.png")
            tile.revealed = True
            self.remaining_tiles -= 1
            self.window.blit(tile.image, tile.image_rect)
            if tile.adjacent_mines != 0:
                adj_mines_num = pygame.image.load("Assets/number_" + str(tile.adjacent_mines) + ".png")
                self.window.blit(adj_mines_num, tile.image_rect)

            pygame.display.flip()

    def update_board_state(self, mouse_pos):
        if self.can_click_board:
            for i in range(self.rows):
                for j in range(self.cols):
                    clicked = self.board[i][j].image_rect.collidepoint(mouse_pos)
                    if clicked:
                        if self.board[i][j].flagged:
                            pass
                        elif self.board[i][j].has_mine:
                            mine_img = pygame.image.load("Assets/mine.png")
                            self.window.blit(mine_img, self.board[i][j].image_rect)
                            self.defeat()
                        else:
                            if not self.board[i][j].revealed:
                                self.remaining_tiles -= 1
                                if self.remaining_tiles == self.num_mines:
                                    self.victory()
                                self.board[i][j].image = pygame.image.load("Assets/tile_revealed.png")
                                self.board[i][j].revealed = True
                                self.window.blit(self.board[i][j].image, self.board[i][j].image_rect)
                                if self.board[i][j].adjacent_mines == 0:
                                    self.floodfill(self.board[i][j])
                                    self.update_counter()
                                else:
                                    adj_mines_num = pygame.image.load(
                                        "Assets/number_" + str(self.board[i][j].adjacent_mines) + ".png")
                                    self.window.blit(adj_mines_num, self.board[i][j].image_rect)

                                pygame.display.flip()
        # changes window and boardstate when different difficulty is pressed
        if self.easy_rect.collidepoint(mouse_pos) and self.difficulty != 1:
            self.reset_board(9, 9, 1)
            h = (self.rows * 32) + 96
            w = self.cols * 32
            self.window = pygame.display.set_mode((w, h))
            self.window.fill((255, 255, 255))
            self.load_all_board_info()
        elif self.medium_rect.collidepoint(mouse_pos):
            self.reset_board(16, 16, 2)
            h = (self.rows * 32) + 96
            w = self.cols * 32
            self.window = pygame.display.set_mode((w, h))
            self.window.fill((255, 255, 255))
            self.load_all_board_info()
        elif self.hard_rect.collidepoint(mouse_pos):
            self.reset_board(16, 30, 3)
            h = (self.rows * 32) + 96
            w = self.cols * 32
            self.window = pygame.display.set_mode((w, h))
            self.window.fill((255, 255, 255))
            self.load_all_board_info()

        elif self.face_rect.collidepoint(mouse_pos):
            self.reset_board(self.rows, self.cols, self.difficulty)
            self.window.fill((255, 255, 255))
            self.load_all_board_info()

    def place_flag(self, mouse_pos):
        if self.can_click_board:
            for i in range(self.rows):
                for j in range(self.cols):
                    clicked = self.board[i][j].image_rect.collidepoint(mouse_pos)
                    if clicked:
                        if not self.board[i][j].revealed:
                            if not self.board[i][j].flagged:
                                self.board[i][j].flagged = True
                                flag = pygame.image.load("Assets/flag.png")
                                self.counter -= 1
                                self.window.blit(flag, self.board[i][j].image_rect)
                                pygame.display.flip()
                                self.update_counter()
                            else:
                                self.board[i][j].flagged = False
                                self.counter += 1
                                self.window.blit(self.board[i][j].image, self.board[i][j].image_rect)
                                pygame.display.flip()
                                self.update_counter()

    def defeat(self):
        self.face = pygame.image.load("Assets/face_lose.png")
        self.can_click_board = False
        self.window.blit(self.face, self.face_rect)
        pygame.display.flip()

    def victory(self):
        self.face = pygame.image.load("Assets/face_win.png")
        self.window.blit(self.face, self.face_rect)
        self.can_click_board = False
        pygame.display.update()

    def update_counter(self):
        temp = self.counter
        if self.counter < 0:
            temp *= -1
            bottom = self.rows * 32
            minus_sign_img = pygame.image.load("Assets/negative.png")
            self.window.blit(minus_sign_img, (0, bottom))
        else:
            pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(0, self.rows * 32, 21, 32))

        digit_1 = temp // 100
        temp %= 100
        digit_2 = temp // 10
        digit_3 = temp % 10

        digit_1_img = pygame.image.load("Assets/" + str(digit_1) + ".png")
        digit_2_img = pygame.image.load("Assets/" + str(digit_2) + ".png")
        digit_3_img = pygame.image.load("Assets/" + str(digit_3) + ".png")
        left = 21
        bottom = self.rows * 32
        self.window.blit(digit_1_img, (left, bottom))
        left += 21
        self.window.blit(digit_2_img, (left, bottom))
        left += 21
        self.window.blit(digit_3_img, (left, bottom))
        pygame.display.flip()  # todo update mine count

    def floodfill(self, tile):
        self.update_tile(tile)
        if tile.adjacent_mines == 0:
            if tile.flagged:
                tile.flagged = False
                self.counter += 1
            if tile.up is not None and not tile.up.revealed:
                self.floodfill(tile.up)
            if tile.right is not None and not tile.right.revealed:
                self.floodfill(tile.right)
            if tile.down is not None and not tile.down.revealed:
                self.floodfill(tile.down)
            if tile.left is not None and not tile.left.revealed:
                self.floodfill(tile.left)
            if tile.up_left is not None and not tile.up_left.revealed:
                self.floodfill(tile.up_left)
            if tile.up_right is not None and not tile.up_right.revealed:
                self.floodfill(tile.up_right)
            if tile.down_left is not None and not tile.down_left.revealed:
                self.floodfill(tile.down_left)
            if tile.down_right is not None and not tile.down_right.revealed:
                self.floodfill(tile.down_right)


class Tile:

    def __init__(self):
        self.has_mine = False
        self.uncovered = False
        self.adjacent_mines = 0
        self.flagged = False
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.up_left = None
        self.up_right = None
        self.down_left = None
        self.down_right = None
        self.image = pygame.image.load('Assets/tile_hidden.png')
        self.image_rect = None
        self.revealed = False

    def count_adj_mines(self):
        if self.left is not None and self.left.has_mine:
            self.adjacent_mines += 1
        if self.right is not None and self.right.has_mine:
            self.adjacent_mines += 1
        if self.up is not None and self.up.has_mine:
            self.adjacent_mines += 1
        if self.down is not None and self.down.has_mine:
            self.adjacent_mines += 1
        if self.up_left is not None and self.up_left.has_mine:
            self.adjacent_mines += 1
        if self.up_right is not None and self.up_right.has_mine:
            self.adjacent_mines += 1
        if self.down_left is not None and self.down_left.has_mine:
            self.adjacent_mines += 1
        if self.down_right is not None and self.down_right.has_mine:
            self.adjacent_mines += 1

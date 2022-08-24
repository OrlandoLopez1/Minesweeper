from Board import *

pygame.init()

rows = 9
cols = 9
run = True
# 16x25
h = (rows * 32) + 96
w = cols * 32
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Minesweeper')
win.fill((255, 255, 255))

game = Board(win, rows, cols, 1)
game.load_all_board_info()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1: # 1 == left click; 3 == right click
                game.update_board_state(mouse_pos)
            elif event.button == 3:
                game.place_flag(mouse_pos)

    # pygame.display.flip()
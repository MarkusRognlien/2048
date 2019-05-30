import pygame
import random
from roundrects import aa_round_rect

DIM = 4
TILE_SIZE = 100
MARGIN_SIZE = 50
SPACING = 4
SHARPNESS = 4
TEXT_HEIGHT = 30

SURFACE_WIDTH = 2 * MARGIN_SIZE + TILE_SIZE * DIM
SURFACE_HEIGHT = SURFACE_WIDTH + TEXT_HEIGHT
TOP_LEFT_X = MARGIN_SIZE
TOP_LEFT_Y = MARGIN_SIZE + TEXT_HEIGHT
INNER_TILE = (TILE_SIZE * DIM - (DIM + 1) * SPACING) // DIM
tile_colors = [(235, 167, 172), (136, 215, 151), (107, 189, 144), (79, 164, 142), (55, 136, 142), (36, 88, 114), (20, 46, 89),
               (9, 13, 64), (9, 13, 64), (9, 13, 64), (9, 13, 64), (9, 13, 64)]
tiles = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
white = (255, 255, 255)
pink = (235, 167, 172)
red = (255, 0, 0)
purple = (100, 20, 55)

pygame.font.init()
font = pygame.font.Font('ARCADE_I.TTF', TEXT_HEIGHT)
lose_font = pygame.font.Font('ARCADE_I.TTF', DIM*TILE_SIZE//6)
lose_subfont = pygame.font.Font('ARCADE_N.TTF', DIM*TILE_SIZE//20)
win = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))


def color_number(num):
    if num < 16:
        return purple
    else:
        return pink


display_numbers = [font.render(str(n), 1, color_number(n)) for n in tiles[1:]]


def fix_row(row):
    new_row = []
    row = [x for x in row if x != 0]
    for col in range(len(row) - 1):
        if row[col + 1] == row[col]:
            new_row.append(row[col] * 2)
            row[col + 1] = 0
        else:
            if row[col] != 0:
                new_row.append(row[col])
            if col == len(row) - 2:
                new_row.append(row[col + 1])
    if len(row) == 1:
        new_row = row
    return new_row + [0] * (DIM - len(new_row))


def random_free(grid):
    free = []
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == 0:
                free.append((y, x))

    return random.choice(free)


def place_new(grid):
    y, x = random_free(grid)
    grid[y][x] = 2
    return grid


def process_move(grid, move):
    if move == 0:
        new_board = [fix_row(row) for row in grid]
    elif move == 1:
        new_board = [list(fix_row(row.__reversed__()).__reversed__()) for row in rotate(grid)]
        for i in range(3):
            new_board = rotate(new_board)
    elif move == 2:
        new_board = [list(fix_row(row.__reversed__()).__reversed__()) for row in grid]
    else:
        new_board = [fix_row(row) for row in rotate(grid)]
        for i in range(3):
            new_board = rotate(new_board)

    if new_board == grid:
        valid = False
    else:
        valid = True

    return new_board, valid


def draw_game(surface, grid):
    draw_board(surface, grid)
    draw_score(surface, grid)
    pygame.display.update()


def rotate(grid):
    return [list(x) for x in zip(*grid[::-1])]


def calc_score(grid):
    score = 0
    for row in grid:
        for value in row:
            score += value

    return score


def draw_board(surface, board):
    surface.fill(pink)
    aa_round_rect(surface, (TOP_LEFT_X, TOP_LEFT_Y, TILE_SIZE*DIM + SPACING, TILE_SIZE*DIM + SPACING), purple,
                  rad=SHARPNESS)
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            aa_round_rect(surface, (TOP_LEFT_X + SPACING + x * TILE_SIZE, TOP_LEFT_Y + SPACING + y * TILE_SIZE,
                                    INNER_TILE, INNER_TILE), tile_colors[tiles.index(value)], rad=SHARPNESS)
            if value != 0:
                width = display_numbers[tiles.index(value) - 1].get_width()
                surface.blit(display_numbers[tiles.index(value) - 1],
                             (TOP_LEFT_X + SPACING + x * TILE_SIZE + (INNER_TILE - width)//2,
                              TOP_LEFT_Y + SPACING + y * TILE_SIZE + (INNER_TILE - TEXT_HEIGHT)//2))


def draw_score(surface, board):
    score_string = str(calc_score(board))
    score_string = "Score:" + "0" * (4 - len(score_string)) + score_string
    score_text = font.render(score_string, 1, purple)
    surface.blit(score_text, (TOP_LEFT_X, TOP_LEFT_Y - TEXT_HEIGHT))


def restart_screen(surface):
    response = False
    main_string = "YOU LOST"
    sub_string = "Press any key to restart"
    main_text = lose_font.render(main_string, 1, red)
    sub_text = lose_subfont.render(sub_string, 1, red)
    surface.blit(main_text, (TOP_LEFT_X + (TILE_SIZE*DIM - main_text.get_width())//2,
                             TOP_LEFT_Y + TILE_SIZE*DIM//3 - SURFACE_HEIGHT//12))
    surface.blit(sub_text, (TOP_LEFT_X + (TILE_SIZE*DIM - sub_text.get_width())//2,
                            TOP_LEFT_Y + TILE_SIZE*DIM//3 + SURFACE_HEIGHT//12))
    pygame.display.update()

    while not response:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return



def is_full(grid):
    for row in grid:
        for value in row:
            if value == 0:
                return False
    return True


def is_lost(grid):
    for move in range(4):
        fake_game, valid = process_move(grid, move)
        if valid:
            return False
    return True


def main():
    run = True
    move = 4
    game = [[0 for i in range(DIM)] for j in range(DIM)]
    place_new(game)
    draw_game(win, game)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move = 0
                elif event.key == pygame.K_UP:
                    move = 1
                elif event.key == pygame.K_RIGHT:
                    move = 2
                elif event.key == pygame.K_DOWN:
                    move = 3
                if move != 4:
                    game, valid = process_move(game, move)
                    move = 4
                    if valid:
                        place_new(game)
                        draw_game(win, game)
                        if is_lost(game):
                            restart_screen(win)
                            main()


main()

import pygame
import random
import string
from wonderwords import RandomWord
from wordsetup import WordSetup
from gameboard import GameBoard
from constants import LEFT_MARGIN, TOP_MARGIN, BOX_HEIGHT, BOX_WIDTH, MAUVE, BEIGE, GREEN, BOARD_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, BOARD_SIZE, WORD_COUNT, MIN_WORD_SIZE

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Search")
clock = pygame.time.Clock()

#fonts 
letter_font = pygame.font.Font(None, 36)
win_font = pygame.font.Font(None, 24)


# Setup game components
running = True
win_status = False

#generate words and coordinates of words
game = WordSetup(BOARD_SIZE, WORD_COUNT, MIN_WORD_SIZE)
# extract coordinates of target words
coordinates_list = game.coordinates_list
# extract target words
word_list = game.word_list

# generate random letters for coordinates without target words
board = GameBoard(screen, letter_font, win_font, BOARD_SIZE, coordinates_list, word_list)
# extract the letters for each coordinate on the board
board_letters = board.board_letters

while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #detect if player clicks on a letter to form a guess
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1:
                left_mouse_down = True
            else:
                left_mouse_down = False
            
            # check which box the coordinates fall under --> change colour of box 
            board.guess_word(mouse_x, mouse_y, left_mouse_down)

    # check game status
    win_status = board.game_status()

    # fill the screen with colour
    screen.fill(MAUVE)

    # render game board with letters
    board.render_board(board_letters)

    # if player has solved the word search display win message
    if win_status == True:
        board.win_message()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
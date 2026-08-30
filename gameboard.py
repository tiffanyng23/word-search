import pygame
import random
import string
from wonderwords import RandomWord
from constants import LEFT_MARGIN, TOP_MARGIN, BOX_HEIGHT, BOX_WIDTH, MAUVE, BEIGE, GREEN, BOARD_SIZE, BOX_SPACING, SCREEN_HEIGHT, SCREEN_WIDTH, WIN_MSG

class GameBoard:
    '''generate game board with the target words'''
    def __init__(self, screen, letter_font, win_font, board_size, coordinates_list, word_list):
        self.board_size = board_size
        self.coordinates_list = coordinates_list
        self.screen = screen
        self.letter_font = letter_font
        self.win_font = win_font
        self.guess_coords = []
        self.remove_guess_coords = []
        self.correct_word_coords = set()

        # store the board letters to feed into render_board()
        self.board_letters = self.generate_letters()

    def generate_letters(self):
        '''create dictionary to place letter for target words in the correct box, and
        generate a random letter for each box in the board with no target word'''

        board_letters = {}
        
        for row in range(self.board_size):
            for col in range(0, self.board_size):
                box_coords = (row, col)

                # generate random letter by default
                box_letter = random.choice(string.ascii_uppercase)

                #check each box to see if any letter from any of the target words should be there
                for assess_coords in self.coordinates_list:
                    # check if box coordinates matches any coordinates in assess coordinates
                    if box_coords in assess_coords:
                        # replace box letter to be the letter from the target word instead of default random letter
                        box_letter = assess_coords[box_coords]
                        break
                
                # update board_letters with the box_letter for the specific coordinates
                board_letters[box_coords] = box_letter
        return board_letters
       
    def render_board(self, board_letters):
        '''render game board with target words'''
        for row in range(0, self.board_size):
            for col in range(0, self.board_size):

                # check if a target word has been correctly guessed based on updated guess list
                self.correct_word()
                # update box to be green if it is a part of a correctly guessed word
                if (row, col) in self.correct_word_coords:
                    box_color = GREEN
                else:
                    # check if player clicked a specific box as a guess
                    if (row, col) in self.guess_coords:
                        box_color = BEIGE
                    else:
                        box_color = MAUVE

                # create a box to hold a letter
                pygame.draw.rect(self.screen, box_color, ((LEFT_MARGIN + BOX_SPACING * col), (TOP_MARGIN + BOX_SPACING * row), BOX_WIDTH, BOX_HEIGHT))

                # use (row,col) as key to find the letter
                #insert letter into box
                letter_surface = self.letter_font.render(board_letters[(row, col)], False, (0,0,0))
                center_x = LEFT_MARGIN + BOX_SPACING * col + BOX_WIDTH/2
                center_y = TOP_MARGIN + BOX_SPACING * row + BOX_HEIGHT/2
                letter_rect = letter_surface.get_rect(center=(center_x, center_y))
                self.screen.blit(letter_surface, letter_rect)
    
    def guess_word(self, mouse_x, mouse_y, left_mouse_down):
        '''allow user to tap on a letter to guess a letter'''
        # left click --> beige, right click --> mauve
        row = (mouse_y - TOP_MARGIN) // BOX_SPACING
        col = (mouse_x - LEFT_MARGIN) // BOX_SPACING

        if (row, col) not in self.guess_coords and left_mouse_down == True:
            self.guess_coords.append((row, col))
        # remove guess --> clear it from guess_coords list
        if (row, col) in self.guess_coords and left_mouse_down == False:
            self.guess_coords.remove((row, col))

    def correct_word(self):
        '''check if a guess completely matches a target word, then make boxes for that word turn green if correct'''
        # check if player guess matches a whole target word
        for word in self.coordinates_list:
            check_coords = set(word.keys()) 
            result = check_coords.issubset(set(self.guess_coords))
            if result == True:
                # add all box coordinates in the correct word to the correct_words set
                # these box coords must be green
                self.correct_word_coords.update(word)

    def game_status(self):
        '''check if player has guessed all the words, return True if all words have been found'''
        reference_coords = set()
        for word in self.coordinates_list:
            coords = set(word.keys())
            reference_coords.update(coords)
        # to win: correct_word_coords should include all the elements as the reference coordinates list
        if self.correct_word_coords == reference_coords:
            # player has won the game
            return True
        else:
            return False

    def win_message(self):
        # print "You have solved the word search!"
        win_surface = self.win_font.render(WIN_MSG, False, (0,0,0))
        center_x = SCREEN_WIDTH/2
        center_y = SCREEN_HEIGHT/16
        win_rect = win_surface.get_rect(center=(center_x, center_y))
        self.screen.blit(win_surface, win_rect)

import pygame
import random
import string
from wonderwords import RandomWord

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Word Search")
clock = pygame.time.Clock()

# game board variables
letter_font = pygame.font.Font(None, 36)
left_margin = 150
top_margin = 150
box_width = 150
box_height = 150

# game logic variables
MIN_WORD_SIZE = 4
WORD_COUNT = 10
BOARD_SIZE = 15

# classes
class WordSetup: 
    '''generate random word and determine coordinates on the board'''
    def __init__(self, board_size, word_count):
        self.board_size = board_size
        self.word_list = []
        self.coordinates_list = []

        for i in range(word_count):
            # generate random word
            self.word = self.render_word()
            #word gets adjusted to random orientation and added to the word list
            self.word_orientation(self.word)
        
        # take the completed target word list and determine position of eachword on the board
        self.word_position(self.word_list, self.coordinates_list)

    def render_word(self):
        '''generate random word'''
        r = RandomWord()
        # make sure word is not longer than the width/height of game board
        target_word = r.word(word_min_length= MIN_WORD_SIZE, word_max_length= self.board_size).upper()
        return target_word

    def word_orientation(self, word):
        '''determine orientation of the word and position on game board'''
        random_spelling = ["forward", "reverse"]
        spelling = random.choice(random_spelling)

        if spelling == "reverse":
            word = word[::-1]

        #add adjusted word to growing word list
        self.word_list.append(word)

        # return the adjusted word back and store it as self.adjusted_word
        return word


    def word_position(self, word_list, coordinates_list):
        for n, adjusted_word in enumerate(word_list):
            placed_word = False
            # if word has not been placed in coordinates list keep looping
            while not placed_word:
                random_word_dir = ["horizontal", "vertical", "down_diagonal", "up_diagonal"]
                word_length = len(adjusted_word)
                word_coords = {}

                # generate a direction for the word
                word_dir = random.choice(random_word_dir) 

                if word_dir == "horizontal":
                    # e.g. a 10 letter word cannot start past index 6 in a 16 column board (index 6 - index 15)
                    row = random.randint(0, self.board_size - 1)
                    col = random.randint(0, self.board_size - word_length)

                    # keep same row, column increase by 1 until the end of the word
                    # map each letter in the word to coordinates here
                    for n, letter in enumerate(adjusted_word):
                        word_coords[(row, col + n)] = letter
                elif word_dir == "vertical":
                    row = random.randint(0, self.board_size - word_length)
                    col = random.randint(0, self.board_size - 1)

                    # keep same col, increase row index by 1
                    for n, letter in enumerate(adjusted_word):
                        word_coords[(row + n, col)] = letter
                elif word_dir == "down_diagonal":
                    #diagonal - determine starting coordinates
                    row = random.randint(0, self.board_size - word_length)
                    col = random.randint(0, self.board_size - word_length)

                    for n, letter in enumerate(adjusted_word):
                        word_coords[(row + n, col + n)] = letter
                else:
                    # up diagonal
                    row = random.randint(word_length - 1, self.board_size - 1)
                    col = random.randint(0, self.board_size - word_length)

                    for n, letter in enumerate(adjusted_word):
                        word_coords[(row - n, col + n)] = letter

                # validation check
                valid_placement = self.validation_check(word_coords, coordinates_list)
                
                # pass validation check - add entry to coordinates list
                if valid_placement == True:  
                    coordinates_list.append(word_coords)
                    # break out of while loop and move to next word
                    placed_word = True
            
        print(coordinates_list)
    def word_intersection(self, current_word, last_mapped_word, coordinates_list):
        '''determine whether current word has any matching letters with previously mapped word'''
        last_mapped_word = coordinates_list[-1]
        candidate_intersections = []

        # check for any matching letters between the current word and previous word
        # identify the coordinates of the matching letter in the previously mapped word
        for last_coord, last_letter in last_mapped_word.items():
            for new_index, new_letter in enumerate(current_word):
                if last_letter == new_letter:
                    candidate_intersections.append((last_coord, new_index))

        # Randomnly select an interesection to use
        random.choice(candidate_intersections)

        # create tentative coordinates for the current_word
        # generate direction of word
        # map out coordinates

        return coordinates

    def validation_check(self, word_coords, coordinates_list):
        '''check if prospective coordinates for the word are valid'''
        valid_placement = True
        
        if len(coordinates_list) >= 1:
            for mapped_word in coordinates_list:
                overlaps = list(mapped_word.keys() & word_coords.keys())
                overlap_count = len(overlaps)
                # more than one set of coordinates overlap between prospective coordinates of a word
                # and already set coordinates of another word
                if overlap_count > 1:
                    valid_placement = False
                    break
                # check if overlap letter matches
                if overlap_count == 1:
                    overlap_coords = overlaps[0]
                    if mapped_word[overlap_coords] != word_coords[overlap_coords]:
                        valid_placement = False
                        break
                        
        return valid_placement

class GameBoard:
    '''generate game board with the target words'''
    def __init__(self, board_size, coordinates_list, word_list):
        self.board_size = board_size

        # store the board letters to feed into render_board()
        self.board_letters = self.generate_letters(coordinates_list, word_list)

    def generate_letters(self, coordinates_list, word_list):
        '''create dictionary to place letter for target words in the correct box, and
        generate a random letter for each box in the board with no target word'''

        box_letter = ""
        board_letters = {}
        
        for row in range(0, self.board_size):
            for col in range(0, self.board_size):
                box_coords = (row, col)
                #check each box to see if any letter from any of the target words should be there
                for assess_coords in coordinates_list:
                    # check if box coordinates matches any coordinates in assess coordinates
                    if box_coords in assess_coords:
                        #remove key:value from assess_coords dictionary and break
                        box_letter = assess_coords.pop(box_coords)
                        # add the box coordinates: letter pair to the board_letters dictionary
                        board_letters[box_coords] = box_letter
                        break
                    else:
                        # generate random letter for the box
                        box_letter = random.choice(string.ascii_uppercase)
                        # need to store the letter with the respective box coordinate
                        board_letters[box_coords] = box_letter
        return board_letters
       
    def render_board(self, board_letters):
        '''render game board with target words'''
        for row in range(0, self.board_size):
            for col in range(0, self.board_size):
                # create a box to hold a letter
                pygame.draw.rect(screen, "pink", ((left_margin + 30 * col), (top_margin + 30 * row), box_width, box_height))

                # use (row,col) as key to find the letter
                #insert letter into box
                letter_surface = letter_font.render(board_letters[(row, col)], False, (0,0,0))
                center_x = (10 + 30 * col) + box_width/2
                center_y = (10 + 30 * row) + box_height/2
                letter_rect = letter_surface.get_rect(center=(center_x, center_y))
                screen.blit(letter_surface, letter_rect)
    
    def guess_word():
        '''allow user to tap on a letter to build a guess'''
        pass               


running = True
win_status = False

# Setup game components once here to prevent new words/boards being rendered each frame
#generate words and coordinates of words
game = WordSetup(BOARD_SIZE, WORD_COUNT)
# extract coordinates of target words
coordinates_list = game.coordinates_list
# extract target words
word_list = game.word_list
print(word_list)
# generate random letters for coordinates without the target word
board = GameBoard(BOARD_SIZE, coordinates_list, word_list)
# extract the letters for each coordinate
board_letters = board.board_letters

while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # render game
    if win_status == False:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("pink")
        # render game board with letters
        board.render_board(board_letters)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
import pygame
import random
import string
from wonderwords import RandomWord

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Word Search")
clock = pygame.time.Clock()

# variables
letter_font = pygame.font.Font(None, 36)
left_margin = 150
top_margin = 150
box_width = 150
box_height = 150

# classes
class WordSetup: 
    '''generate game board with randomnly generated word correctly integrated into the board'''
    def __init__(self, board_size):
        self.board_size = board_size

        # generate random word
        self.word = self.render_word()

        # list of target words, create this since I eventually want to loop through multiple words
        self.word_list = []
        
        #word gets adjusted to random orientation and added to the word list
        self.adjusted_word = self.word_orientation(self.word)

        # list of coordinates for target words
        self.coordinates_list = []

        # take the adjusted word and determine position of word on the board
        self.word_position(self.adjusted_word, self.coordinates_list)


    def render_word(self):
        '''generate random word'''
        r = RandomWord()
        # make sure word is not longer than the width/height of game board
        target_word = r.word(word_min_length=4, word_max_length= self.board_size).upper()
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


    def word_position(self, adjusted_word, coordinates_list):
        # randomnly pick a row/col in the gameboard to insert the word
        # make sure word fits within boundaries of board
        random_word_dir = ["horizontal", "vertical", "down_diagonal", "up_diagonal"]
        word_dir = random.choice(random_word_dir) 

        # get word length
        word_length = len(adjusted_word)

        # store coordinates for each letter
        word_coords = {}
        
        if word_dir == "horizontal":
            # e.g. a 10 letter word cannot start past index 6 in a 16 column board (index 6 - index 15)
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - word_length)

            # keep same row, column increase by 1 until the end of the word
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

        # add entry to word list
        coordinates_list.append({adjusted_word : word_coords})
        print(coordinates_list)

    def word_overlap():
        '''make sure that each target word does not overlap
        more than one letter with another target word''' 
        pass

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
                #check each box to see if a letter from a target word should be in there or not
                # extract each target word dictionary mapping the coordinates to each letter in the word
                for coordinates,word in zip(coordinates_list, word_list):
                    assess_coords = coordinates[word]
                    # check if box_coords matches any coords (key) in assess_coords
                    if box_coords in assess_coords:
                        #remove key:value from assess_coords dictionary and break
                        box_letter = assess_coords.pop(box_coords)
                        # add the coords: letter pair to the board_letters dictionary
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
                
            
class GameScore:
    pass


running = True
found_word = False

# Setup game components once here to prevent new words/boards being rapidly generated
game = WordSetup(15)
coordinates_list = game.coordinates_list
word_list = game.word_list
board = GameBoard(15, coordinates_list, word_list)
board_letters = board.board_letters

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if found_word == False:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("pink")
        board.render_board(board_letters)
    
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
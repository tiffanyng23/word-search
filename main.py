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
left_margin = 80
top_margin = 80
box_width = 20
box_height = 20

# game logic variables
MIN_WORD_SIZE = 4
WORD_COUNT = 10
BOARD_SIZE = 15
WHITE = 255, 255, 255
BEIGE = 222, 212, 186

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
        
        # take the completed target word list and determine position of each word on the board
        self.word_position(self.word_list, self.coordinates_list)

        # render game board in a separate class

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
        '''determine coordinates of all the words'''
        for n, adjusted_word in enumerate(word_list):
            placed_word = False
            # if word has not been placed in coordinates list keep looping
            while not placed_word:
                # check for word intersection 75% of the time
                if len(coordinates_list) != 0 and random.random() < 0.75:
                    word_coords = self.word_intersection(adjusted_word, coordinates_list)
                    # if intersection is not possible
                    if word_coords == None:
                        word_coords = self.random_word_position(adjusted_word)
                else:
                    word_coords = self.random_word_position(adjusted_word)
                   
                # validation check
                valid_placement = self.validation_check(word_coords, coordinates_list)
                
                # pass validation check - add entry to coordinates list
                if valid_placement == True:  
                    coordinates_list.append(word_coords)
                    # break out of while loop and move to next word
                    placed_word = True
        
        print(coordinates_list)
    
    def word_intersection(self, current_word, coordinates_list):
        '''determine whether current word has any matching letters with previously mapped word and intersect if they do'''
        # retrieve most recently mapped word
        last_mapped_word = coordinates_list[-1]
        # store potential intersection coordinates
        candidate_intersections = []

        # check for any matching letters between the current word and previous word
        # identify the coordinates of the matching letter in the previously mapped word
        for last_coord, last_letter in last_mapped_word.items():
            # new index = index of letter in current word
            for new_index, new_letter in enumerate(current_word):
                if last_letter == new_letter:
                    candidate_intersections.append((last_coord, new_index))

        # no matching letters between current word and previous word
        if len(candidate_intersections) == 0:
            return None

        # Randomnly select an interesection to use
        intersect_coords = random.choice(candidate_intersections)

        # determine board boundaries based on intersection
        left_max_offset = intersect_coords[0][1]
        top_max_offset = intersect_coords[0][0]
        right_max_offset = (self.board_size - 1) - intersect_coords[0][1]
        bottom_max_offset = (self.board_size - 1) - intersect_coords[0][0]

        # determine which directions are possible and map coordinates
        directions = ["horizontal","vertical","down_diagonal","up_diagonal"]
        valid_directions = ["horizontal","vertical","down_diagonal","up_diagonal"]
        word_length = len(current_word)
        start_point = intersect_coords[1]
        baseline_coords = intersect_coords[0]

        for direction in directions:
            before_intersection = start_point
            after_intersection = (word_length - 1) - start_point
            # start coordinate check
            if direction == "horizontal":
                if before_intersection > left_max_offset:
                    valid_directions.remove(direction)
                    continue
                if after_intersection > right_max_offset:
                    valid_directions.remove(direction)
                    continue

            elif direction == "vertical":
                if before_intersection > top_max_offset:
                    valid_directions.remove(direction)
                    continue
                if after_intersection > bottom_max_offset:
                    valid_directions.remove(direction)
                    continue

            elif direction == "down_diagonal":
                if before_intersection > top_max_offset:
                    valid_directions.remove(direction)
                    continue
                if before_intersection > left_max_offset:
                    valid_directions.remove(direction)
                    continue
                if after_intersection > bottom_max_offset:
                    valid_directions.remove(direction)
                    continue
                if after_intersection > right_max_offset:
                    valid_directions.remove(direction)
                    continue

            elif direction == "up_diagonal":
                if before_intersection > bottom_max_offset:
                    valid_directions.remove(direction)
                    continue
                if before_intersection > left_max_offset:
                    valid_directions.remove(direction)
                    continue
                if after_intersection > top_max_offset:
                    valid_directions.remove(direction)
                    continue
                if after_intersection > right_max_offset:
                    valid_directions.remove(direction)
                    continue
        # if this particular intersection cannot be mapped in any direction
        if not valid_directions:
            return None
        # use valid directions to randomnly pick a valid direction
        word_direction = random.choice(valid_directions)
        
        # generate coordinates for the current_word
        word_coords = {}
        for n, letter in enumerate(current_word):
            offset = n - start_point
            if word_direction == "horizontal":
                row = baseline_coords[0] 
                col = baseline_coords[1] + offset
            elif word_direction == "vertical":
                row = baseline_coords[0] + offset
                col = baseline_coords[1] 
            elif word_direction == "down_diagonal":
                row = baseline_coords[0] + offset
                col = baseline_coords[1] + offset
            elif word_direction == "up_diagonal":
                row = baseline_coords[0] - offset
                col = baseline_coords[1] + offset

            word_coords[(row,col)] = letter
        return word_coords
    
    def random_word_position(self, adjusted_word):
        #randomnly place word on board
        random_word_dir = ["horizontal", "vertical", "down_diagonal", "up_diagonal"]
        word_length = len(adjusted_word)
        word_coords = {}

        # generate a direction for the word
        word_dir = random.choice(random_word_dir) 

        if word_dir == "horizontal":
            # determine valid starting coordinates for the word
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
        elif word_dir == "up_diagonal":
            row = random.randint(word_length - 1, self.board_size - 1)
            col = random.randint(0, self.board_size - word_length)

            for n, letter in enumerate(adjusted_word):
                word_coords[(row - n, col + n)] = letter
        return word_coords

    def validation_check(self, word_coords, coordinates_list):
        '''check if prospective coordinates for the word are valid. Do not want a word to intersect at more than 1 letter'''
        valid_placement = True
        
        if len(coordinates_list) >= 1:
            # go through each set of coordinates that are mapped to other words
            # check if there is more than one overlap per word
            for mapped_word in coordinates_list:
                overlaps = list(mapped_word.keys() & word_coords.keys())
                overlap_count = len(overlaps)
                # if more than one set of coordinates overlap between prospective coordinates of a word
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
        self.guess_coords = []

        # store the board letters to feed into render_board()
        self.board_letters = self.generate_letters(coordinates_list, word_list)

    def generate_letters(self, coordinates_list, word_list):
        '''create dictionary to place letter for target words in the correct box, and
        generate a random letter for each box in the board with no target word'''

        board_letters = {}
        
        for row in range(self.board_size):
            for col in range(0, self.board_size):
                box_coords = (row, col)

                # generate random letter by default
                box_letter = random.choice(string.ascii_uppercase)

                #check each box to see if any letter from any of the target words should be there
                for assess_coords in coordinates_list:
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

                # check if player clicked a specific box as a guess
                if (row, col) in self.guess_coords:
                    box_color = BEIGE
                else:
                    box_color = WHITE
                # create a box to hold a letter
                pygame.draw.rect(screen, box_color, ((left_margin + 30 * col), (top_margin + 30 * row), box_width, box_height))

                # use (row,col) as key to find the letter
                #insert letter into box
                letter_surface = letter_font.render(board_letters[(row, col)], False, (0,0,0))
                center_x = left_margin + 30 * col + box_width/2
                center_y = top_margin + 30 * row + box_height/2
                letter_rect = letter_surface.get_rect(center=(center_x, center_y))
                screen.blit(letter_surface, letter_rect)
    
    def guess_word(self, mouse_x, mouse_y):
        '''allow user to tap on a letter to build a guess'''
        # store coordinates that need to be beige in a list
        row = (mouse_y - top_margin) // 30
        col = (mouse_x - left_margin) // 30

        if (row, col) not in self.guess_coords:
            self.guess_coords.append((row,col))


running = True
win_status = False

# Setup game components
#generate words and coordinates of words
game = WordSetup(BOARD_SIZE, WORD_COUNT)
# extract coordinates of target words
coordinates_list = game.coordinates_list
# extract target words
word_list = game.word_list
print(word_list)
# generate random letters for coordinates without target words
board = GameBoard(BOARD_SIZE, coordinates_list, word_list)
# extract the letters for each coordinate on the board
board_letters = board.board_letters

while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #detect if player clicks on a letter to form a guess
        if event.type == pygame.MOUSEBUTTONDOWN and event.button:
            mouse_x, mouse_y = event.pos
            # check which box the coordinates fall under --> change colour of box to beige 
            board.guess_word(mouse_x, mouse_y)

    # render game board
    if win_status == False:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(WHITE)
        # render game board with letters
        board.render_board(board_letters)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
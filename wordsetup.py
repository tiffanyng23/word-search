import pygame
import random
import string
from wonderwords import RandomWord
from constants import BOARD_SIZE, WORD_COUNT, MIN_WORD_SIZE

class WordSetup: 
    '''generate random word and determine coordinates on the board'''
    def __init__(self, board_size, word_count, min_word_size):
        self.board_size = board_size
        self.min_word_size = min_word_size
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
        target_word = r.word(word_min_length= self.min_word_size, word_max_length= self.board_size).upper()
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
        print(f"Word List: {word_list}")
        print(f"Answer Key: {coordinates_list}")
    
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


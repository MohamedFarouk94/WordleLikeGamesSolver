'''
This file contains the structure of the language by defining two classes, which
are: Word and Language.

File contents:
    imports
    class Word:
        Constructor
        Methods:
            calc_prob
            calc_possible_points
            calc_info
            copy
    class Language:
        Constructor
        Functions to add/remove words to/from the language:
            add_word
            remove_word
        Functions to apply on all the words of the language:
            update_prob
            update_possible_points
            update_info
        Functions to apply on the language globally:
            sort
            massive_remove
            update_everything
            print
        A function to save tha language as csv file:
            to_csv
'''


from math import log2, ceil
from tqdm import tqdm
from game_core import comparen
import pandas as pd
from copy import deepcopy


class Word():
    '''
    Class of word
    Static Variables:
        length: int, the exact valid length (number of characters) of every word
    Dynamic Variables:
        str: string, the actual word in lower case [Unchangeable]
        points: numerical value, represents the popularity of the word [Unchangeable]
        list_of_all_possible_points: list of (3^length) numerical values,
            each index represents specific color pattern, and each value represents
            sum of all points we can get from this pattern with this word
        prob: float between 0 and 1, probability of appearing for this word
        info: float, expected information we can get by choosing this word
    '''
    length = 5

    def change_length(new_length):
        Word.length = new_length


    def __init__(self, str='', points=0):
        '''
        Constructor for the Word object
        Parameters:
            str: string, the actual word in any letter case
            points: numerical value, represents the popularity of the word
        '''

        # Unchangeable
        self.str = str.lower()
        self.points = points

        # Changeable
        self.list_of_all_possible_points = [0] * (3**Word.length)   # initially
        self.prob = 0    # initially
        self.info = 0    # initially

    # Methods of Word class

    def calc_prob(self, total_points):
        '''
        Calculating probability of this word
        Parameters:
            total_points: numerical value, summation of all points of all words
        Return:
            None, working inplace and updating self.prob
        '''
        self.prob = self.points/total_points

    def calc_possible_points(self, language_dict):
        '''
        Calculating possible points of each pattern we may get
        Parameters:
            language_dict: dictionary, key = words in strings, values = word objects of the all available words
        Return:
            None, working inplace and updating self.list_of_all_possible_points
        '''
        self.list_of_all_possible_points = [0] * (3**Word.length)
        for word_ in language_dict:
            self.list_of_all_possible_points[comparen(self.str, word_)] +=\
                language_dict[word_].points

    def calc_info(self):
        '''
        Calculating expected information
        Parameters:
            None
        Return:
            None, working inplace and updating self.info
        '''
        ss = sum(self.list_of_all_possible_points)
        self.info = sum([pts/ss * log2(ss/pts) for pts in self.list_of_all_possible_points if pts])

    def copy(self):
        '''
        Copying the word object (Useful in multiprocessing)
        Parameters:
            None
        Return:
            Word object, a copy
        '''
        copied_word = Word(str=self.str, points=self.points)
        copied_word.info = self.info
        copied_word.prob = self.prob
        copied_word.list_of_all_possible_points = self.list_of_all_possible_points.copy()
        return copied_word


class Language():
    '''
    Class of language
    Static Variables:
        None
    Dynamic Variables:
        total_points: numerical value, summation of the points of all words in language
        all_words: dictionary, keys = string words, values = word objects
        alphabet: list of character constants, contains all valid characters
    '''

    def __init__(self, alphabet=[], length=5, from_csv=''):
        '''
        Constructor of the Language object
        Parameters:
            alphabet: list of characters, contains all valid characters
            from_csv: string, empty or path of csv file
                if empty then the language is initially empty,
                if such file exists then it will be uploaded
        '''
        self.total_points = 0  # initially
        self.all_words = {}  # initially
        self.length = Word.length = length   #permenantly
        self.alphabet = alphabet.copy()  # permenantly

        if from_csv:
            df = pd.read_csv(from_csv)
            for _, row in tqdm(df.iterrows()):
                word = Word(str(row.Word), row.Points)
                self.add_word(word)
                word.info = row.Info

    # Methods to add/remove words to/from language

    def add_word(self, word):
        '''
        Adding word to the language (the word itself, not a copy)
        Parameters:
            word: Word object, to be added
        Return:
            None, working inplace and updating self.all_words and self.total_points
        '''
        self.all_words[word.str] = word
        self.total_points += word.points

    def remove_word(self, word):
        '''
        Removing word from the language
        Parameters:
            word: Word object, to be removed
        Return:
            None, working inplace and updating self.all_words and self.total_points
        '''
        self.total_points -= word.points
        del self.all_words[word.str]

    # Methods to apply on all the words of the language
    # All of them start with 'update_'
    # Note: from now on 'word' is a Word object while 'word_' is a string

    def update_prob(self, progress_bar=False):
        '''
        Updating probability of every word in the language
        Parameters:
            None
        Return:
            None, working inplace and updating every word in self.all_words
        '''
        iterative_object = tqdm(
            self.all_words) if progress_bar else self.all_words
        for word_ in iterative_object:
            self.all_words[word_].calc_prob(self.total_points)

    def update_possible_points(self, progress_bar=False):
        '''
        Updating possible points of every word in the language
        Parameters:
            None
        Return:
            None, working inplace and updating every word in self.all_words
        '''
        iterative_object = tqdm(
            self.all_words) if progress_bar else self.all_words
        for word_ in iterative_object:
            self.all_words[word_].calc_possible_points(self.all_words)

    def update_info(self, progress_bar=False):
        '''
        Updating expected information of every word in the language
        Parameters:
            None
        Return:
            None, working inplace and updating every word in self.all_words
        '''
        iterative_object = tqdm(self.all_words) if progress_bar else self.all_words
        for word_ in iterative_object:
            self.all_words[word_].calc_info()

    # Functions to apply on the language globally

    def sort(self):
        '''
        Sorting all the words of the language by their expected information
        Parameters:
            None
        Return:
            None, working inplace and updating self.all_words
        '''
        self.all_words = {word_: word for word_, word in sorted(self.all_words.items(),
                                                                key=lambda x: (
                                                                    x[1].info, x[1].prob),
                                                                reverse=True)}

    def massive_remove(self, word_='', pattern=0):
        '''
        Removing all words except those which meet the pattern with some specific word
        Parameters:
            word_: string, the specific word
            pattern: int, a pattern of colors mapped to a decimal value
        Return:
            None, working inplace and updating self.all_words
        '''
        iterative_copy = self.all_words.copy()
        for some_word_ in iterative_copy:
            word = iterative_copy[some_word_]
            if comparen(word_, word.str) != pattern:
                self.remove_word(word)

    def update_everything(self, prob_bar=False, pts_bar=False, info_bar=False):
        '''
        Calling all 'update_' functions
        Parameters:
            prob_bar: boolean, if update_prob progress bar is activated
            pts_bar: boolean, if update_possible_points progress bar is activated
            info_bar: boolean, if update_info progress bar is activated
        Return:
            None, working inplace and updating self.all_words and its elements
        '''
        self.update_prob(progress_bar=prob_bar)
        self.update_possible_points(progress_bar=pts_bar)
        self.update_info(progress_bar=info_bar)
        self.sort()

    def print(self, k=10):
        '''
        Not actually printing anythin, but returning logs summary including the
        best k words to guess
        Parameters:
            k: int, number of words which will be printed
        Return:
            string, a brief summary of the game situation
        '''
        output = f'there are {len(self.all_words)} available words.\n'
        output += "{:<4} {:<10} {:<20} {:30}".format(
            '#', 'word', 'info', 'prob')
        output += "\n"
        for i, word_ in enumerate(self.all_words):
            if i == k:
                return output
            word = self.all_words[word_]
            output += "{:<4} {:<10} {:<20} {:<30}".format(
                i+1, word.str, round(word.info,4), round(word.prob,4))
            output += "\n"
        return output

    # Saving language as csv file

    def to_csv(self, file_name='language.csv'):
        '''
        Saving the language as csv file
        Parameters:
            file_name: string, destination file path
            list_chunk: int, length of each of the mini-lists which every word's
                list_of_all_possible_points will be chunked into
        Return:
            None
        '''
        dict = {'Word': [], 'Points': [], 'Info': []}

        for word_ in tqdm(self.all_words):
            word = self.all_words[word_]
            dict['Word'].append(word.str)
            dict['Points'].append(word.points)
            dict['Info'].append(word.info)

        df = pd.DataFrame(dict)
        df.to_csv(file_name, index=False)

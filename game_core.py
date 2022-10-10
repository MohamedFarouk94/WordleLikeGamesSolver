'''
This file contains the core or the backend of the game in addition to simple
low level input/output functions.
Here there are no objects or any high level approaches but only dealing with
strings, numerical variables and lists.

File contents:
    imports
    Colors (and other commands) for terminals
    Functions to check the validity of words and color patterns:
        check_word
        check_pattern
    Functions to compute game core calculations:
        compare
        comparen
        gotit
        choose_word
    Functions to scan words or patterns from terminal or GUI:
        scan_language
        listen_language
        scan_mode
        listen_mode
        scan_word
        listen_word
        scan_theword
        take_theword
        scan_pattern
        listen_pattern
    Functions to display outputs in terminal or GUI:
        print_error
        print_word
        send_word
        print_summary
        send_summary
        print_end
        disp_end
'''

from random import choices
import game_gui as gg

# Colors (and other commands) for terminals
_GRAY = "\033[100m"
_GREEN = "\033[42m"
_YELLOW = "\033[43m"
ARRAY_OF_COLORS = [_GRAY, _YELLOW, _GREEN]
_REDFONT = "\033[31m"
_GREENFONT = "\033[32m"
_RESET = "\033[0m"
_ERASE = "\033[A                             \033[A"


# Checking the validity of words and color patterns

def check_word(alphabet=[], language_dict={}, length=5, word=''):
    '''
    Check if a given word is valid
    A given word is valid if and only if it's totally consisted of characters
    in the selected alphabet (if such one is selected), and the word itself is
    in the selected language (if such one is selected), and its length is equal
    to the selected length.

    Parameters:
        alphabet: list of chars, contains all valid chars, if empty then ignore alphabet check
        language_dict: list of strings or dictionary with string keys, of all valid words, if empty then ignore language check
        length: int, the exact valid length of the word
    Return:
        boolean, True if the word is valid, False otherwise
    '''
    res = len(word) == length
    res = res and not (len(alphabet) > 0 and sum(
        [1 for ch in word if ch not in alphabet]))
    res = res and (not language_dict or word in language_dict)
    return res


def check_pattern(length=5, pattern=''):
    '''
    Check if given pattern is valid
    A pattern is valid if and only if it's consisted of 0s, 1s and 2s in char
    data type (not integers) 0 represents black, 1 represents yellow and 2
    represents green.
    Parameters:
        length: valid length of word
        pattern: list of chars or string, represents pattern as explained above
    Return:
        boolean, True if pattern is valid, False otherwise
    '''
    return len(pattern) == length\
            and sum([1 for ch in pattern if ch in ['0', '1', '2']]) == length


# Computing the game core calculations


def compare(word='', the_word=''):
    '''
    Compare two words to give a pattern that represents a sequence of colors
    Parameters:
        word: string, a valid guess (check_word(word) == True is gauranteed)
        the_word: string, which should be treated as the actual solution (check_word(word) == True is gauranteed)
    Return:
        list of chars, a pattern of coded colors as explained in the previous function
    '''
    pattern = ['0'] * len(word)
    word_list = list(word)
    theword_list = list(the_word)

    # Green path
    for i, (ch1, ch2) in enumerate(zip(word_list, theword_list)):
        if ch1 == ch2:
            pattern[i] = '2'
            theword_list[i] = 0

    # Yellow path
    for i, (ch,pat) in enumerate(zip(word_list, pattern)):
        if pat != '2' and ch in theword_list:
            pattern[i] = '1'
            theword_list.remove(ch)

    return pattern


def comparen(word='', the_word=''):
    '''
    The same as compare but returns a mapped decimal value instead of pattern list
    Parameters:
        word: as word in the previous function
        the_word: as the_word in the previous function
    Return:
        int, a decimal value by reading the pattern string as an integer in base 3
    '''
    return int(''.join(compare(word=word, the_word=the_word)), 3)


def gotit(pattern='', length=5):
    '''
    Checking if the player gets the right answer
    Parameters:
        pattern: string, representing the color sequence of the last guess
        length: int, number of characters of the word
    Return:
        boolean, True if player gets it, False otherwise
    '''
    return int(pattern,3) == 3**length - 1


def choose_word(language_dict={}, list_of_points=[]):
    '''
    Choosing word according to language words probability distribution instead
    of scanning it
    Parameters:
        language_dict: dictionary with keys = word strings
        list_of_points: list of numerical values, words' corresponding weights
    Return:
        string, a chosen word
    '''
    return choices(list(language_dict), weights=tuple(list_of_points), k=1)[0]


# Scanning functions


def scan_language():
    '''
    Scan language from terminal in the begining of the game
    Parameters:
        None
    Return:
        string, the selected language
    '''
    languages = ['engwordle', 'primel', 'nerdle']
    while True:
        for i, language in enumerate(languages):
            print(f'For {language} press {i+1}')
        print("")
        try:
            x = int(input())
            return languages[x-1]
        except:
            print_error('INPUT')


def listen_language():
    '''
    Scan language from GUI in the begining of the game
    Parameters:
        None
    Return:
        string, the selected language
    '''
    while not gg.LANGUAGE['ready']:
        pass

    language = gg.LANGUAGE['value']
    gg.LANGUAGE['accepted'] = True
    return language



def scan_mode():
    '''
    Scan mode from terminal in the begining of the game
    Parameters:
        None
    Return:
        string, the selected mode
    '''
    modes = ['with', 'against', 'multi']
    descriptions = ['Playing with computer', 'Playing against computer', 'Two players']
    while True:
        for i, description in enumerate(descriptions):
            print(f'For {description} press {i+1}')
        print("")
        try:
            x = int(input())
            return modes[x-1]
        except:
            print_error('INPUT')


def listen_mode():
    '''
    Scan mode from GUI in the begining of the game
    Parameters:
        None
    Return:
        string, the selected mode
    '''
    while not gg.MODE['ready']:
        pass

    mode = gg.MODE['value']
    gg.MODE['accepted'] = True
    return mode


def scan_word(alphabet=[], language_dict={}, length=5):
    '''
    Scan word from terminal
    Parameters:
        alphabet: as alphabet in check_word function
        language_dict: as language_dict in check_word function
        length: as length in check_word function
    Return:
        string, a valid word
    '''
    while True:
        word = input()
        word = word.lower()
        if check_word(alphabet=alphabet, language_dict=language_dict, length=length, word=word):
            return word
        print_error('WORD')


def listen_word(alphabet=[], language_dict={}, length=5):
    '''
    Scan word from gui
    Parameters:
        alphabet: as alphabet in check_word function
        language_dict: as language_dict in check_word function
        length: as length in check_word function
    Return:
        string, a valid word
    '''
    pass    #TBC


def scan_theword(alphabet=[], language_dict={}, length=5):
    '''
    Scan the target word from terminal
    Parameters:
        alphabet: as alphabet in check_word function
        language_dict: as language_dict in check_word function
        length: as length in check_word function
    Return:
        string, a valid word
    '''
    global _ERASE
    print("Player to enter the target word (The other player will have to go away a little bit!!:)")
    word = scan_word(alphabet=alphabet, language_dict=language_dict, length=length)
    print(_ERASE,_ERASE,"\n")
    return word


def take_theword(alphabet=[], language_dict={}, length=5):
    '''
    Scan the target word from GUI
    Parameters:
        alphabet: as alphabet in check_word function
        language_dict: as language_dict in check_word function
        length: as length in check_word function
    Return:
        string, a valid word
    '''
    while True:
        while not gg.THE_WORD['ready']:
            pass

        the_word = gg.THE_WORD['value']
        if check_word(alphabet=alphabet, language_dict=language_dict, length=length, word=the_word):
            gg.THE_WORD['accepted'] = True
            return the_word

        gg.THE_WORD['ready'] = False
        gg.THE_WORD['rejected'] = True


def scan_pattern(length=5):
    '''
    Scan pattern in terminal
    Parameters:
        length: as length in check_pattern function
    Return:
        string, a valid pattern
    '''
    global _ERASE
    while True:
        pattern = input()
        print(_ERASE)
        if check_pattern(length=length, pattern=pattern):
            return pattern
        print_error('PATTERN')


def listen_pattern(length=5):
    '''
    Scan word from GUI
    Parameters:
        length: as length in check_pattern function
    Return:
        string, a valid pattern
    '''
    pass    #TBC


# Displaying functions


def print_error(msg='WORD'):
    '''
    Print error message in terminal
    Parameters:
        msg: string ('WORD', 'PATTERN' or 'INPUT')
    Return:
        None
    '''
    global _REDFONT, _ERASE, _RESET

    print('\n',_ERASE, _REDFONT, 'NOT A VALID', msg, _RESET)


def print_word(word='', pattern=''):
    '''
    Print word in terminal according to a given color-coded pattern
    Parameters:
        word: string, a valid word
        pattern: list of chars or string, a valid pattern
    Return:
        None
    '''
    global ARRAY_OF_COLORS, _ERASE

    word = word.upper()
    print('\n',_ERASE, end='')
    for pat, ch in zip(pattern, word):
        print(ARRAY_OF_COLORS[ord(pat)-ord('0')], ch, end='')
    print(_RESET)


def send_word(word='', pattern=''):
    '''
    sending word to display in GUI according to a given color-coded pattern
    Parameters:
        word: string, a valid word
        pattern: list of chars or string, a valid pattern
    Return:
        None
    '''
    pass    #TBC


def print_summary(message=''):
    '''
    Printing reported summary in terminal
    Parameters:
        message: string, reported summary of the situation
    Return:
        None
    '''
    print('\n'+message+'\n')


def send_summary(message=''):
    '''
    Displaying reported summary in GUI
    Parameters:
        message: string, reported summary of the situation
    Return:
        None
    '''
    pass    #TBC


def print_end(winning_flag=False, score=6, the_word=''):
    '''
    Printing game over in terminal
    Parameters:
        winning_flag: boolean, True when win and False when lose
        score: int, number of guesses that were used in the game (only when winning_flag is True)
        the_word: string, the right answer (only when winning_flag is False)
    Return:
        None
    '''
    global _GREENFONT, _REDFONT, _RESET

    if winning_flag:
        print(_GREENFONT, 'You Won in', score, '!', _RESET)
    else:
        print(_REDFONT, 'Game Over! The ward was ', the_word, _RESET)


def disp_end(winning_flag):
    '''
    Displaying game over in GUI
    Parameters:
        winning_flag: boolean, True when win and False when lose
    Return:
        None
    '''
    pass    #TBC

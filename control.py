'''
This file contains functions that controls the input/output processes simply by
calling game_core input/output functions.

File contents:
    imports
    Functions:
        Input functions:
            get_language
            get_mode
            get_theword
            get_word
            get_pattern
        Output functions:
            disp_word
            summary
            end_game
        Functions to get game and language Parameters:
            get_lang_params
            get_params
'''

import game_core as gc


# Input functions

def get_language(type='io'):
    '''
    Getting language from any available way in the begining of game
    Parameters:
        type: string ('io' or 'gui'), if 'io' language will be scanned from terminal,
            otherwise it will be scanned from GUI
    Return:
        string, the selected language
    '''
    if type == 'io':
        return gc.scan_language()

    else:   #type == 'gui'
        return gc.listen_language()


def get_mode(type='io'):
    '''
    Getting mode from any available way in the begining of game
    Parameters:
        type: string ('io' or 'gui'), if 'io' mode will be scanned from terminal,
            otherwise it will be scanned from GUI
    Return:
        string, the selected mode
    '''
    if type == 'io':
        return gc.scan_mode()

    else:   #type == 'gui'
        return gc.listen_mode()


def get_theword(type='none', language=None):
    '''
    Getting THE word (the solution word) from any available way
    Parameters:
        type: string ('io', 'gui', 'bg', 'none'), if 'io' word will be scanned
            from terminal, elif 'gui' word will be scanned from GUI, elif 'bg'
            word will not be scanned but chosen randomly instead, otherwise there
            won't be a solution word at all
        language: language object (will be used only if type == 'bg')
        length: int, the exact number of characters of the word
    Return:
        string, a chosen word
    '''
    if type == 'io':
        return gc.scan_theword(alphabet=language.alphabet, language_dict=language.all_words, length=language.length)

    if type == 'gui':
        return gc.take_theword()  # TBC

    if type == 'bg':
        list_of_points = [language.all_words[word_].points for word_ in language.all_words]
        return gc.choose_word(language_dict=language.all_words, list_of_points=list_of_points)

    # if type == 'nan'
    return ''


def get_word(type='io', alphabet=[], language_dict={}, length=5):
    '''
    Getting word from any available way
    Parameters:
        type: string ('io' or 'gui'), if 'io' word will be scanned from terminal,
            otherwise it will be scanned from GUI
        alphabet: list of characters, of all valid characters of the language
        language_dict: list of all words as strings or dictionary with keys = words as strings
        length: int, the exact number of characters of the word
    Return:
        string, a valid word
    '''
    if type == 'io':
        return gc.scan_word(alphabet=alphabet, language_dict=language_dict, length=length)

    # if type == 'gui':
    return gc.listen_word()  # TBC


def get_pattern(type='io', length=5, word='', the_word=''):
    '''
    Getting pattern from any available way
    Parameters:
        type: string ('io', 'gui' or 'bg'), if 'io' pattern will be scanned from
            terminal, elif 'gui' pattern will be scanned from GUI, otherwise it
            will not be scanned but instead it will be calculated according to
            both the entered guess and the solution in the background
        length: int, the exact number of characters of the word
        word: string, the user guess (will be used only if type = 'bg')
        the_word: string, the right solution in the background (will be used only if type = 'bg')
    Return:
        string, a valid pattern
    '''
    if type == 'io':
        return gc.scan_pattern(length=length)

    if type == 'gui':
        return gc.listen_pattern()  # TBC

    # if type == 'bg'
    return ''.join(gc.compare(word, the_word))


# Output functions

def disp_word(type='io', word='', pattern=''):
    '''
    Displaying word by any available way
    Parameters:
        type: string ('io' or 'gui'), if 'io' word will be printed in terminal
            otherwise it will be displayed via GUI
        word: string, a word to be displayed
        pattern: string, a pattern to be displayed
    Return:
        None
    '''
    if type == 'io':
        gc.print_word(word=word, pattern=pattern)

    else:  # type == 'gui'
        gc.send_word()  # TBC


def summary(type='io', message = ''):
    '''
    Displaying the summary of the situation by any available way
    Parameters:
        type: string ('io' or 'gui'), if 'io' summary will be printed in terminal
            otherwise it will be displayed via GUI
        message: string, contains the reported summary
    Return:
        None
    '''
    if type == 'io':
        gc.print_summary(message)
    else:   #GUI
        gc.send_summary(message)    #TBC


def end_game(type='io', winning_flag=True, score=6, the_word=''):
    '''
    Displaying the end game message by any available way
    Parameters:
        type: string ('io' or 'gui'), if 'io' message will be printed in terminal
            otherwise it will be displayed via GUI
        winning_flag: boolean, True if player won, False if lose
        score: int, number of total guesses till player won (Will be used only if winning_flag == True)
        the_word: string, the solution (Will be used only if winning_flag == False)
    Return:
        None
    '''
    if type == 'io':
        gc.print_end(winning_flag=winning_flag, score=score, the_word=the_word)
    else:   #GUI
        pass    #TBC


# Functions to get game and language Parameters

def lang_params(language='engwordle'):
    '''
    Getting alphabet, length and number of tryouts for a specific language
    Parameters:
        language: string, a specific language (has to be the same as the language python file name)
    Return:
        dictionary, keys are 'alphabet', 'length' & 'n_tryouts', values are the corresponding values
    '''
    language_library = __import__(language)
    lang_params = {'alphabet': language_library.alphabet,
                   'length': language_library.length,
                   'n_tryouts': language_library.n_tryouts}
    return lang_params


def mode_params(type='io', mode='with'):
    '''
    Getting the types of functions get_word, disp_word, end_game, get_theword, get_pattern & print
    Parameters:
        type: string ('io' or 'gui') the interface of game
        mode: string ('with', 'against' or 'multi') mode of the game
    Return:
        dictionary, keys are functions' names as strings, values are the corresponding values
    '''
    params = {}

    if type == 'io':
        params['get_word'] = 'io'
        params['disp_word'] = 'io'
        params['end_game'] = 'io'


        if mode == 'with':
            params['get_theword'] = 'none'
            params['get_pattern'] = 'io'
            params['print'] = True

        elif mode == 'against':
            params['get_theword'] = 'bg'
            params['get_pattern'] = 'bg'
            params['print'] = False


        else:    #mode == 'multi'
            params['get_theword'] = 'io'
            params['get_pattern'] = 'bg'
            params['print'] = False

    else:   #type == 'gui'
        params['get_word'] = 'gui'
        params['disp_word'] = 'gui'
        params['end_game'] = 'gui'

        if mode == 'with':
            params['get_theword'] = 'none'
            params['get_pattern'] = 'gui'
            params['print'] = True

        elif mode == 'against':
            params['get_theword'] = 'bg'
            params['get_pattern'] = 'bg'
            params['print'] = False


        else:    #mode == 'multi'
            params['get_theword'] = 'gui'
            params['get_pattern'] = 'bg'
            params['print'] = False

    return params

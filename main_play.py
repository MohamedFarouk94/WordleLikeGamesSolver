'''
This file contains the main procedure of the game

File contents:
    imports
    class Game:
        Constructor
        Methods:
            play
    Main Code
'''


import control as ctrl
from language import Language
from game_core import gotit


class Game():
    '''
    Class of Game
    Static Variables:
        None
    Dynamic Variables:
        n_tryouts: int, number of available guesses
        language: Language object, the language of the game
    '''
    def __init__(self, language='engwordle'):
        '''
        Constructor of the Game object
        Parameters:
            language: string, the language of the game
        '''
        lang_params = ctrl.get_lang_params(language)
        self.n_tryouts = lang_params['n_tryouts']
        self.language = Language(alphabet=lang_params['alphabet'],
                                length=lang_params['length'],
                                from_csv=language+'.csv')


    def play(self, type='io', mode='with'):
        '''
        Playing main procedure
        Parameters:
            type: string ('io' or 'gui') the interface of game
            mode: string ('with', 'against' or 'multi') mode of the game
        Return:
            None
        '''
        params = ctrl.get_params(type=type, mode=mode)
        the_word = ctrl.get_theword(type=params['get_theword'],
                                    language=self.language)

        print("")

        for i in range(self.n_tryouts):
            if params['print']:
                ctrl.summary(type=params['disp_word'], message=self.language.print())

            word_ = ctrl.get_word(type=params['get_word'],
                                  alphabet=self.language.alphabet,
                                  language_dict=self.language.all_words,
                                  length=self.language.length)

            pattern = ctrl.get_pattern(type=params['get_pattern'],
                                       length=self.language.length,
                                       word=word_, the_word=the_word)

            ctrl.disp_word(type=params['disp_word'], word=word_, pattern=pattern)


            if gotit(pattern=pattern, length=self.language.length):
                ctrl.end_game(type=params['end_game'], winning_flag=True, score=i+1)
                return

            if i == self.n_tryouts - 1:
                ctrl.end_game(type=params['end_game'], winning_flag=False, the_word=the_word)
                return

            self.language.massive_remove(word_=word_, pattern=int(pattern,3))
            self.language.update_everything()

            if not len(self.language.all_words):
                print('Something went wrong!')
                exit()


# # # # # # MAIN # # # # # #
'''
A simple main code, creating a Game object then calling play function
'''
game = Game(language=ctrl.get_language())
game.play(type='io', mode=ctrl.get_mode())

import pandas as pd
from language import Word, Language
from tqdm import tqdm


lower_letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
upper_letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]
alphabet = lower_letters + upper_letters
length = 5
n_tryouts = 6


def install():
    '''
    Installing function
    To be called only once, then the language will be saved in a csv file
    Parameters:
        None
    Return:
        None
    '''

    # Preparing alphabet
    lower_letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    upper_letters = [chr(i) for i in range(ord('A'), ord('Z')+1)]

    # Handling json file
    df = pd.read_json('english.json', orient='index')
    df = df.reset_index()
    df.rename(columns={'index': 'Word', 0: 'Points'}, inplace=True)

    # Creating an empty language object
    engwordle = Language(alphabet=lower_letters+upper_letters, length=5)

    # Adding all words
    for i, row in tqdm(df.iterrows()):
        word = Word(str=row['Word'], points=row['Points'])
        engwordle.add_word(word)

    # Doing all the information job
    engwordle.update_everything(True, True, True)

    # Saving language
    engwordle.to_csv(file_name='engwordle.csv')

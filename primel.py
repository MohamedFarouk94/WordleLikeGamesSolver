from math import sqrt
from language import Word, Language


alphabet = [chr(i) for i in range(ord('0'), ord('9')+1)]
length = 5
n_tryouts = 6


def isprime(n):
    '''
    The classic algorithm for checking if n is prime
    Parameters:
        n: int, to check if it is a prime or not
    Return:
        boolean, True if prime and False if not
    '''
    if n < 2:
        return False

    if n < 4:
        return True

    sqrtn = int(sqrt(n)) + 1
    for i in range(2, sqrtn):
        if n % i == 0:
            return False
    return True


def create():
    '''
    Creating all prime numbers between 10,000 and 99,999
    Parameters:
        None
    Return:
        list of strings, NOT INTEGERS, of all five-digit prime numbers
    '''
    primes = []
    for i in range(10000, 99999):
        if isprime(i):
            primes.append(str(i))
    return primes


def install():
    '''
    Installing function
    To be called only once, then the language will be saved in a csv file
    Parameters:
        None
    Return:
        None
    '''

    # Length
    Word.length = 5

    # Creating alphabet
    digits = [chr(i) for i in range(ord('0'), ord('9')+1)]

    # Creating primes
    primes = create()

    # Creating an empty language object
    primel = Language(alphabet=digits, length=5)

    # Adding all words
    for prime in primes:
        word = Word(str=prime, points=1)
        primel.add_word(word)

    # Doing all the information job
    primel.update_everything(True, True, True)

    # Saving language
    primel.to_csv(file_name='primel.csv')

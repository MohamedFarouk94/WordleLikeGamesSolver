from language import Language, Word
from tqdm import tqdm, tqdm_gui
import multiprocessing as mp
from copy import deepcopy
from time import sleep

digits = [chr(i) for i in range(ord('0'), ord('9')+1)]
operators = ['+', '-', '*', '/']
alphabet = digits + operators + ['=']
length = 8
n_tryouts = 6
zero = 1e-5

SHARED_SUM = mp.Value('i', 0)
SHARED_DICT = mp.Manager().dict()
mp.managers.BaseManager.register('Word', Word)
manager = mp.managers.BaseManager()
manager.start()


def one_op():
    stored_expressions = []
    global operators, zero, length

    for arg1 in tqdm(range(1000)):
        for arg2 in range(1000):
            for op in operators:

                exp_to_eval = str(arg1) + op + str(arg2)

                if len(exp_to_eval) > length - 2:
                    continue

                try:
                    res = eval(exp_to_eval)
                except:
                    continue

                if res < -zero:  # check if negative
                    continue

                if (res + zero) % 1 > 2 * zero:  # check if not integer
                    continue

                res = int(res + zero)

                exp_to_store = exp_to_eval + '=' + str(res)

                if len(exp_to_store) != length:
                    continue

                stored_expressions.append(exp_to_store)

    return stored_expressions


def two_op():
    global operators, zero, length
    stored_expressions = []

    for arg1 in tqdm(range(100)):
        for arg2 in range(100):
            for arg3 in range(100):
                for op1 in operators:
                    for op2 in operators:

                        exp_to_eval = str(arg1) + op1 + \
                                          str(arg2) + op2 + str(arg3)

                        if len(exp_to_eval) > length - 2:
                            continue

                        try:
                            res = eval(exp_to_eval)
                        except:
                            continue

                        if res < -zero:  # check if negative
                            continue

                        if (res + zero) % 1 > 2 * zero:  # check if not integer
                            continue

                        res = int(res + zero)

                        exp_to_store = exp_to_eval + '=' + str(res)

                        if len(exp_to_store) != length:
                            continue

                        stored_expressions.append(exp_to_store)

    return stored_expressions


def partiall_update(language, start, end):
    global SHARED_SUM, SHARED_DICT
    for i, word_ in enumerate(SHARED_DICT.keys()):
        if i < start:
            continue
        if i == end:
            return

        copied_word = SHARED_DICT[word_].copy()
        copied_word.calc_possible_points(language.all_words)
        SHARED_DICT[word_] = copied_word
        with SHARED_SUM.get_lock():
            SHARED_SUM.value += 1


def observe(N):
    global SHARED_SUM
    for i in tqdm(range(N)):
        while SHARED_SUM.value <= i:
            pass


def install():

    # Length
    Word.change_length(8)

    # Creating alphabet
    global alphabet

    # Creating valid expressions
    print("Preparing expressions.")
    expressions = one_op() + two_op()

    # Creating an empty Language object
    nerdle = Language(alphabet=alphabet, length=8)

    # Adding all words
    print(f'Adding {len(expressions)} words to our language...')
    for expression in tqdm(expressions):
        word = Word(str=expression, points=1)
        nerdle.add_word(word)

    # HERE WE WILL NOT CALL update_everything AS USUAL
    # BUT WE WILL DO THE JOB OURSELVES USING multiprocessing

    # First update_prob
    nerdle.update_prob()

    # Then preparing number of words to be updated per process

    # Copying words to a shared memory
    n_per_job = (len(expressions) // 4) + 1
    global SHARED_DICT
    print("Copying words to a shared memory...")
    for word_ in tqdm(nerdle.all_words):
        word = nerdle.all_words[word_]
        SHARED_DICT[word_] = manager.Word(str=word.str, points=word.points)

    # Creating 4 processes, in addition to an observer process
    p1 = mp.Process(target=partiall_update, args=(nerdle, 0, n_per_job,))
    p2 = mp.Process(target=partiall_update, args=(nerdle, n_per_job, 2*n_per_job,))
    p3 = mp.Process(target=partiall_update, args=(nerdle, 2*n_per_job, 3*n_per_job,))
    p4 = mp.Process(target=partiall_update, args=(nerdle, 3*n_per_job, len(expressions),))
    observer = mp.Process(target=observe, args=(len(expressions),))

    # Starting
    print("Let's start the multiprocessing party!!")
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    observer.start()

    # Waiting
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    observer.join()

    # Now it's time to copy back to our unshared memory
    print("Copying back to our memory scope...")
    for word_ in tqdm(SHARED_DICT.keys()):
        nerdle.all_words[word_] = SHARED_DICT[word_].copy()

    # Back to our ordinary algorithm, let's update_info and sort
    nerdle.update_info(progress_bar=True)
    nerdle.sort()

    # Saving language
    print("Saving...")
    nerdle.to_csv(file_name='nerdle.csv')

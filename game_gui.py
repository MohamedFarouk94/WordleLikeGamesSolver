import tkinter as tk
import easygui as eg


LANGUAGE = {'value': '', 'ready': False, 'accepted': False}
MODE = {'value': '', 'ready': False, 'accepted': False}
THE_WORD = {'value': '', 'ready': False, 'accepted': False, 'rejected': False}

def assign_language(lang):
    global LANGUAGE
    LANGUAGE['value'] = lang
    LANGUAGE['ready'] = True


def assign_mode(mode):
    global MODE
    MODE['value'] = mode
    MODE['ready'] = True


def first_screen():
    global LANGUAGE

    screen1 = tk.Tk()
    screen1.title('CHOOSE A GAME')
    screen1.geometry('250x200')
    screen1.eval('tk::PlaceWindow . center')
    btns = []

    wordle = tk.Button(screen1,
                       text='Wordle',
                       height=3,
                       width=30,
                       command=lambda: assign_language('engwordle'))
    wordle.pack()
    primel = tk.Button(screen1,
                       text='Primel',
                       height=3,
                       width=30,
                       command=lambda: assign_language('primel'))
    primel.pack()
    nerdle = tk.Button(screen1,
                       text='Nerdle',
                       height=3,
                       width=30,
                       command=lambda: assign_language('nerdle'))
    nerdle.pack()

    while True:
        try:
            screen1.update_idletasks()
            screen1.update()

            if LANGUAGE['accepted']:
                screen1.destroy()
                break

        except:
            exit()


def second_screen():
    global MODE

    screen2 = tk.Tk()
    screen2.title('CHOOSE A MODE')
    screen2.geometry('250x200')
    screen2.eval('tk::PlaceWindow . center')
    btns = []

    with_ = tk.Button(screen1,
                       text='Play with Computer',
                       height=3,
                       width=30,
                       command=lambda: assign_mode('with'))
    with_.pack()
    against = tk.Button(screen1,
                       text='Play against Computer',
                       height=3,
                       width=30,
                       command=lambda: assign_mode('against'))
    against.pack()
    multi = tk.Button(screen1,
                       text='Two Players',
                       height=3,
                       width=30,
                       command=lambda: assign_mode('multi'))
    multi.pack()

    while True:
        try:
            screen2.update_idletasks()
            screen2.update()

            if MODE['accepted']:
                screen2.destroy()
                break

        except:
            exit()

def input_box():
    msg = "Player to enter the target word\n(The other player will have to go away a little bit!!:)"
    while True:
        THE_WORD['value'] = eg.enterbox(msg).lower()
        THE_WORD['ready'] = True
        while not (THE_WORD['accepted'] or THE_WORD['rejected']):
            pass

        if THE_WORD['rejected']:
            msg = 'Not a valid word!\nEnter again:'
            THE_WORD['rejected'] = False

        else:
            break


def main_screen():
    global LANGUAGE

    top = tk.Tk()
    top.title(LANGUAGE['value'])
    top.eval('tk::PlaceWindow . center')

    field = tk.Canvas(top, bg='white')
    field.pack()

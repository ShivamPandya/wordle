#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import os
import random
import sys

from boxit import boxit

debug = False

def display_score(score):
    """
    Display a white-yellow-and-green grid
    representing player's guesses after a won game
    """
    colors = {'g': '🟩', 'y': '🟨', 'n': '⬜'}
    score += 'n'*(30-len(score))
    score = list(score)
    for count, value in enumerate(score):
        score[count] = colors[value]
    scorecard = ""
    for i in range(0, 30, 5):
        scorecard += '    '+''.join(score[i:i+5])+'\n'
    print(scorecard)


def print_interface(letter_grid, keyboard, game_state, correct_answer):
    """
    Based on the current game state, print all the main elements
    of the game interface, including, top to bottom:
    - instructions on how to quit the game
    - letter grid
    - keyboard
    - error message when an illegal word is entered
    - messages notifying the player of victory or loss
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("'g' to give up or 'q' to quit\n")

    for i in letter_grid:
        for j in i:
            print(f"  {j}", end="")
        print()

    print(f"\n{keyboard}")
    if debug:
        print(correct_answer)

    if game_state['invalid_word']:
        print("Guess not allowed! Please try again")
        game_state['invalid_word'] = False
    else:
        print()

    if game_state['game_over']:
        print(boxit("YOU WON!", "green", pattern='solid',
              shift=2, spacing=2))
        print(boxit(f"  Total tries: {game_state['attempt']}", "orange"))
        display_score(game_state['score'])
    elif game_state['attempt'] == 6:
        print(boxit("Sorry, you didn't make it! Better luck next time:)",
                    'red'))
        print("The word was: " + boxit(correct_answer, 'green'))
        game_state['game_over'] = True

    return game_state


def get_word():
    """
    Load a word to guess from a word list on game init
    """
    with open('wordlist.txt', encoding='utf-8') as words:
        wordlist = words.read().splitlines()
        return random.choice(wordlist).upper()


def guess_is_valid(player_guess):
    """
    Validate player's guess by checking a word list
    """
    if not player_guess:
        return False
    with open('allowed.txt', encoding='utf-8') as guess_file:
        guesslist = guess_file.read().splitlines()
    with open('wordlist.txt', encoding='utf-8') as words:
        word_list = words.read().splitlines()
    if player_guess in guesslist or player_guess in word_list:
        return True
    return False


def update_letter_display(letter_grid, keyboard, game_state, correct_answer, player_guess):
    """
    Based on player's previous guess, update the letter grid and keyboard display to be
    printed with the print_interface() function
    """
    # First pass: Deal with green and white letters
    for position, letter in enumerate(player_guess):
        if letter == correct_answer[position]:
            letter_grid[game_state['attempt']][position] = boxit(letter, 'green')
            keyboard = keyboard.replace(letter, boxit(letter, 'green'))
        else:
            letter_grid[game_state['attempt']][position] = letter
            if letter not in correct_answer:
                keyboard = keyboard.replace(letter, '■')

    # Second pass: When turning letters yellow, check against green ones
    for position, letter in enumerate(player_guess):
        if letter not in correct_answer:
            continue
        if len(letter_grid[game_state['attempt']][position]) > 1:
            continue  # letter is already green
        tmp_answer = list(correct_answer)
        for pos, char in enumerate(letter_grid[game_state['attempt']]):
            if char in [boxit(letter, 'green'), boxit(letter, 'green')]:
                tmp_answer[pos] = '_'
        if letter in tmp_answer:
            letter_grid[game_state['attempt']][position] = boxit(letter, 'yellow')
            if boxit(letter, 'green') not in keyboard:
                keyboard = keyboard.replace(letter,
                                            boxit(letter, 'yellow'))

    # Go over the last evaluated guess and set the score accordingly
    for letter in letter_grid[game_state['attempt']]:
        if letter.startswith('\x1b[32m'):
            game_state['score'] += 'g'
        elif letter.startswith('\x1b[93m'):
            game_state['score'] += 'y'
        else:
            game_state['score'] += 'n'

    return letter_grid, keyboard


if __name__ == '__main__':

    if sys.version_info[0] < 3:
        print('You are using Python 2.x! Please switch to Python 3.6 or higher.')
        sys.exit(1)

    # Command line options
    # Don't list -D in help, it's cheating:)
    program_usage_string = (
        "Usage:"  #pylint: disable=consider-using-f-string
        "\n{0} [-h]"
        "\n"
    ).format(os.path.basename(__file__))


    program_options = (
        "\n    -h, --help                  Print this help and exit"
    )

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'Dh',
                                   ['debug', 'help'])
    except getopt.GetoptError as err:
        print(err)
        print(program_usage_string)
        print(program_options)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ['-h', '--help']:
            print(program_usage_string)
            print(program_options)
            sys.exit(0)
        if opt in ['-D', '--debug']:
            debug = True



    word = get_word()
    grid = [["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0"]]

    kbd = "Q W E R T Y U I O P \nA S D F G H J K L ■\n■ Z X C V B N M ■ ■"

    state = {'attempt': 0,
             'game_over': False,
             'invalid_word': False,
             'score': ''}

    while True:
        state = print_interface(grid, kbd, state, word)
        if state['game_over']:
            break
        try:
            guess = input("Take your guess: \n ").upper()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(1)

        if guess.lower() in ['q', 'quit']:
            print("You quit the game")
            break
        if guess.lower() == 'g':
            print("You gave up! The word was: " + boxit(word, 'green'))
            break
        if not guess_is_valid(guess.lower()):
            state['invalid_word'] = True
            # Don't count this attempt
            continue

        grid, kbd = update_letter_display(grid, kbd, state, word, guess)

        if guess == word:
            state['game_over'] = True
        state['attempt'] += 1

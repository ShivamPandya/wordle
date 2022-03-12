#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import sys

from boxit.boxit import boxit


def display_score(score):
    colors = {'g': '🟩', 'y': '🟨', 'n': '⬜'}
    score += 'n'*(30-len(score))
    score = list(score)
    for count, value in enumerate(score):
        score[count] = colors[value]
    scorecard = ""
    for i in range(0, 30, 5):
        scorecard += '    '+''.join(score[i:i+5])+'\n'
    return scorecard


def print_interface(letter_grid, keyboard, game_state, correct_answer):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("'g' to give up or 'q' to quit\n")

    for i in letter_grid:
        for j in i:
            print(f"  {j}", end="")
        print()

    print(f"\n{keyboard}")

    if game_state['invalid_word']:
        print("Guess not allowed! Please try again")
        game_state['invalid_word'] = False
    else:
        print()

    if game_state['game_over']:
        print(boxit("YOU WON!", "green", pattern='solid',
              shift=2, spacing=2))
        print(boxit(f"  Total tries: {game_state['attempt']}", "orange"))
        print(display_score(game_state['score']))
    elif game_state['attempt'] == 6:
        print(boxit("Sorry, you didn't make it! Better luck next time:)",
                    'red'))
        print("The word was: " + boxit(correct_answer, 'green'))
        game_state['game_over'] = True

    return game_state


def get_word():
    with open('wordlist.txt', encoding='utf-8') as words:
        wordlist = words.read().splitlines()
        return random.choice(wordlist).upper()


def check_word(player_guess):
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
    for position, letter in enumerate(player_guess):
        if letter in correct_answer:
            if letter == correct_answer[position]:
                letter_grid[game_state['attempt']][position] = boxit(letter, 'green')
                keyboard = keyboard.replace(letter, boxit(letter, 'green'))
                game_state['score'] += "g"
            else:
                letter_grid[game_state['attempt']][position] = boxit(letter, 'yellow')
                if not boxit(letter, 'green') in keyboard:
                    keyboard = keyboard.replace(letter,
                                                boxit(letter, 'yellow'))
                game_state['score'] += "y"
        else:
            letter_grid[game_state['attempt']][position] = letter
            keyboard = keyboard.replace(letter, '■')
            game_state['score'] += 'n'
    return letter_grid, keyboard


if __name__ == '__main__':

    if sys.version_info[0] < 3:
        print('You are using Python 2.x! Please switch to Python 3.6 or higher.')
        sys.exit(1)

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
        if not check_word(guess.lower()):
            state['invalid_word'] = True
            # Don't count this attempt
            continue

        grid, kbd = update_letter_display(grid, kbd, state, word, guess)

        if guess == word:
            state['game_over'] = True
        state['attempt'] += 1

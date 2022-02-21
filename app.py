#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import sys

from boxit.boxit import boxit


def gameplay():

    if sys.version_info[0] < 3:
        return 'You are using Python 2.x! Please switch to Python 3.6 or higher.'

    word = get_word()
    count = 0
    grids = [["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"],
             ["0", "0", "0", "0", "0"]]

    score = ""

    keyboard = "Q W E R T Y U I O P \nA S D F G H J K L ■\n■ Z X C V B N M ■ ■"

    print_grid(grids)
    print()
    print(keyboard)

    guess = input("\nTake your guess: \n ").upper()

    while True:
        if guess.lower() == 'q' or guess.lower() == 'quit':
            print("You quit the game")
            break
        if guess.lower() == 'g':
            print("You gave up! The word was: " + boxit(word, 'green'))
            break
        if not check_word(guess.lower()):
            print_grid(grids)
            print()
            print(keyboard)
            print("Guess not allowed! Please try again")
            guess = input("Take your guess: \n ").upper()
            continue
        for position, letter in enumerate(guess):
            if letter in word:
                if letter == word[position]:
                    grids[count][position] = boxit(letter, 'green')
                    keyboard = keyboard.replace(letter, boxit(letter, 'green'))
                    score += "g"
                else:
                    grids[count][position] = boxit(letter, 'yellow')
                    if not boxit(letter, 'green') in keyboard:
                        keyboard = keyboard.replace(letter,
                                                    boxit(letter, 'yellow'))
                    score += "y"
            else:
                grids[count][position] = letter
                keyboard = keyboard.replace(letter, '■')
                score += 'n'
        print_grid(grids)
        print()
        print(keyboard)

        if guess == word:
            print(boxit("YOU WON!", "green", pattern='solid',
                        shift=2, spacing=2))
            print(boxit(f"  Total tries: {count+1}", "orange"))
            print(display_score(score))
            break
        count += 1
        if count == 6:
            print(boxit("Sorry, you didn't make it! Better luck next time:)",
                        'red'))
            print("The word was: " + boxit(word, 'green'))
            break
        print()
        guess = input("Take your guess: \n ").upper()


def print_grid(grids):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("'g' to give up or 'q' to quit\n")
    for i in grids:
        for j in i:
            print(f"  {j}", end="")
        print()


def get_word():
    with open('wordlist.txt', encoding='utf-8') as words:
        wordlist = words.read().splitlines()
        return random.choice(wordlist).upper()


def check_word(word):
    with open('allowed.txt', encoding='utf-8') as guess_file:
        guesslist = guess_file.read().splitlines()
    with open('wordlist.txt', encoding='utf-8') as words:
        word_list = words.read().splitlines()
    if word in guesslist or word in word_list:
        return True
    return False


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


if __name__ == '__main__':
    gameplay()

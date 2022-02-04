# -*- coding: utf-8 -*-

import os, random
from boxit.boxit import boxit

def gameplay():

    wordle = get_word()
    word = list(wordle)
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
        if not check_word(guess.lower()):
            print_grid(grids)
            print(keyboard)
            print("Guess not allowed! Please try again")
            guess = input("Take your guess: \n ").upper()
            continue
        for i in range(len(guess)):
            if guess[i] in word:
                if guess[i] == word[i]:
                    grids[count][i] = boxit(guess[i], 'green')
                    keyboard = keyboard.replace(guess[i], boxit(guess[i], 'green'))
                    score += "g"
                else:
                    grids[count][i] = boxit(guess[i], 'yellow')
                    if not boxit(guess[i], 'green') in keyboard:
                        keyboard = keyboard.replace(guess[i], boxit(guess[i], 'yellow'))
                    score += "y"
            else:
                grids[count][i] = guess[i]
                keyboard = keyboard.replace(guess[i], '■')
                score += 'n'
        print_grid(grids)
        print()
        print(keyboard)

        if guess == ''.join(word):
            print(boxit("YOU WON!", "green", pattern = 'solid', shift=2, spacing=2))
            print(boxit(f"  Total tries: {count+1}", "orange"))
            print(display_score(score))
            break
        count += 1
        if count == 6:
            print(boxit("Sorry, you didn't make it! Better luck next time:)", 'red'))
            print("The word was: "+ boxit(wordle, 'green'))
            print("\nPress enter to exit!")
            input()
            break
        print()
        guess = input("Take your guess: \n ").upper()

def print_grid(grids):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in grids:
        for j in i:
            print(f"  {j}", end="")
        print()

def get_word():
    with open('wordlist.txt', 'r+') as words:
        wordlist = words.read().splitlines()
        return random.choice(wordlist).upper()

def check_word(word):
    guess_file = open('allowed.txt', 'r+')
    guesslist = guess_file.read().splitlines()
    guess_file.close()
    words = open('wordlist.txt', 'r+')
    word_list = words.read().splitlines()
    words.close()
    if word in guesslist or word in word_list:
        return True
    return False

def display_score(score):
    colors = {'g':'🟩', 'y':'🟨', 'n':'⬜'}
    score += 'n'*(30-len(score))
    score = list(score)
    for i in range(len(score)):
        score[i] = colors[score[i]]       
    scorecard = ""
    for i in range(0,30,5):
        scorecard += '    '+''.join(score[i:i+5])+'\n'
    return scorecard

gameplay()

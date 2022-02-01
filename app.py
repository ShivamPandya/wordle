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

    clscr()
    print_grid(grids)

    guess = input("\nTake your guess: \n ").upper()

    while True:
        if guess.lower() == 'q' or guess.lower() == 'quit':
            print("You quit the game")
            break
        if not check_word(guess.lower()):
            clscr()
            print_grid(grids)
            print("Guess not allowed! Please try again")
            guess = input("Take your guess: \n ").upper()
            continue
        for i in range(len(guess)):
            if guess[i] in word:
                if guess[i] == word[i]:
                    grids[count][i] = boxit(guess[i], 'green')
                else:
                    grids[count][i] = boxit(guess[i], 'yellow')
            else:
                grids[count][i] = guess[i]
        clscr()
        print_grid(grids)

        if guess == ''.join(word):
            print(boxit("YOU WON!", "green", pattern = 'solid', shift=2, spacing=2))
            print(boxit(f"  Totatl tries: {count+1}", "orange"))
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
        clscr()

def print_grid(grids):
    for i in grids:
        for j in i:
            print(f"  {j}", end="")
        print()

def clscr():
    os.system('cls' if os.name == 'nt' else 'clear')

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

gameplay()
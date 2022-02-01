import configparser, os
from boxit.boxit import boxit

def gameplay():
    config = configparser.RawConfigParser()   
    config.read('word.conf')

    wordle = config.get('secret', 'word').upper()
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
    clscr()

    while count != 5:
        if guess.lower() == 'q' or guess.lower() == 'quit':
            print("You quit the game")
            break
        if len(guess) != 5:
            print("Word length should exactly be 5 characters, plese try again")
            guess = input("Take your guess: \n ").upper()
        for i in range(len(guess)):
            if guess[i] in word:
                if guess[i] == word[i]:
                    grids[count][i] = boxit(guess[i], 'green')
                else:
                    grids[count][i] = boxit(guess[i], 'yellow')
            else:
                grids[count][i] = guess[i]
        
        print_grid(grids)

        if guess == ''.join(word):
            print(boxit("YOU WON!", "green", pattern = 'solid', shift=2, spacing=2))
            print(boxit(f"  Totatl tries: {count+1}", "orange"))
            break
        count += 1
        if count == 6:
            print(boxit("Sorry, you didn't make it! Better luck next time:)", 'red'))
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

gameplay()
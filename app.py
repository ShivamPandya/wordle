import configparser
from boxit.boxit import boxit

config = configparser.RawConfigParser()   
config.read('word.conf')

wordle = config.get('secret', 'word').upper()
word = list(wordle)
count = 0

guess = input("Take your guess: \n ").upper()

grids = [["0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0"],
         ["0", "0", "0", "0", "0"]]

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
    
    for i in grids:
        for j in i:
            print(f"  {j}", end="")
        print()

    if guess == ''.join(word):
        print(boxit("YOU WON!", "green", pattern = 'solid', shift=2, spacing=2))
        print(boxit(f"  Totatl tries: {count+1}", "orange"))
        break
    count += 1
    if count == 5:
        print(boxit("Sorry, you didn't make it! Better luck next time:)", 'red'))
    print()
    guess = input("Take your guess: \n ").upper()

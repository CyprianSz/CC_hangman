from random import choice
from sys import exit
from time import time, sleep
from re import match
from datetime import date
from graphics import *
from os.path import isfile


def load_capitals(list_of_words):
    '''Checks if file exist before proceeding.
    Opens file with capitals and countries. Reads each line
    and appends them to new list ('list_of_words'). Before
    appending separate capital from country, what allows us
    to simply refer to choosen capital or country by entering
    2 element list, where always [0] is country and [1] is capital.'''

    if not isfile("countries_and_capitals.txt"):
        print("\nFile does not exist.")
        exit()

    file_with_capitals = open("countries_and_capitals.txt")

    for line in file_with_capitals.readlines():
        cleared_line = line[:-1]
        splited_line = cleared_line.split(" | ")
        list_of_words.append(splited_line)


def erase_spaces(working_word_splited, secret_word_splited):
    '''This is for erase spaces from our working word.'''
    index = 0
    for char in secret_word_splited:
        if char == " ":
            working_word_splited[index] = " "
        index += 1
    return "".join(working_word_splited)


def give_feedback(lives_left, not_in_word, working_word, secret_word):
    print(green + "\nYou have {} lives left.".format(lives_left))
    print("Used letters: {}".format(not_in_word) + black)
    print(bold + "\n{} - ({})".format(working_word, len(secret_word)) + black)


def append_to_high_scores(high_scores_list, end_time, guessing_count, secret_word):
    '''Takes user name. Compare actual 'end_time' with
    10 best 'end_times' and insert actual data on proper position.'''
    name = input(bold + "\nWhat's your name?\n" + black)
    index = 0
    for line in high_scores_list:
        if int(line.split(" | ")[2]) > round(end_time):
            to_write = ("{:<14} | {} | {:^5} | {:^5} | {:<20}\n".format(name, date.today(), round(end_time),
                                                                        guessing_count, secret_word))
            high_scores_list.insert(index, to_write)
            break
        index += 1


def fill_high_scores_list(high_scores_list):
    '''Fills list - one element is one line of high scores.'''
    high_scores = open("high_scores.txt", "r")
    for line in high_scores.readlines():
        high_scores_list.append(line)
    high_scores.close()


def print_high_scores(high_scores_list):
    '''Open file in write mode, which allows to
    override previous high scores with actual ones.
    Simultaneously printing a high scores list.'''
    high_scores = open("high_scores.txt", "w")
    print(bold + "\nHIGH SCORES LIST:" + black)
    print(green + '\n{:<14} {:<12} {:<7} {:<7} {:<20}\n'.format("Name:", "Date:", "Time:",
                                                                "Tries:", "Capital:") + black)
    for line in high_scores_list[:10]:
        high_scores.write(line)
        print(line.rstrip("\n"))
    high_scores.close()


def play_again():
    print(green + "\nPlay again ?")
    play_again = input("Type \"yes\" to confirm or whatever different to exit.\n" + black)
    if play_again not in ["yes", "YES", "y"]:
        exit()


def print_congratulations(secret_word, end_time, guessing_count):
    print(yellow + "\nCongratulations ! You guessed the Secret Word: {} !".format(secret_word))
    print("It took you: {} seconds and {} moves.".format(round(end_time), guessing_count) + black)
    sleep(2)


def hint_or_hang(lives_left, hint, guessing_count, decreased):
    '''In case of 'lives_left' take proper action'''
    print(red + "\nLives left decreased by {} !".format(decreased) + black)
    if lives_left == 1:
        print(bold + "\nHint: The capital of {}.".format(hint) + black)
    elif lives_left <= 0:
        print(bold + "\nYOU HANGED !\n" + black)
        print(hanged)
        sleep(2)


def update_working_word(working_word, secret_word_splited, user_input):
    '''Update 'working_word' with currently guessed letter'''
    index = 0
    working_word_splited = list(working_word)
    for char in secret_word_splited:
        if char == user_input:
            working_word_splited[index] = user_input
        index += 1
    working_word = "".join(working_word_splited)
    return working_word


def main():
    '''Creates while loop, needed for playing again without exiting
    script, if user choose so.

    Chooses random pair 'country - capital' and assign
    'secret word' and 'hint' for better readability in further code.
    Using upper to remove casesensitivity.
    Variable 'secret_word_splited' is needed for comparing when single letter given.

    Creating 'working_word' based on 'secret_word', needed for
    displaying letters guessed so far and their proper positions.

    Set variables needed to display to user how many moves he did
    and how much time it took him ('start_time', 'guessing_count').

    If user type a single letter, script iterate through
    'secret_word' and compare each element with given letter. If given
    letter is equal to a letter in 'secret_word' it assigns in to the proper
    position in 'working_word'. To achieve that spliting 'working_word' before
    iteration and joining after is needed.

    If user type whole word at once, script checks if he
    guessed. After this he decide to play again or exit script.
    If he gave wrong answer his 'lives_left' decreases by 2 and if he
    has no 'lives_left' - he loses. Script gives extra hint if 'lives_left' is 1.'''

    print(intro)
    list_of_words = []
    load_capitals(list_of_words)

    while True:
        lives_left = 5
        not_in_word = []
        lot = choice(list_of_words)
        secret_word = lot[1].upper()
        secret_word_splited = list(secret_word)
        hint = lot[0]
        working_word = len(secret_word) * "_"
        start_time = time()
        guessing_count = 1
        working_word_splited = list(working_word)
        working_word = erase_spaces(working_word_splited, secret_word_splited)
        win = False

        # This print is for presentation purpose only. Not to guess every time,
        # just show how script works. Should be erased if wont to play for real.
        print(secret_word)

        while not win and lives_left > 0:
            give_feedback(lives_left, not_in_word, working_word, secret_word)
            user_input = input("\nType whole word or a single letter: \n").upper()

            if match("^[A-Z]$", user_input):
                guessing_count += 1
                working_word = update_working_word(working_word, secret_word_splited, user_input)
                if working_word == secret_word:
                    win = True
                elif user_input not in secret_word_splited:
                    not_in_word.append(user_input)
                    lives_left -= 1
                    hint_or_hang(lives_left, hint, guessing_count, 1)
            else:
                if user_input == secret_word:
                    win = True
                else:
                    guessing_count += 1
                    lives_left -= 2
                    hint_or_hang(lives_left, hint, guessing_count, 2)

            if win:
                end_time = time() - start_time
                high_scores_list = []
                print_congratulations(secret_word, end_time, guessing_count)
                fill_high_scores_list(high_scores_list)
                append_to_high_scores(high_scores_list, end_time, guessing_count, secret_word)
                print_high_scores(high_scores_list)

        play_again()


if __name__ == '__main__':
    main()

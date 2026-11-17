import json
import os
import sys
import random
import time

def resource_path(relative_path):
    """Return the path to a bundled resource."""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def load_dict_from_json(file_name):
    file_path = resource_path(file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise TypeError("The JSON file does not contain a dictionary.")

    return data

country_dict = load_dict_from_json("gmcdict_v1.0.json")
list_of_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def clear_screen():
    print("\033[2J\033[H", end="")

def header():
    print("Guess My Country!\n")


bot_country = random.choice(list(country_dict))
player_country = input("Enter your country below:\n> ").upper()

def create_skeleton(country):
    skeleton = []
    for letter in country:
        if letter == " ":
            skeleton.append(" ")
        elif letter != " ":
            skeleton.append("-")
    return skeleton

bot_skeleton = create_skeleton(bot_country)
player_skeleton = create_skeleton(player_country)

turn = 1

def bot_engine(skeleton, list_of_letters): # Bot guessing is incomplete for now, actual guessing will be adapted from my solver later on
    guess = random.choice(list_of_letters)
    return guess

def bot_turn(guess, player_skeleton, player_country):
    original_skeleton = player_skeleton.copy()
    clear_screen()
    header()
    if len(guess) == 1:
        print(f"Guessing {guess}...")
        time.sleep(2.5)
        if guess in list(player_country):
            for letter in player_skeleton:
                for index in range(len(list(player_country))):
                    if player_country[index] == guess and player_skeleton[index] == "-":
                        player_skeleton[index] = guess
            if guess not in original_skeleton:
                print(f"{guess} is in the country!")
                time.sleep(2.5)
                clear_screen()
                header()
                for letter in player_skeleton:
                    print(letter, end=" ")
                time.sleep(2.5)
            elif guess in original_skeleton:
                input(f"'{guess}' has already been guessed.")
                time.sleep(2.5)
        elif guess not in list(player_country):
            print(f"{guess} is not in the country!")
            time.sleep(2.5)
    elif len(guess) > 3:
        if list(guess) == list(bot_country):
            player_skeleton = list(player_country)
    return player_skeleton

def player_turn(skeleton, bot_country):
    original_skeleton = skeleton.copy()
    clear_screen()
    header()
    for letter in skeleton:
        print(letter, end=" ")
    guess = input("Guess a letter:\n> ").capitalize()
    if len(guess) == 1:
        if guess in list(bot_country):
            for letter in skeleton:
                for index in range(len(list(bot_country))):
                    if bot_country[index] == guess and skeleton[index] == "-":
                        skeleton[index] = guess
            if guess not in original_skeleton:
                input(f"{guess.capitalize()} is in the country!")
                clear_screen()
                header()
                for letter in skeleton:
                    print(letter, end=" ")
                input("\nPress enter: ")
            elif guess in original_skeleton:
                input(f"'{guess.capitalize()}' has already been guessed.")
        elif guess not in list(bot_country):
            input(f"{guess} is not in the country!")
    elif len(guess) > 3:
        if list(guess.upper()) == list(bot_country):
            skeleton = list(bot_country)
    return skeleton


# GAME
while True:
    bot_skeleton = player_turn(bot_skeleton, bot_country)

    turn += 1
    if bot_skeleton == list(bot_country):
        clear_screen()
        header()
        print(f"{bot_country}\nYou have won the game!")
        print(f"\n\nBot Progress: {player_skeleton} ({player_country})")
        break
    if player_skeleton == list(player_country):
        clear_screen()
        header()
        print(f"{player_country}\nThe bot has won the game.")
        print(f"\n\nYour Progress: {bot_skeleton} ({bot_country})")
        break

    bot_guess = bot_engine(player_skeleton, list_of_letters)
    player_skeleton = bot_turn(bot_guess, player_skeleton, player_country)

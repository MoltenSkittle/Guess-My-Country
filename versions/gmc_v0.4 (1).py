import copy
import json
import math
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
list_of_letters = {
            "A": {},
            "B": {},
            "C": {},
            "D": {},
            "E": {},
            "F": {},
            "G": {},
            "H": {},
            "I": {},
            "J": {},
            "K": {},
            "L": {},
            "M": {},
            "N": {},
            "O": {},
            "P": {},
            "Q": {},
            "R": {},
            "S": {},
            "T": {},
            "U": {},
            "V": {},
            "W": {},
            "X": {},
            "Y": {},
            "Z": {}
            }

def clear_screen():
    print("\033[2J\033[H", end="")

def header():
    print("Guess My Country!\n")

while True:
    clear_screen()
    header()
    setting = input("Choose a difficulty:\n1. Easiest\n2. Easy-Mid\n3. Medium\n4. Hard\n5. Next to Impossible\n> ")
    if setting in ("1", "2", "3", "4", "5"):
        break
    else:
        continue

if setting == "5":
    strong_country_dict = copy.deepcopy(country_dict)
    remove_items = {"ANTIGUA AND BARBUDA",
                    "BOSNIA AND HERZEGOVINA,"
                    "CABO VERDE",
                    "CENTRAL AFRICAN REPUBLIC",
                    "COSTA RICA",
                    "COTE DIVOIRE",
                    "DEMOCRATIC REPUBLIC OF THE CONGO",
                    "DOMINICAN REPUBLIC",
                    "EL SALVADOR",
                    "EQUATORIAL GUINEA",
                    "LIECHTENSTEIN",
                    "MARSHALL ISLANDS",
                    "NEW ZEALAND",
                    "NORTH MACEDONIA",
                    "PAPUA NEW GUINEA",
                    "REPUBLIC OF THE CONGO",
                    "SAINT KITTS AND NEVIS",
                    "SAINT VINCENT AND THE GRENADINES",
                    "SAN MARINO",
                    "SAO TOME AND PRINCIPE",
                    "SIERRA LEONE",
                    "SOLOMON ISLANDS",
                    "SRI LANKA",
                    "TRINIDAD AND TOBAGO",
                    "TURKMENISTAN",
                    "UNITED ARAB EMIRATES",
                    "UNITED KINGDOM"
}
    filtered_data = {k: v for k, v in strong_country_dict.items() if k not in remove_items}
    bot_country = random.choice(list(filtered_data))
else:
    bot_country = random.choice(list(country_dict))
while True:
    clear_screen()
    header()
    player_country = input("Enter your country below:\n> ").upper()
    if player_country.upper() in country_dict:
        break
    else:
        clear_screen()
        header()
        print("Your country doesn't exist. Perhaps it was misspelt?")

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
filter_info = []
player_guessed_letters = []


turn = 1





# NOTE BOT ENGINE

def bot_engine_A(skeleton, list_of_letters, country_dict, filter_info):
    while True:
        guess = random.choice(list_of_letters)
        if guess in filter_info:
            continue
        elif guess not in filter_info:
            break
    return guess, filter_info

def bot_engine_B(skeleton, list_of_letters, country_dict, filter_info, deviator_ceiling):
    given_letters = []
    possible_countries = {}
    for item in skeleton:
        if item != "-":
            given_letters.append(item)
    for country in country_dict:
        variable = ""
        for character in list(country):
            if character != " ":
                variable += "-"
            elif character == " ":
                variable += " "
        new_skeleton = list(variable)
        for given_letter in given_letters:
            for country_letter in list(country):
                for index in range(len(country)):
                    if country[index] == given_letter and new_skeleton[index] == "-":
                        new_skeleton[index] = given_letter
        if new_skeleton == skeleton:
            cont = country_dict[country]["CONTINENT"]
            landlocked = country_dict[country]["LANDLOCKED"]
            has_a_coastline = country_dict[country]["HAS A COASTLINE"]
            island = country_dict[country]["ISLAND"]

            possible_countries[country] = {}

            possible_countries[country] = {
            "CONTINENT": cont,
            "LANDLOCKED": landlocked,
            "HAS A COASTLINE": has_a_coastline,
            "ISLAND": island
            }

    if len(filter_info) >= 1:
        if len(skeleton) == 0:
            possible_countries = country_dict.copy()
            for country in list(possible_countries):
                for letter in list(filter_info):
                    if letter in country: 
                        if country in possible_countries:
                            del possible_countries[country]
        elif len(skeleton) >= 1:
            for country in list(possible_countries):
                for letter in list(filter_info):
                    if letter in country and country in possible_countries:
                        del possible_countries[country]

    if len(possible_countries) != 0:
        if len(possible_countries) == 1:
            if deviator_ceiling == 7000:
                guess_correctly = random.randint(1, 5)
                if guess_correctly == 1:
                    guess = next(iter(possible_countries))
                else:                       
                    guessing_letters = list(list_of_letters.copy())
                    for letter in list(guessing_letters):
                        if letter in filter_info:
                            del guessing_letters[letter]
                    guess = random.choice(guessing_letters)
            elif deviator_ceiling == 70:
                guess_correctly = random.randint(1, 3)
                if guess_correctly == 1:
                    guess = next(iter(possible_countries))
                else:                       
                    guessing_letters = list(list_of_letters.copy())
                    for letter in list(guessing_letters):
                        if letter in filter_info:
                            del guessing_letters[letter]
                    guess = random.choice(guessing_letters)
            else:
                guess = next(iter(possible_countries))
        else:
            letters = list_of_letters.copy()
            for letter in list(letters):
                if letter in filter_info:
                    del letters[letter]
            best_letter = None
            best_entropy = -1
            for letter in letters:
                probabilities = []
                entropy = 0
                letters[letter]["NO INFO"] = 0
                for country in possible_countries:
                    new2_skeleton = skeleton.copy()
                    for bit in country:
                        if bit != " ":
                            new2_skeleton.append("-")
                        elif bit == " ":
                            new2_skeleton.append(" ")
                    for index in range(len(country)):
                        if country[index] == letter and new2_skeleton[index] == "-":
                            new2_skeleton[index] = letter
                    no_info = True
                    for character in new2_skeleton:
                        if character != "-" and character != " ":
                            no_info = False
                    if no_info == True:
                        letters[letter]["NO INFO"] += 1
                    elif tuple(new2_skeleton) in letters[letter]:
                        letters[letter][tuple(new2_skeleton)] += 1
                    elif tuple(new2_skeleton) not in letters[letter]:
                        letters[letter][tuple(new2_skeleton)] = 1
                for pattern, quantity in letters[letter].items():
                    probabilities.append(quantity/len(possible_countries))
                deviator = random.randint(1, deviator_ceiling)
                entropy = -sum(deviator * p * math.log2(p) for p in probabilities if p > 0)
                if entropy > best_entropy:
                    best_entropy = entropy
                    best_letter = letter
                elif entropy == best_entropy:
                    best_letter += letter
            if best_letter is not None:
                if deviator_ceiling == 7000:
                    guess_correctly = random.randint(1, 5)
                    if guess_correctly == 1:
                        guess = random.choice(best_letter)
                    else:
                        guessing_letters = list(list_of_letters.copy())
                        for letter in list(guessing_letters):
                            if letter in filter_info:
                               guessing_letters.remove(letter)
                        guess = random.choice(guessing_letters)

                elif deviator_ceiling == 70:
                    guess_correctly = random.randint(1, 3)
                    if guess_correctly == 1:
                        guess = random.choice(best_letter)
                    else:
                        guessing_letters = list(list_of_letters.copy())
                        for letter in list(guessing_letters):
                            if letter in filter_info:
                                del guessing_letters[letter]
                        guess = random.choice(guessing_letters)
                else:
                    guess = random.choice(best_letter)
            elif best_letter is None:
                print('bug')
    return guess, filter_info

def bot_engine_selector(setting, filter_info):
    if setting == "1":
        bot_guess, filter_info = bot_engine_A(player_skeleton, list_of_letters, country_dict, filter_info)
    elif setting == "2":
        bot_guess, filter_info = bot_engine_B(player_skeleton, list_of_letters, country_dict, filter_info, 7000)
    elif setting == "3":
        bot_guess, filter_info = bot_engine_B(player_skeleton, list_of_letters, country_dict, filter_info, 70)
    elif setting == "4":
        bot_guess, filter_info = bot_engine_B(player_skeleton, list_of_letters, country_dict, filter_info, 20)
    elif setting == "5":
        bot_guess, filter_info = bot_engine_B(player_skeleton, list_of_letters, country_dict, filter_info, 1)
    return bot_guess, filter_info

# NOTE BOT & PLAYER TURNS

def bot_turn(guess, player_skeleton, player_country, filter_info):
    incorrect_cguess = False
    original_skeleton = player_skeleton.copy()
    clear_screen()
    header()
    print("BOT TURN")
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
            filter_info.append(guess)
            for letter in player_skeleton:
                print(letter, end=" ")
            time.sleep(2.5)
    elif len(guess) > 3:
        if list(guess) == list(player_country):
            player_skeleton = list(player_country)
        elif list(guess) != list(player_country):
            incorrect_cguess = True
    return player_skeleton, incorrect_cguess, filter_info

def player_turn(skeleton, bot_country, player_guessed_letters):
    incorrect_cguess = False
    clear_screen()
    header()
    for letter in skeleton:
        print(letter, end=" ")
    guess = input("Guess a letter:\n> ").capitalize()
    if len(guess) == 1:
        if guess in player_guessed_letters:
            input(f"'{guess.capitalize()}' has already been guessed.")
        elif guess not in player_guessed_letters:
            player_guessed_letters.append(guess)
            if guess in list(bot_country):
                for letter in skeleton:
                    for index in range(len(list(bot_country))):
                        if bot_country[index] == guess and skeleton[index] == "-":
                            skeleton[index] = guess
                input(f"{guess.capitalize()} is in the country!")
                clear_screen()
                header()
                for letter in skeleton:
                    print(letter, end=" ")
                input("\nPress enter: ")
            elif guess not in list(bot_country):
                input(f"{guess} is not in the country!")

    elif len(guess) > 3:
        if list(guess.upper()) == list(bot_country):
            skeleton = list(bot_country)
        elif list(guess.upper()) != list(bot_country):
            incorrect_cguess = True

    return skeleton, incorrect_cguess, player_guessed_letters


# NOTE GAME LOOP

while True:
    bot_skeleton, p_incorrect_cguess, player_guessed_letters = player_turn(bot_skeleton, bot_country, player_guessed_letters)

    turn += 1
    if bot_skeleton == list(bot_country):
        clear_screen()
        header()
        print(f"{bot_country}\nYou have won the game!")
        print("\n\nBot Progress:", end=" ")
        for character in player_skeleton:
            print(character, end=" ")
        print(f" ({player_country})")
        break
    if player_skeleton == list(player_country):
        clear_screen()
        header()
        print(f"{player_country}\nThe bot has won the game.")
        print(f"\n\nYour Progress: {bot_skeleton} ({bot_country})")
        break
    if p_incorrect_cguess == True:
        clear_screen()
        header()
        print(f"You guessed incorrectly! The bot has won the game.\nTheir actual country was {bot_country}.")
        break

    bot_guess, filter_info = bot_engine_selector(setting, filter_info)
    player_skeleton, b_incorrect_cguess, filter_info = bot_turn(bot_guess, player_skeleton, player_country, filter_info)

    if bot_skeleton == list(bot_country):
        clear_screen()
        header()
        print(f"{bot_country}\nYou have won the game!")
        print("\n\nBot Progress:", end=" ")
        for character in player_skeleton:
            print(character, end=" ")
        print(f" ({player_country})")
        break
    if player_skeleton == list(player_country):
        clear_screen()
        header()
        print(f"{player_country}\nThe bot has won the game.")
        print(f"\n\nYour Progress: {bot_skeleton} ({bot_country})")
        break
    if p_incorrect_cguess == True:
        clear_screen()
        header()
        print(f"The bot guessed incorrectly! You have won the game.\nThe bot's country was {bot_country}.")
        break

import copy
import json
import math
import os
import sys
import random
import tkinter as tk

"""
Planned additions:
- pre-game setting selection
    - Tutorial
        - This will need more conceptual thinking, because I don't have any discrete idea yet other than a popup-window.
    - List of available countries
    - Better UI quality
    
    - I might have to consider using classes soon.

I think that the foundation of my code is complete.


"""

root = tk.Tk()
active_game = False

def open_fullscreen_window(root, title):
  root.title(title)
  root.configure(bg="#bedbe4")
  root.geometry("1500x1000")

  # Optional: Escape key to exit fullscreen
  root.bind("<Escape>", lambda e: root.destroy())

def disable_game(entry, button):
    entry.config(state="disabled")
    entry.config(disabledbackground="#929292")
    button.config(state="disabled")
    button.config(bg="#4D4D4D")

def enable_game(entry, button):
    entry.config(state="normal")
    entry.config(bg="#8ea3ff")
    button.config(state="normal")
    button.config(bg="#8ea3ff")

def resource_path(relative_path):
    """Return the path to a file beside the EXE, or beside the Python script."""
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
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


def create_skeleton(country):
    skeleton = []
    string = ""
    for letter in country:
        if letter == " ":
            skeleton.append(" ")
        elif letter != " ":
            skeleton.append("-")
    for character in skeleton:
        string += character + " "
    return skeleton, string

country_dict = load_dict_from_json("gmcdict_v1.0.json")
list_of_letters = { "A": {}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}, "G": {}, "H": {}, "I": {}, "J": {}, "K": {}, "L": {}, "M": {}, 
                   "N": {}, "O": {}, "P": {}, "Q": {}, "R": {}, "S": {}, "T": {}, "U": {}, "V": {}, "W": {}, "X": {}, "Y": {}, "Z": {} }

settings = {
    "1": False,
    "2": False,
    "3": False,
    "4": False,
    "5": False
}

def setting_selection(setting):
    global settings
    settings[setting] = not settings[setting]
    for pos_setting in settings:
        if pos_setting != setting:
            settings[pos_setting] = False
            # for making all unselected setting grey

    if settings["1"] == True:
        button_1.config(bg="#009E0D")
    else:
        button_1.config(bg="#252525")
    if settings["2"] == True:
        button_2.config(bg="#009E0D")
    else:
        button_2.config(bg="#252525")
    if settings["3"] == True:
        button_3.config(bg="#009E0D")
    else:
        button_3.config(bg="#252525")
    if settings["4"] == True:
        button_4.config(bg="#009E0D")
    else:
        button_4.config(bg="#252525")
    if settings["5"] == True:
        button_5.config(bg="#009E0D")
    else:
        button_5.config(bg="#252525")



filter_info = []
player_guess = []

top_title = tk.Label(root, bg="#bedbe4",  text="Guess My Country", fg="navy", font=("calibre", 45, "bold"), width=25, height=2)

play_button = tk.Button(root, text="Play", activebackground="white", activeforeground="black", anchor="center", bd=3, bg="#C8F9FF",  
                        cursor="hand2", fg="navy", font=("Arial", 45, "bold"), height=1, highlightbackground="black", highlightcolor="green", highlightthickness=2,
                        justify="center", overrelief="ridge", width=10)

choose_country_label = tk.Label(root, bg="#bedbe4", text="Choose Your Country", fg="#1100FF", font=("calibre",35 , "bold"), width=25, height=2)

choose_country_entry = tk.Entry(root, bg="#8ea3ff", font=('arial',25, 'normal'), fg="black", width=30, bd=2, relief="sunken")

unexisting_country = tk.Label(root, bg="#bedbe4", text="Your country isn't part of the list of recognized countries.", 
                              fg="#bedbe4", font=("calibre",13 , "bold"), width=50, height=1)

country_not_given = tk.Label(root, bg="#bedbe4", text="Please enter a country.", fg="#bedbe4", font=("calibre",13 , "bold"), width=50, height=1)

diff_unselected = tk.Label(root, bg="#bedbe4", text="Please select a difficulty.", fg="#bedbe4", font=("calibre",13 , "bold"), width=50, height=1)
                                    
buttons_label = tk.Label(root, bg="#bedbe4", text="Select Difficulty:\n1 = Easiest, 5 = Near-Impossible", fg="#1100FF", font=("calibre",25 , "bold"), width=25, height=2)

button_1 = tk.Button(root, text="Easiest", activebackground="white", activeforeground="black", anchor="center", bd=3, bg="#252525",
                      command=lambda: setting_selection("1"), cursor="hand2", fg="white", font=("Arial", 15, "bold"), highlightbackground="black", 
                      highlightcolor="green", highlightthickness=2, justify="center",  overrelief="ridge")
button_2 = tk.Button(root, text="Easy", activebackground="white", activeforeground="black", anchor="center", bd=3, bg="#252525",
                      command=lambda: setting_selection("2"), cursor="hand2", fg="white", font=("Arial", 15, "bold"), highlightbackground="black", 
                      highlightcolor="green", highlightthickness=2, justify="center",  overrelief="ridge")
button_3 = tk.Button(root, text="Medium", activebackground="white", activeforeground="black", anchor="center", bd=3, bg="#252525",
                      command=lambda: setting_selection("3"), cursor="hand2", fg="white", font=("Arial", 15, "bold"), highlightbackground="black", 
                      highlightcolor="green", highlightthickness=2, justify="center",  overrelief="ridge")
button_4 = tk.Button(root, text="Hard", activebackground="white", activeforeground="black", anchor="center", bd=3, bg="#252525",
                      command=lambda: setting_selection("4"), cursor="hand2", fg="white", font=("Arial", 15, "bold"), highlightbackground="black", 
                      highlightcolor="green", highlightthickness=2, justify="center",  overrelief="ridge")
button_5 = tk.Button(root, text="Near-Impossible", activebackground="white", activeforeground="black", anchor="center", bd=3, bg="#252525",
                      command=lambda: setting_selection("5"), cursor="hand2", fg="white", font=("Arial", 15, "bold"), highlightbackground="black", 
                      highlightcolor="green", highlightthickness=2, justify="center",  overrelief="ridge")

top_title.place(relx=0.5, rely=0.1, anchor="center") # x= 1500, y = 1000
choose_country_label.place(relx=0.5, rely=0.25, anchor="center")
choose_country_entry.place(relx=0.5, rely=0.3, anchor="center")
unexisting_country.place(relx=0.5, rely=0.35, anchor="center")
country_not_given.place(relx=0.5, rely=0.35, anchor="center")
diff_unselected.place(relx=0.5, rely=0.38, anchor="center")
buttons_label.place(relx=0.5, rely=0.47, anchor="center")
button_1.place(relx=0.36, rely=0.55, anchor="center")
button_2.place(relx=0.43, rely=0.55, anchor="center")
button_3.place(relx=0.5, rely=0.55, anchor="center")
button_4.place(relx=0.57, rely=0.55, anchor="center")
button_5.place(relx=0.67, rely=0.55, anchor="center")
play_button.place(relx=0.5, rely=0.75, anchor="center")

# page 2
pside_header = tk.Label(root, bg="#bedbe4", text="BOT's Country:", fg="navy", font=("calibre", 25, "bold"), width=30, height=2)
bside_header = tk.Label(root, bg="#bedbe4", text="Your Country:", fg="navy", font=("calibre", 25, "bold"), width=30, height=2)

pside_skeleton = tk.Label(root, bg="#bedbe4", fg="navy", font=("calibre", 25, "bold"), width=40, height=2)
bside_skeleton = tk.Label(root, bg="#bedbe4", fg="navy", font=("calibre", 25, "bold"), width=40, height=2)

guess_entry = tk.Entry(root, bg="#8ea3ff", font=('arial',20, 'normal'), fg="black", width=20, bd=2, relief="sunken")
guess_button = tk.Button(root, text="Guess", activebackground="white", activeforeground="black", anchor="center", bd=3, bg="#8ea3ff",
                        cursor="hand2", fg="white", font=("Arial", 20, "bold"), height=2, highlightbackground="black", highlightcolor="green", 
                        highlightthickness=2, justify="center", overrelief="ridge", width=10)


player_turn_label = tk.Label(root, bg="#bedbe4", text="Player Turn", fg="#000000", font=("calibre", 30, "bold"), width=30, height=2)
bot_turn_label = tk.Label(root, bg="#bedbe4", text="Bot Turn", fg="#000000", font=("calibre", 30, "bold"), width=30,  height=2)

player_win = tk.Label(root, bg="#bedbe4", font=('arial', 30, 'bold'), fg="#bedbe4", width=25, bd=10, text="You Win!")
bot_win = tk.Label(root, bg="#bedbe4", font=('arial', 30, 'bold'), fg="#bedbe4", width=25, bd=10, text="Bot Wins!")

p_guessing_label = tk.Label(root, bg="#bedbe4", font=('arial', 20, 'normal'), fg="#bedbe4", width=25, bd=10, text=".")
b_guessing_label = tk.Label(root, bg="#bedbe4", font=('arial', 20, 'normal'), fg="#bedbe4", width=25, bd=10, text=".")

player_country_label = tk.Label(root, bg="#bedbe4", font=('arial', 15, 'normal'), fg="#000000", width=20, bd=10)
bot_country_label = tk.Label(root, bg="#bedbe4", font=('arial', 15, 'normal'), fg="#bedbe4", width=20, bd=10)

def game_loop():
    global game_running, bot_skeleton, bot_country, player_guessed_letters, player_guess, player_skeleton, p_incorrect_cguess, filter_info, turn
    if len(player_guess) == 1:
        bot_skeleton, p_incorrect_cguess, player_guessed_letters, bot_string = player_turn(bot_skeleton, bot_country, player_guessed_letters, player_guess[0])
        player_guess.clear()
        turn += 1
        if bot_skeleton == list(bot_country):
            player_win.lift()
            player_win.config(fg="#137200")
            disable_game(guess_entry, guess_button)

        elif p_incorrect_cguess == True:
            str_skeleton = ""
            for letter in player_country:
                str_skeleton += letter + " "
            bside_skeleton.config(text=str_skeleton)
            bot_win.config(fg="#B40000")
            bot_win.lift()
            disable_game(guess_entry, guess_button)
            bot_country_label.config(fg="#000000")

        else: 
            bot_turn_label.lift()
            bot_guess, filter_info = bot_engine_selector(setting, filter_info)
            player_skeleton, b_incorrect_cguess, filter_info, player_string = bot_turn(bot_guess, player_skeleton, player_country, filter_info)

            if player_skeleton == list(player_country):
                bot_win.config(fg="#B40000")
                bot_win.lift()
                disable_game(guess_entry, guess_button)
                
            elif p_incorrect_cguess == True:
                str_skeleton = ""
                for letter in bot_country:
                    str_skeleton += letter + " "
                pside_skeleton.config(text=str_skeleton)
                player_win.config(fg="#137200")
                player_win.lift()
                disable_game(guess_entry, guess_button)
            else:
                player_turn_label.lift()
                enable_game(guess_entry, guess_button)

    if game_running:
        root.update()
        root.after(100, game_loop)

def attempt_play_game():
    global country_dict, settings
    active_game = False
    global player_country
    setting_active = False

    for key in settings:
        if settings[key] == True:
            setting_active = True
            diff_unselected.config(fg="#bedbe4")
    if setting_active == False:
        diff_unselected.config(fg="red")

    player_country = chosen_country_var.get().upper()
    if len(player_country) == 0:
        country_not_given.config(fg="red")
        unexisting_country.config(fg="#bedbe4")
        country_not_given.lift()
    elif player_country not in list(country_dict):
        country_not_given.config(fg="#bedbe4")
        unexisting_country.config(fg="red")
        unexisting_country.lift()
    elif player_country in list(country_dict):
        country_not_given.config(fg="#bedbe4")
        unexisting_country.config(fg="#bedbe4")
        for key in settings:
            if settings[key] == True:
                active_game = True
                global setting
                setting = key
        if active_game == True:
            for widget in root.winfo_children():
                widget.place_forget()
            
            global bot_country
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

            global bot_skeleton, bot_string, player_skeleton, player_string
            bot_skeleton, bot_string = create_skeleton(bot_country)
            player_skeleton, player_string = create_skeleton(player_country)
            pside_skeleton.config(text=bot_string)
            bside_skeleton.config(text=player_string)
            guess_entry.config(textvariable=input_info_var)
            guess_button.config(command=submit)
            player_country_label.config(text=f"({player_country})")
            bot_country_label.config(text=f"({bot_country})")



            top_title.place(relx=0.5, rely=0.1, anchor="center") # x= 1500, y = 1000
            pside_header.place(relx=0.2, rely=0.33, anchor="center")
            bside_header.place(relx=0.8, rely=0.33, anchor="center")
            pside_skeleton.place(relx=0.2, rely=0.4, anchor="center")
            bside_skeleton.place(relx=0.8, rely=0.4, anchor="center")
            guess_entry.place(relx=0.2, rely=0.50, anchor="center")
            guess_button.place(relx=0.2, rely=0.60, anchor="center")

            player_turn_label.place(relx=0.5, rely=0.25, anchor="center")
            bot_turn_label.place(relx=0.5, rely=0.25, anchor="center")

            player_win.place(relx=0.5, rely=0.25, anchor="center")
            bot_win.place(relx=0.5, rely=0.25, anchor="center")

            p_guessing_label.place(relx=0.2, rely=0.7, anchor="center")
            b_guessing_label.place(relx=0.8, rely=0.7, anchor="center")

            player_country_label.place(relx=0.8, rely=0.45, anchor="center")
            bot_country_label.place(relx=0.2, rely=0.45, anchor="center")
            player_turn_label.lift()
            game_loop()

play_button.config(command=attempt_play_game)



def submit():
    global player_guess
    input_info = input_info_var.get()
    player_guess.append(input_info.upper())
    input_info_var.set("")
    # In a way, this sends the player guess over.


player_guessed_letters = []
input_info_var = tk.StringVar()
chosen_country_var = tk.StringVar()
choose_country_entry.config(textvariable=chosen_country_var)
open_fullscreen_window(root, "Guess My Country")




# NOTE BOT ENGINE

def bot_engine_A(skeleton, list_of_letters, country_dict, filter_info):
    while True:
        guess = random.choice(list(list_of_letters))
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
                            guessing_letters.remove(letter)
                    guess = random.choice(guessing_letters)
            else:
                guess = next(iter(possible_countries))

        else:
            letters = list_of_letters.copy()
            for letter in list(letters.copy()):
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
                        for letter in list(guessing_letters.copy()):
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
                                guessing_letters.remove(letter)
                        guess = random.choice(guessing_letters)
                else:
                    guess = random.choice(best_letter)

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
    b_guessing_label.config(text=f"Guessing {guess}...")
    b_guessing_label.config(fg="#000000")
    b_guessing_label.lift()
    root.update()
    root.after(2500)
    b_guessing_label.config(fg="#bedbe4")
    if len(guess) == 1:
        if guess in list(player_country):
            for letter in player_skeleton:
                for index in range(len(list(player_country))):
                    if player_country[index] == guess and player_skeleton[index] == "-":
                        player_skeleton[index] = guess
            if guess not in original_skeleton:
                b_guessing_label.lift()
                b_guessing_label.config(text=f"{guess} is in the country!")
                b_guessing_label.config(fg="black")
                str_skeleton = ""
                for letter in player_skeleton:
                    str_skeleton += letter + " "
                bside_skeleton.config(text=str_skeleton)
                root.update()
                root.after(2500)
                b_guessing_label.config(fg="#bedbe4")
            elif guess in original_skeleton:
                b_guessing_label.lift()
                b_guessing_label.config(text=f"{guess} has already been guessed.")
                b_guessing_label.config(fg="black")
                root.update()
                root.after(2500)
                b_guessing_label.config(fg="#bedbe4")
        elif guess not in list(player_country):
            b_guessing_label.lift()
            b_guessing_label.config(text=f"{guess} is not in the country!")
            b_guessing_label.config(fg="black")
            root.update()
            root.after(2500)
            b_guessing_label.config(fg="#bedbe4")
            filter_info.append(guess)
            root.update()
    elif len(guess) > 3:
        if list(guess) == list(player_country):
            player_skeleton = list(player_country)
            str_skeleton = ""
            for letter in player_country:
                str_skeleton += letter + " "
            bside_skeleton.config(text=str_skeleton)
        elif list(guess) != list(player_country):
            incorrect_cguess = True
    player_string = ""
    for character in player_skeleton:
        player_string += character + " "
    return player_skeleton, incorrect_cguess, filter_info, player_string

def player_turn(skeleton, bot_country, player_guessed_letters, guess):
    disable_game(guess_entry, guess_button)
    incorrect_cguess = False
    if len(guess) == 1:
        if guess in player_guessed_letters:
            p_guessing_label.lift()
            p_guessing_label.config(text=f"{guess} has already been guessed!")
            p_guessing_label.config(fg="#000000")
            root.update()
            root.after(2500)
            p_guessing_label.config(fg="#bedbe4")
        elif guess not in player_guessed_letters:
            player_guessed_letters.append(guess)
            if guess in list(bot_country):
                for letter in skeleton:
                    for index in range(len(list(bot_country))):
                        if bot_country[index] == guess and skeleton[index] == "-":
                            skeleton[index] = guess
                p_guessing_label.lift()
                p_guessing_label.config(text=f"{guess} is in the country!")
                p_guessing_label.config(fg="#000000")
                root.update()
                root.after(2500)
                p_guessing_label.config(fg="#bedbe4")
                str_skeleton = ""
                for letter in skeleton:
                    str_skeleton += letter + " "
                pside_skeleton.config(text=str_skeleton)
                root.update()
                root.after(2500)
            elif guess not in list(bot_country):
                p_guessing_label.lift()
                p_guessing_label.config(text=f"{guess} is not in the country!")
                p_guessing_label.config(fg="#000000")
                root.update()
                root.after(2500)
                p_guessing_label.config(fg="#bedbe4")

    elif len(guess) > 3:
        if list(guess.upper()) == list(bot_country):
            skeleton = list(bot_country)
            str_skeleton = ""
            for letter in bot_country:
                str_skeleton += letter + " "
            pside_skeleton.config(text=str_skeleton)
        elif list(guess.upper()) != list(bot_country):
            incorrect_cguess = True
    
    bot_string = ""
    for character in skeleton:
        bot_string += character + " "
    return skeleton, incorrect_cguess, player_guessed_letters, bot_string


turn = 0
game_running = True

root.mainloop()
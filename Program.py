#####################################################################################################
#####################################################################################################
# This is the main file for the game Startup Tycoon
# Programpy.py
#####################################################################################################
#####################################################################################################


# Import modules
import random
import numpy as np
import pandas as pd
from flask import Flask

from User import *
from Functions import *
from Workflow import *

from time import sleep


# Set the number of Months
M = 2


# Welcome Message
print("******************************************************************************")
print("Starting The Game! Welcome to Startup Tycoon!")
print("******************************************************************************")

# Print instructions
instructions()

space()

# 1. Setup --> Endowment 10'000

# Ask for number of players
ply = no_of_players()


if ply == "1":
    only_one_player = True
else: 
    only_one_player = False


# Ask player names
players = set_names(ply) 

# Print table with the shops
table()

space()

# Ask for location of the shop
players = ask_location(players=players)


categories = {
    "marketing": ["Run club event", "Influencer collab", "Local newspaper ad", "Coffee testing event", "Advertisement in St Galler Tagblatt"],
    "product development": ["Sell matcha", "Vegan snacks", "Increase products quality"],
    "investment": ["Hire barista", "Buy new machine", "Renovate shop"],
    "none": ["Okay let's relax this month", "Let's go fish for this month", "Okay Boss, holiday for you this month" ]
}

action_cost = {
  'Run club event': -376,
  'Influencer collab': -498,
  'Local newspaper ad': -275,
  'Coffee testing event': -144,
  'Advertisement in St Galler Tagblatt': -429,
  'Sell matcha': -103,
  'Vegan snacks': -276,
  'Increase products quality': -401,
  'Hire barista': -487,
  'Buy new machine': -365,
  'Renovate shop': -444,
  "Okay let's relax this month": -51,
  "Let's go fish for this month": -88,
  "Okay Boss, holiday for you this month": -62
}


outcomes = {
    "Great success": {"transactions": 20, "reputation": 2, "cash": 500},
    "Success": {"transactions": 10, "reputation": 1, "cash": 200},
    "Neutral": {"transactions": 0, "reputation": 0, "cash": -100},
    "Fail": {"transactions": -5, "reputation": -1, "cash": -500},
}



for month in range(1, 2): 
    print(f"********************************** Month {month} **********************************")
    print(" ")
    sleep(1)
    for player in players:
        print(player.name, "it's your turn!")
        if month == 1:
            player.display_status()

        # Select one of the option (keys) for what to imporve in your shop!
        category_choice = None
        while category_choice not in categories:
            print("Choose a category: marketing / product development / investment / none")
            category_choice = input().lower()
            if category_choice not in categories:
                print("Invalid category. Please choose again.")

        # Sleep for better visualization
        sleep(0.5)

        # Select one of the action in the list of the chosen category: each action has a cost (we don't display it)
        action_choice = None
        while action_choice not in categories[category_choice]:
            print("Choose one of the following actions:", categories[category_choice])
            action_choice = input()
            if action_choice not in categories[category_choice]:
                print("Invalid action. Please choose again.")



        print(" ")

        # Random outcome of the chosen action
        outcome = random.choice(list(outcomes.keys()))
        result = outcomes[outcome]

        sleep(3)

        print("***********************************************************************************")
        print("*************** Outcome of the month for you business decision *********************")
        print(" ")
        print("Outcome:", outcome)
        print("Effect:", result)
        print(" ")
        print("***********************************************************************************")

        print(" ")
        sleep(3)

        print("***********************************************************************************")
        print("************************* Time to roll a dice or pay ******************************")
        print(" ")
        # Ask to pay or move like in monoploy
        payment_unevent, event = pay_or_hope()

        print(" ")
        print("***********************************************************************************")
        sleep(1)
        if event:
            print(" ")
            print("The ouctome of your dice is: ")
            sleep(3)
            out = throw_dice_unevent()
            sleep(1)
            print(" ")
            if out: 
                # Unexpected Event
                print("***********************************************************************************")
                print("************************ An Unexpected Event Occurred *****************************")
                print(" ")
                trans, rep, cash_u = unexpected_event()
                print(" ")
                print("***********************************************************************************")
            else:
                trans, rep, cash_u = 0, 0, 0
        else:
            trans, rep, cash_u = 0, 0, 0



        print("Summary of the Month")

        # Apply effects to player
        player.compute_sales(result["transactions"] + trans)
        player.change_reputation(result["reputation"] + rep)

        # Search the cost of the action in the dictionary and add it to the costs
        cost_of_the_action = action_cost[action_choice]


        sleep(1)

        print(" ")

        # This already applies shop profit (after rent, wages, supplies!)
        player.change_endowment(result["cash"] + cash_u + cost_of_the_action + payment_unevent,result["transactions"] + trans)

        # Show updated status
        player.display_status()

        print(" ")

        if player.endowment <= 0:
            print(f"Sorry {player.name}, you are out of money and out of the game!")
            players.remove(player)

            if len(players) == 0:
                print("\033All players are out of money. Game over!\033[0m")
                exit()
                if only_one_player:
                    print("\033[31 END!\033[0m")
                    game_over_ascii()
                    exit()
                elif len(players) == 1:
                    winner = players[0]
                    print_winner(winner.name)
                    end_game()
                    exit()

        if month % 1 == 0:
            k = 1
            m = np.random.randint(1, 2)
            if k == m or player.name == "Jacopo":
                sleep(5)
                print("Oh noooooo! Some rival HSG students \033[31msets fire\033[0m 🔥🔥🔥 to your shop! You have to close it for the rest of the game!")
                sleep(5)
                print_loser(player.name)
                sleep(3)
                players.remove(player)
                if only_one_player:
                    print("\033[31 END!\033[0m")
                    game_over_ascii()
                    exit()
                elif len(players) == 1:
                    winner = players[0]
                    print_winner(winner.name)
                    sleep(3)
                    end_game()
                    exit()

        


    # After last month, game ends: decide the winner 
    if month == 1:
        sleep(4)
        print("***********************************************************************************")
        print("The game has ended! Final results:")
        # Dataframe with results 
        df = final_ranking(players, only_one_player=only_one_player, no_months= M)
        ("***********************************************************************************")

        loser_and_winner(df)

        break












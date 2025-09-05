################################################################################################################
# File Name: User.py
# Description: This file contains the user interface for the Startup Tycoon game.
################################################################################################################


import pyfiglet

def instructions(): 
    """ 
    This function prints the instructions for the game.
    """
    print("Hi! Welcome to the game! We start with some instructions on how to play the game. Are you ready?")
    print("The First Thing you need to do is to choose a location for your shop.")
    print("Each round, you’ll choose an action to grow your business. But be careful, the market is unpredictable, and unexpected disruptions can strike at any time. Your challenge is to make smart decisions, and generate profit. The ultimate goal: earn as much money as possible over 12 months and prove your startup’s success to your competitors!")



def table():
    from tabulate import tabulate
    print("Here is a table with the different shops you can choose from:")
    # Data
    shops = [
        ["Drei Weieren", "A cozy shop by the lake, perfect for summer afternoons."],
        ["HSG - Campus", "Busy student hub with strong espresso for study sessions."],
        ["Altstadt", "Rustic café in the old town with vintage charm."],
        ["Bahnhof", "Fast-paced shop serving commuters fresh coffee on the go."]
    ]

    # Print table
    print(tabulate(shops, headers=["Shop", "Description"], tablefmt="grid"))



def no_of_players():
    print("How many players are going to play? (1-4)")
    players = input()
    if players not in ["1", "2", "3", "4"]:
        print("Invalid number of players. Please choose again.")
        players = no_of_players()
    print(" ")
    return players




def space():
    """
    Just add some spaces for better visualization in the terminal.
    """
    print("******************************************************************************")
    print("                                                                              ")






def game_over_ascii():
    game_over = """
   ██████╗   █████╗  ███╗   ███╗ ███████╗      ██████╗ ██╗   ██╗███████╗██████╗ 
  ██╔═══██╗ ██╔══██╗ ████╗ ████║ ██╔════╝     ██╔═══██╗██║   ██║██╔════╝██╔══██╗
  ██║       ███████║ ██╔████╔██║ █████╗       ██║   ██║██║   ██║█████╗  ██████╔╝
  ██║  ══██ ██╔══██║ ██║╚██╔╝██║ ██╔══╝       ██║   ██║██║   ██║██╔══╝  ██╔══██╗
  ╚██████╔╝ ██║  ██║ ██║ ╚═╝ ██║ ███████╗     ╚██████╔╝╚██████╔╝███████╗██║  ██║
   ╚═════╝  ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚══════╝      ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    print(game_over)



def print_winner(player_name):
    """
    pyfiglet call of the winner
    """
    text = f"{player_name} YOU WIN!"
    banner = pyfiglet.figlet_format(text, font="starwars")  
    print(banner)


def print_loser(player_name):
    """
    pyfiglet print for call of the winner
    """
    text = f"{player_name} YOU ... LOST!"
    banner = pyfiglet.figlet_format(text, font="starwars")  
    print(banner)



def end_game():
    """
    pyfiglet print for call of the winner
    """
    text = "THE GAME IS FINISHED, SEE YOU NEXT TIME"
    banner = pyfiglet.figlet_format(text, font="starwars")  
    print(banner)



DICE_ART = {
    1: (
        "┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘",
    ),
    2: (
        "┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘",
    ),
    3: (
        "┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘",
    ),
    4: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘",
    ),
    5: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘",
    ),
    6: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘",
    ),
}


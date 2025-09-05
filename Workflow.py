################################################################################################################
# File Name: Workflow.py
# Description: This file contains function for the forkflow of the game.
################################################################################################################


from Functions import *
from User import *
import random
import pandas as pd
from time import sleep
import matplotlib.pyplot as plt

def set_names(number_players):
    lista = []
    for i in range(int(number_players)):
        name = input(f"Enter the name of player {i+1}: ")
        player = Player(name)
        lista.append(player)
        print(f"Player {i+1} is {player.name} with an endowment of {player.endowment} and a Coffe shop reputation of {player.reputation_scale[player.reputation]}")
        print(" ")
    return lista


def ask_location(players: list):
    """
    Ask each player to choose a unique shop location.
    """
    available_locations = ["Drei Weieren", "HSG - Campus", "Altstadt", "Bahnhof"]

    for player in players:
        # Keep asking until a valid, available location is chosen
        while True:
            print(f"Hi {player.name}. Choose your location from the following options:")
            print(", ".join(available_locations))
            choice = input("Your choice: ")
            print(" ")
            if choice in available_locations:
                player.place = choice
                player.assign_shop() 
                available_locations.remove(choice)  # make it unavailable for other players
                break
            else:
                print("Invalid or already taken location. Please choose again.")

    return players



def pay_or_hope():
    print("It's the time to choose! Do you want to pay CHF500 or incur in an unexpected event?")
    choice = input("Your choice: (dice/pay) ")

    if choice.lower() == "dice":
        print("You chose to throw a dice!")
        return 0, True
    elif choice.lower() == "pay":
        print("You chose to pay 500 CHF.")
        return -500, False
    else:
        print("Invalid choice. Please type 'dice' or 'pay'.")
        return pay_or_hope()  




def throw_dice_unevent():
    dice_no = np.random.randint(1,7)
    for line in DICE_ART[dice_no]:
        print("                        ", line, "                        ")
    if dice_no == 1 or dice_no == 6:
        return True
    else:
        return False 



def unexpected_event():

    # Events with clear positive/negative tag in the key
    all_events = {
        # Positive
        "Good – Anonymous donation – A mysterious donor left an envelope of cash.": {"transactions": 0, "reputation": 0, "cash": 1000},
        "Good – Erasmus students discovered your shop – Extra transactions this round.": {"transactions": 25, "reputation": 0, "cash": 0},
        "Good – A bus full of tourists stops right in front.": {"transactions": 40, "reputation": 0, "cash": 0},
        "Good – Free samples worked – Customers loved it and bought more.": {"transactions": 25, "reputation": 1, "cash": 0},
        "Good – Coffee and Coding Meetup – Programmers flood your shop for a hackathon.": {"transactions": 30, "reputation": 1, "cash": 0},
        "Good – Customer proposes in your café – The video goes viral!": {"transactions": 0, "reputation": 2, "cash": 0},
        "Good – Student Exam Week – Everyone overdoses on caffeine.": {"transactions": 50, "reputation": 0, "cash": 0},
        "Good – Rainy week – More people came for hot drinks.": {"transactions": 20, "reputation": 0, "cash": 300},
        "Good – Local TV Feature – Your shop is featured on the evening news.": {"transactions": 30, "reputation": 1, "cash": 0},
        "Good – Supplier Discount – Your supplier gives you a bulk deal, supplies cost less.": {"transactions": 0, "reputation": 0, "cash": 500},
        "Good – Food Blogger 5 Stars – Transactions boom after the review.": {"transactions": 35, "reputation": 1, "cash": 0},
        "Good – Customer forgot their wallet but returned with double payment.": {"transactions": 0, "reputation": 0, "cash": 200},
        "Good – Student wrote their thesis in your café – tipped you 0 CHF but gave free publicity.": {"transactions": 0, "reputation": 1, "cash": 0},
        "Good – Board game night – Customers stayed until 3AM playing Monopoly.": {"transactions": 15, "reputation": 0, "cash": -300},
        "Good – Glitch in the Matrix – The universe glitches. All your costs are 0 for this round.": {"transactions": 0, "reputation": 0, "cash": 1000},
        "Good – Finance-Bro Tip War – Two finance bros try to out-tip each other.": {"transactions": 0, "reputation": 0, "cash": 2000},
        "Good – Gallus Blessing – The spirit of Saint Gallus blesses your kitchen.": {"transactions": 0, "reputation": 1, "cash": 500},
        "Good – St. Gallen Weather Miracle – It doesn’t rain for once! Locals celebrate.": {"transactions": 30, "reputation": 1, "cash": 0},
        "Good – Consulting Case Night – Students all buy food 'for research'.": {"transactions": 40, "reputation": 1, "cash": 0},

        # Negative
        "Bad – A group of grandmas steals all your cookies for bingo night": {"transactions": -25, "reputation": 0, "cash": 0},
        "Bad – Your barista spilled 50 cappuccinos in one morning → lose supplies.": {"transactions": 0, "reputation": 0, "cash": -200},
        "Bad – Rival shop spreads rumor that your coffee is decaf.": {"transactions": 0, "reputation": -1, "cash": 0},
        "Bad – Influencer posted a bad review: 'Worst latte art I’ve seen.'": {"transactions": 0, "reputation": -1, "cash": 0},
        "Bad – You sold alcohol to an underage teenager and got a legal fine.": {"transactions": 0, "reputation": -1, "cash": -8000},
        "Bad – Coffee machine breakdown → shop has to close for one week.": {"transactions": -30, "reputation": 0, "cash": 0},
        "Bad – Barista union strike → lose a week of sales.": {"transactions": -25, "reputation": 0, "cash": 0},
        "Bad – Food poisoning of a customer → reputation tanks.": {"transactions": -15, "reputation": -2, "cash": -500},
        "Bad – Food inspector finds a mouse in your shop.": {"transactions": -20, "reputation": -2, "cash": -1000},
        "Bad – You ordered a new item but it was a scam.": {"transactions": 0, "reputation": 0, "cash": -500},
        "Bad – Break-in → someone stole your cash register.": {"transactions": 0, "reputation": 0, "cash": -1000},
        "Bad – Playlist bug → Swiss national hymn on repeat all day.": {"transactions": 0, "reputation": -1, "cash": 0},
        "Bad – Espresso challenge – +20 transactions, but lose 1 reputation for reckless service.": {"transactions": 20, "reputation": -1, "cash": 0},
        "Bad – Wrong delivery – 50kg of onions instead of coffee beans.": {"transactions": -30, "reputation": 0, "cash": -300},
        "Bad – OLMA Cow Rampage – A cow escapes and smashes your shop.": {"transactions": 0, "reputation": 0, "cash": -5000},
        "Bad – START Summit Fail – You forgot your slides, investors boo.": {"transactions": 0, "reputation": -2, "cash": 0},
        "Bad – Säntis Avalanche - City closed down, no customers.": {"transactions": -50, "reputation": 0, "cash": 0},
    }

    # Example: trigger an event
    event_description, effects = random.choice(list(all_events.items()))

    trans = effects["transactions"]
    rep = effects["reputation"]
    cash_u = effects["cash"]

    print(" ")
    sleep(3)
    print(event_description)
    print(f"Your shop is affected as follows: transactions {trans}, reputation {rep}, cash {cash_u}.")
    print(" ")
    sleep(5)


    return trans, rep, cash_u





def final_ranking(players, only_one_player, no_months):
    K = len(players)
    
    if only_one_player:
        # Check if is a good result and def win or loser
        print("Your Final Results are: ")
        print(" ")
        print("Your Reputation is:", players[0].reputation)
        print("Your Cash is:", players[0].endowment)
        print("The Total Customers you has over 12 month are", players[0].cum_transactions)

        money = players[0].money_history
        reput = players[0].reputation_history
        print(money)

        mesi = np.arange(0,no_months)
        print(mesi)


        # Plt
        fig, ax1 = plt.subplots(figsize=(6, 6))

        # Two axis
        ax1.plot(mesi, money, color="blue", label="Cash")
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Cash", color="blue")
        ax1.tick_params(axis='y', labelcolor="blue")

        ax2 = ax1.twinx()
        ax2.plot(mesi, reput, color="red", label="Reputation")
        ax2.set_ylabel("Reputation", color="red")
        ax2.tick_params(axis='y', labelcolor="red")

        # Title
        plt.title("Evolution of the Cash in the Balance Sheet")

        # Optional: show both legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

        plt.show()
        
        end_game()
        exit()


    df = pd.DataFrame(data={
        "Player_name": ["" for _ in range(K)],   
        "Location": ["" for _ in range(K)],      
        "Reputation": np.ones(K),                
        "Cash": np.full(K, 10000),               
        "Tot_Transaction": np.zeros(K, dtype=int),
        "Points": np.zeros(K, dtype=int)})
    
    # Store in the pandas df the data
    for idx, player in enumerate(players):
        df.loc[idx,"Player_name"] = player.name
        df.loc[idx,"Location"] = player.place
        df.loc[idx,"Reputation"] = player.reputation*150
        df.loc[idx,"Cash"] = player.endowment
        df.loc[idx,"Tot_Transaction"] = player.cum_transactions
        df.loc[idx,"Points"] = df.loc[idx,"Reputation"] + df.loc[idx,"Cash"] + df.loc[idx,"Tot_Transaction"]

    df = df.sort_values(by = "Points", ascending=False).set_index(keys = np.arange(1,K+1))


    return df 




def loser_and_winner(df):
    # Number of Row
    K = len(df)
    # Define winner name 
    winner = df.loc[1,"Player_name"]

    losers = [df.loc[i,"Player_name"] for i in range(2,K+1)]
    
    for loser in losers:
        sleep(5)
        print_loser(loser)
        print("***********************************************************************************")
    sleep(3)
    # Show winner 
    print_winner(winner)
    sleep(3)
    print("***********************************************************************************")
    # Show results
    print(df)
    print("***********************************************************************************")
    sleep(5)
    # Show the end game banner
    end_game()





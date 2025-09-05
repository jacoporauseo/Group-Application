################################################################################################################
# File Name: Functions.py
# Description: This file contains the class and function for the Startup Tycoon game.
################################################################################################################

import numpy as np


class Player:
    def __init__(self, name, endowment=10000):
        self.name = name
        self.endowment = endowment
        self.money_history = [endowment]
        self.reputation = 1
        self.cum_transactions = 0
        self.period_transaction = 0
        self.reputation_scale = {0: "Bad", 1: "Average", 2: "Good", 3: "Excellent"}
        self.reputation_history = [1]

    def location(self, possible_locations = ["Drei Weieren", "HSG - Campus", "Altstadt", "Bahnhof"]):
        """
        Ask the player to choose a location for their shop.
        """
        print(f"Hi {self.name}. Choose your location:")
        lieux = input()
        if lieux not in possible_locations:
            print("Invalid location. Please choose again.")
            lieux = self.location()
        self.place = lieux


    def change_endowment(self, unexpected_exp, customers_change):
        """
        Change the endowment of the player by x amount + shop profit.
        Shop profit already accounts for rent, wages, supplies.
        """
        monthly_profit = self.shop.profit(customers_change)   # includes rent!
        #print(monthly_profit)
        self.endowment = self.endowment + unexpected_exp + monthly_profit

        if self.endowment < 0:
            print("You don't have enough money!")

        else:
            self.endowment = self.endowment
            self.money_history.append(self.endowment)
            print(f"{self.name}'s new balance is: {self.endowment} "
                f"(shop profit: {monthly_profit}, Unexpected cash (+/-): {unexpected_exp}, customers change: {customers_change})")
            


    def change_reputation(self, y : int):
        if self.reputation + y >= 0 and self.reputation + y <= 3:
            past_reputation = self.reputation_scale[self.reputation]
            self.reputation += y
            self.reputation_history.append(self.reputation)
            current_rep = self.reputation_scale[self.reputation]
            print(f"Your reputation changed from {past_reputation} to {current_rep}")
        elif self.reputation + y > 3:
            self.reputation = 3
        elif self.reputation + y < 0:
            self.reputation = 0

    
    def compute_sales(self, z : int):
        self.period_transaction = z
        self.cum_transactions += z
        return self.cum_transactions
    

    
    def assign_shop(self): 
        """ Construct a shop object based on the chosen location """
        if self.place == "Altstadt":
            self.shop = AltstadtShop(owner_name=self.name)

        if self.place == "Drei Weieren":
            self.shop = DreiWeierenShop(owner_name=self.name)

        if self.place == "HSG - Campus":
            self.shop = HSGCampusShop(owner_name=self.name)

        if self.place == "Bahnhof":
            self.shop = BahnhofShop(owner_name=self.name)
        return self.shop


    def display_status(self):
        print("******************************************************************************")
        print(f"Player: {self.name}")
        print(f"Endowment: {self.endowment}")
        print(f"Reputation: {self.reputation_scale[self.reputation]}")
        print(f"Cumulative Transactions: {self.cum_transactions}")
        print("******************************************************************************")






class AltstadtShop:
    def __init__(self, owner_name):
        self.owner = owner_name
        self.employees = 1
        self.rent = 975
        self.transactions = 995
        self.location = "Altstadt"
        self.cost_supply_unit = 6
        self.price_unit = 11

    def wage(self):
        return self.employees * 4000

    def revenue(self, customers_change):
        return self.price_unit * (self.transactions + customers_change)
    
    def totalcosts(self):
        supplies_total = round(self.cost_supply_unit * self.transactions * np.random.uniform(0.9, 1.1), 0)
        return self.rent + supplies_total + self.wage()
    
    def profit(self, customers_change):
        return self.revenue(customers_change) - self.totalcosts()
    


class HSGCampusShop:
    def __init__(self, owner_name):
        self.owner = owner_name
        self.employees = 1
        self.rent = 850
        self.transactions = 970
        self.location = "HSG - Campus"
        self.cost_supply_unit = 6
        self.price_unit = 11

    def wage(self):
        return self.employees * 4000

    def revenue(self, customers_change):
        return self.price_unit * (self.transactions + customers_change)
    
    def totalcosts(self):
        supplies_total = round(self.cost_supply_unit * self.transactions * np.random.uniform(0.9, 1.1), 0)
        return self.rent + supplies_total + self.wage()
    
    def profit(self, customers_change):
        return self.revenue(customers_change) - self.totalcosts()


class DreiWeierenShop:
    def __init__(self, owner_name):
        self.owner = owner_name
        self.employees = 1
        self.rent = 700 
        self.transactions = 940 # Each month this much of customers
        self.location = "Drei Weiern"
        self.cost_supply_unit = 6
        self.price_unit = 11

    def wage(self):
        return self.employees * 4000

    def revenue(self, customers_change):
        return self.price_unit * (self.transactions + customers_change)
    
    def totalcosts(self):
        supplies_total = round(self.cost_supply_unit * self.transactions * np.random.uniform(0.9, 1.1), 0)
        return self.rent + supplies_total + self.wage()
    
    def profit(self, customers_change):
        return self.revenue(customers_change) - self.totalcosts()


class BahnhofShop:
    def __init__(self, owner_name):
        self.owner = owner_name
        self.employees = 1
        self.rent = 1100
        self.transactions = 1020
        self.location = "Bahnhof"
        self.cost_supply_unit = 6
        self.price_unit = 11

    def wage(self):
        return self.employees * 4000

    def revenue(self, customers_change):
        return self.price_unit * (self.transactions + customers_change)
    
    def totalcosts(self):
        supplies_total = round(self.cost_supply_unit * self.transactions * np.random.uniform(0.7, 1.3), 0)
        return self.rent + supplies_total + self.wage()
    
    def profit(self, customers_change):
        return self.revenue(customers_change) - self.totalcosts()



































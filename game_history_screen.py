# Author: Gabi Melby
#
# Date: 4/30/2025
#
# Description: This is the format of the saved games. This
# is also the format of the json file.
#
#Used ChatGPT and https://www.geeksforgeeks.org/python-staticmethod/
# -------------------------------------------------------

class GameHistoryScreen:
    @staticmethod #This isn't an object of the class, doesn't need implicit first argument.
    def display(game): #this displays the stats of the game in a nice way
        print(f"\nGame vs {game.opponent}")
        print(f"Date: {game.date.strftime('%Y-%m-%d')}")
        print(f"Q1 Kills: {game.stats.q1_kills}")
        print(f"Q2 Kills: {game.stats.q2_kills}")
        print(f"Q3 Kills: {game.stats.q3_kills}")
        print(f"Q4 Kills: {game.stats.q4_kills}")
        print("-" * 20) #separator line! 
        print(f"Total Kills: {game.stats.total_kills}")
        print(f"Total Stops: {game.stats.total_stops}")
        input("\nPress Enter to return...") #allows user to return. Got this from ChatGPT

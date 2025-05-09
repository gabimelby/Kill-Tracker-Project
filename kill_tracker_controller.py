# Author: Gabi Melby
#
# Date: 4/30/2025
#
# Description: This is the controller file. It provides
# the current state of the game. The controller mediates
# between the view and model and it processes the user inputs.
#
#Used ChatGPT, DeepSeek, and https://www.geeksforgeeks.org/python-property-function/
# -------------------------------------------------------


import json
from datetime import datetime
from pathlib import Path
from game_stats import GameStats, SavedGame


class KillTrackerController:
    def __init__(self): #constructor!!!!!
        #sets the game stats and default values
        self._game_stats = GameStats()
        self._current_quarter = 'Q1'
        self._saved_games = []

    @property #allows you to manage class with more control using getter & setter 
    def game_stats(self):
        #current game statistics
        return self._game_stats

    @property
    def current_quarter(self):
        #current quarter
        return self._current_quarter

    @property #this checks if a kill is active (3 stops in a row) 
    def is_kill_active(self):
        return self._game_stats.is_kill_active

    @property #calculates how many stops in a row
    def consecutive_stops(self):
        return self._game_stats.consecutive_stops

    @property #the list of saved games
    def saved_games(self):
        return self._saved_games

    def change_quarter(self, quarter): #if quarter is changed Q1, Q2, Q3, Q4
        self._current_quarter = quarter

    def add_stop(self): #defensive stop to the counter
        self._game_stats.add_stop()

    def add_kill(self): #adds kill to the quarter counter
        self._game_stats.add_kill(self._current_quarter)

    def reset_stops(self): #resets if there is a stop 
        self._game_stats.reset_stops()

    def reset_all(self): #resets the whole game
        self._game_stats.reset_all()

    #saves the current games stats as a SavedGame instance
    def save_game(self, opponent, date):
        new_stats = GameStats()
        new_stats.q1_kills = self._game_stats.q1_kills
        new_stats.q2_kills = self._game_stats.q2_kills
        new_stats.q3_kills = self._game_stats.q3_kills
        new_stats.q4_kills = self._game_stats.q4_kills
        new_stats.total_stops = self._game_stats.total_stops
        #adds the game to a list
        self._saved_games.append(SavedGame(opponent, date, new_stats))

    #this is my json file where it saves
    def save_to_file(self, filename="basketball_stats.txt"):
        """Save current game and saved games to a text file"""
        data = {
            "current_game": {
                "q1_kills": self._game_stats.q1_kills,
                "q2_kills": self._game_stats.q2_kills,
                "q3_kills": self._game_stats.q3_kills,
                "q4_kills": self._game_stats.q4_kills,
                "total_stops": self._game_stats.total_stops,
                "current_quarter": self._current_quarter,
                "is_kill_active": self._game_stats.is_kill_active,
                "consecutive_stops": self._game_stats.consecutive_stops
            },
            "saved_games": [
                {
                    "opponent": game.opponent,
                    "date": game.date.strftime("%Y-%m-%d"),
                    "stats": {
                        "q1_kills": game.stats.q1_kills,
                        "q2_kills": game.stats.q2_kills,
                        "q3_kills": game.stats.q3_kills,
                        "q4_kills": game.stats.q4_kills,
                        "total_stops": game.stats.total_stops
                    }
                }
                for game in self._saved_games
            ]
        }
        #where it writes it as a json file. Got this from class assignment p5
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    #can input a file and it read the data and add it back in 
    def load_from_file(self, filename="basketball_stats.txt"):
        """Load game data from a text file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Load current game
            current = data.get("current_game", {})
            self._game_stats.q1_kills = current.get("q1_kills", 0)
            self._game_stats.q2_kills = current.get("q2_kills", 0)
            self._game_stats.q3_kills = current.get("q3_kills", 0)
            self._game_stats.q4_kills = current.get("q4_kills", 0)
            self._game_stats.total_stops = current.get("total_stops", 0)
            self._current_quarter = current.get("current_quarter", "Q1")
            self._game_stats.is_kill_active = current.get("is_kill_active", False)
            self._game_stats.consecutive_stops = current.get("consecutive_stops", 0)

            # Load saved games
            self._saved_games = []
            for saved in data.get("saved_games", []):
                stats = GameStats()
                stats.q1_kills = saved["stats"].get("q1_kills", 0)
                stats.q2_kills = saved["stats"].get("q2_kills", 0)
                stats.q3_kills = saved["stats"].get("q3_kills", 0)
                stats.q4_kills = saved["stats"].get("q4_kills", 0)
                stats.total_stops = saved["stats"].get("total_stops", 0)

                date = datetime.strptime(saved["date"], "%Y-%m-%d").date()
                self._saved_games.append(SavedGame(saved["opponent"], date, stats))

            return True
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return False


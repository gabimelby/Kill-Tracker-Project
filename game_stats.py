# Author: Gabi Melby
#
# Date: 4/30/2025
#
# Description: This is the Model file for the MVC. This is 
# the data and logic that tracks the kills, stops, gamestate,
# and also manages game history.
#
#Used ChatGPT and DeepSeek. 
# -------------------------------------------------------

class GameStats:
    #sets the default values as 0
    def __init__(self):
        self.q1_kills = 0
        self.q2_kills = 0
        self.q3_kills = 0
        self.q4_kills = 0
        self.total_stops = 0
        self.is_kill_active = False
        self.consecutive_stops = 0

    @property #calculates the total amount of kills in all quarters
    def total_kills(self):
        return self.q1_kills + self.q2_kills + self.q3_kills + self.q4_kills

    def add_stop(self): #this is the counter to add stops
        self.total_stops += 1 #total stops throughout the whole game
        self.consecutive_stops += 1 #stops in a row cann be reset
        if self.consecutive_stops >= 3: #tracks if opportunity for kill
            self.is_kill_active = True #activates the kill

    def add_kill(self, quarter): #adds the kills to the quarter
        if not self.is_kill_active:
            return
        
        if quarter == 'Q1':
            self.q1_kills += 1
        elif quarter == 'Q2':
            self.q2_kills += 1
        elif quarter == 'Q3':
            self.q3_kills += 1
        elif quarter == 'Q4':
            self.q4_kills += 1
            
        self.is_kill_active = False
        self.consecutive_stops = 0 #resets stops in a row if someone scored

    def reset_stops(self):
        self.is_kill_active = False 
        self.consecutive_stops = 0

    def reset_all(self):  #this resets the whole game to default values
        self.q1_kills = 0 
        self.q2_kills = 0
        self.q3_kills = 0
        self.q4_kills = 0
        self.reset_stops()


class SavedGame:  #gives the opponent, date, and game stats for saved game
    def __init__(self, opponent, date, stats):
        self.opponent = opponent #string
        self.date = date #date
        self.stats = stats #game stats object

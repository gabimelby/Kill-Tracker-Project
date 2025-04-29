class GameStats:
    def __init__(self):
        self.q1_kills = 0
        self.q2_kills = 0
        self.q3_kills = 0
        self.q4_kills = 0
        self.total_stops = 0
        self.is_kill_active = False
        self.consecutive_stops = 0

    @property
    def total_kills(self):
        return self.q1_kills + self.q2_kills + self.q3_kills + self.q4_kills

    def add_stop(self):
        self.total_stops += 1
        self.consecutive_stops += 1
        if self.consecutive_stops >= 3:
            self.is_kill_active = True

    def add_kill(self, quarter):
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
        self.consecutive_stops = 0

    def reset_stops(self):
        self.is_kill_active = False
        self.consecutive_stops = 0

    def reset_all(self):
        self.q1_kills = 0
        self.q2_kills = 0
        self.q3_kills = 0
        self.q4_kills = 0
        self.reset_stops()


class SavedGame:
    def __init__(self, opponent, date, stats):
        self.opponent = opponent
        self.date = date
        self.stats = stats
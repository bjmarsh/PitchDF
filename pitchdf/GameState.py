#
# Simple object for storing all info about the current state of the game
#

import datetime as dt

class GameState:
    def __init__(self):
        self.gid = ""
        self.gamePk = -1
        self.date = dt.datetime(2000,1,1)
        self.away_team = ""
        self.home_team = ""
        self.DH = 1
        self.batter = -1
        self.pitcher = -1
        self.inning = 1
        self.half = "top"
        self.b = 0
        self.s = 0
        self.o = 0
        self.first = -1
        self.second = -1
        self.third = -1
        self.base_state = 0
        self.home_score = 0
        self.away_score = 0
        # scores *after* current at-bat
        self.home_score_after = 0
        self.away_score_after = 0
        self.umpire = -1
        self.BH = "R"
        self.PH = "R"
        self.event = ""
        self.pitch_counts = {}
        self.cur_pc = 0

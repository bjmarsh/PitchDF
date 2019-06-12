import numpy as np
import pandas as pd
import cPickle as pickle
import gzip
from Output import Output

class OutputDF(Output):
    _columns = [
        ("date",  "datetime64[ns]"),
        ("gamePk",      "uint32"),
        ("DH",          "uint8"),
        ("away_team",   "category"),
        ("home_team",   "category"),
        ("inning",      "uint8"),
        ("half",        "category"),
        ("balls",       "uint8"),
        ("strikes",     "uint8"),
        ("outs",        "uint8"),
        ("base_state",  "uint8"),
        ("batter",      "uint32"),
        ("pitcher",     "uint32"),
        ("BH",          "category"),
        ("PH",          "category"),
        ("pitch_count", "uint8"),
        ("home_score",  "uint8"),
        ("away_score",  "uint8"),
        ("home_score_after", "uint8"),
        ("away_score_after", "uint8"),
        ("runner_first",  "int32"),
        ("runner_second", "int32"),
        ("runner_third",  "int32"),
        ("umpire",        "int32"),
        ("is_last_pitch", "bool"),
        ("event",        "category"),
        ("des",          "category"),
        ("strike_type",  "category"),
        ("pitch_type",   "category"),
        ("x",            "float32"),
        ("y",            "float32"),
        ("pfx_x",        "float32"),
        ("pfx_z",        "float32"),
        ("px",           "float32"),
        ("pz",           "float32"),
        ("start_speed",  "float32"),
        ("end_speed",    "float32"),
        ("sz_top",       "float32"),
        ("sz_bot",       "float32"),
        ("x0",           "float32"),
        ("y0",           "float32"),
        ("z0",           "float32"),
        ("vx0",          "float32"),
        ("vy0",          "float32"),
        ("vz0",          "float32"),
        ("ax",           "float32"),
        ("ay",           "float32"),
        ("az",           "float32"),
        ("break_y",      "float32"),
        ("break_angle",  "float32"),
        ("break_length", "float32"),
        ("type_conf",    "float32"),
        ("zone",         "int8"),
        ("nasty",        "int16"),
        ("spin_dir",     "float32"),
        ("spin_rate",    "float32"),
        ("hit_x",        "float32"),
        ("hit_y",        "float32"),
        ("hit_launchAngle",   "float32"),
        ("hit_launchSpeed",   "float32"),
        ("hit_totalDistance", "float32"),
        ("hit_location",      "int8"),
        ("hit_trajectory",    "category"),
        ("hit_hardness",      "category"),
        ]

    def __init__(self, output_file):
        self._output_file = output_file
        self._data = {col:[] for col in zip(*self._columns)[0]}
                
    def add_entry(self, game_state, pitch):
        
        self._data["date"] +=        [game_state.date]
        self._data["gamePk"] +=      [game_state.gamePk]
        self._data["DH"] +=          [game_state.DH]
        self._data["away_team"] +=   [game_state.away_team]
        self._data["home_team"] +=   [game_state.home_team]
        self._data["inning"] +=      [game_state.inning]
        self._data["half"] +=        [game_state.half]
        self._data["balls"] +=       [game_state.b]
        self._data["strikes"] +=     [game_state.s]
        self._data["outs"] +=        [game_state.o]
        self._data["base_state"] +=  [game_state.base_state]
        self._data["batter"] +=      [game_state.batter]
        self._data["pitcher"] +=     [game_state.pitcher]
        self._data["BH"] +=          [game_state.BH]
        self._data["PH"] +=          [game_state.PH]
        self._data["pitch_count"] += [game_state.cur_pc]
        self._data["home_score"] +=  [game_state.home_score]
        self._data["away_score"] +=  [game_state.away_score]
        self._data["home_score_after"] += [game_state.away_score_after]
        self._data["away_score_after"] += [game_state.home_score_after]
        self._data["runner_first"] +=  [game_state.first]
        self._data["runner_second"] += [game_state.second]
        self._data["runner_third"] +=  [game_state.third]
        self._data["umpire"] +=        [game_state.umpire]
        self._data["is_last_pitch"] += [Output.is_last_pitch(game_state,pitch)]
        self._data["event"] +=        [game_state.event]
        self._data["des"] +=          [pitch.des]
        self._data["strike_type"] +=  [Output.get_strike_type(pitch)]
        self._data["pitch_type"] +=   [pitch.pitch_type] 
        self._data["x"] +=            [float(getattr(pitch,"x",-9999))]
        self._data["y"] +=            [float(getattr(pitch,"y",-9999))]
        self._data["pfx_x"] +=        [float(getattr(pitch,"pfx_x",-9999))]
        self._data["pfx_z"] +=        [float(getattr(pitch,"pfx_z",-9999))]
        self._data["px"] +=           [float(getattr(pitch,"px",-9999))]
        self._data["pz"] +=           [float(getattr(pitch,"pz",-9999))]
        self._data["start_speed"] +=  [float(getattr(pitch,"start_speed",-9999))]
        self._data["end_speed"] +=    [float(getattr(pitch,"end_speed",-9999))]
        self._data["sz_top"] +=       [float(getattr(pitch,"sz_top",-9999))]
        self._data["sz_bot"] +=       [float(getattr(pitch,"sz_bot",-9999))]
        self._data["x0"] +=           [float(getattr(pitch,"x0",-9999))]
        self._data["y0"] +=           [float(getattr(pitch,"y0",-9999))]
        self._data["z0"] +=           [float(getattr(pitch,"z0",-9999))]
        self._data["vx0"] +=          [float(getattr(pitch,"vx0",-9999))]
        self._data["vy0"] +=          [float(getattr(pitch,"vy0",-9999))]
        self._data["vz0"] +=          [float(getattr(pitch,"vz0",-9999))]
        self._data["ax"] +=           [float(getattr(pitch,"ax",-9999))]
        self._data["ay"] +=           [float(getattr(pitch,"ay",-9999))]
        self._data["az"] +=           [float(getattr(pitch,"az",-9999))]
        self._data["break_y"] +=      [float(getattr(pitch,"break_y",-9999))]
        self._data["break_angle"] +=  [float(getattr(pitch,"break_angle",-9999))]
        self._data["break_length"] += [float(getattr(pitch,"break_length",-9999))]
        self._data["type_conf"] +=    [float(getattr(pitch,"type_confidence",-9999))]
        self._data["zone"] +=         [int(getattr(pitch,"zone",-1))]
        self._data["nasty"] +=        [int(getattr(pitch,"nasty",-1))]
        self._data["spin_dir"] +=     [float(getattr(pitch,"spin_dir",-9999))]
        self._data["spin_rate"] +=    [float(getattr(pitch,"spin_rate",-9999))]
        self._data["hit_x"] +=        [float(getattr(pitch,"hit_x",-9999))]
        self._data["hit_y"] +=        [float(getattr(pitch,"hit_y",-9999))]
        self._data["hit_launchAngle"] +=   [float(getattr(pitch,"hit_launchAngle",-9999))]
        self._data["hit_launchSpeed"] +=   [float(getattr(pitch,"hit_launchSpeed",-9999))]
        self._data["hit_totalDistance"] += [float(getattr(pitch,"hit_totalDistance",-9999))]
        self._data["hit_location"] +=      [int(getattr(pitch,"hit_location",-1))]
        self._data["hit_trajectory"] +=    [getattr(pitch,"hit_y","NONE")]
        self._data["hit_hardness"] +=      [getattr(pitch,"hit_y","NONE")]
               
    def convert_dtypes(self, df):
        dcols = dict(self._columns)
        for col in df.columns:
            df[col] = df[col].astype(dcols[col])

    def write(self, use_gzip=True):
        self._df = pd.DataFrame.from_dict(self._data)
        self.convert_dtypes(self._df)
        # re-order columns to pre-defined order
        self._df = self._df[list(zip(*self._columns)[0])]
        if use_gzip:
            with gzip.open(self._output_file+".gz", 'wb') as fid:
                pickle.dump(self._df, fid, protocol=-1)
        else:
            with open(self._output_file, 'wb') as fid:
                pickle.dump(self._df, fid, protocol=-1)

    def __del__(self):
        pass

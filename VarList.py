import ROOT
import numpy as np

## game state stuff
year = np.zeros(1, dtype=int)
month = np.zeros(1, dtype=int)
day = np.zeros(1, dtype=int)
DH = np.zeros(1, dtype=int)
inning  = np.zeros(1, dtype=int)
batter  = np.zeros(1, dtype=int)
pitcher = np.zeros(1, dtype=int)
balls   = np.zeros(1, dtype=int)
strikes = np.zeros(1, dtype=int)
outs    = np.zeros(1, dtype=int)
home_score = np.zeros(1, dtype=int)
away_score = np.zeros(1, dtype=int)
runner_first = np.zeros(1, dtype=int)
runner_second = np.zeros(1, dtype=int)
runner_third = np.zeros(1, dtype=int)
umpire = np.zeros(1, dtype=int)
is_last_pitch = np.zeros(1,dtype=int)

gid = ROOT.std.string()
away_team = ROOT.std.string()
home_team = ROOT.std.string()
half = ROOT.std.string()
batter_hand = ROOT.std.string()
pitcher_hand = ROOT.std.string()
event = ROOT.std.string()

## pitchf/x data
des = ROOT.std.string()
type = ROOT.std.string()
pitch_type = ROOT.std.string()
strike_type = ROOT.std.string()  ## C,S,F,FT,FB,MB,B for called, swinging, foul, foul tip, foul bunt, missed bunt, ball

x = np.zeros(1, dtype=float)
y = np.zeros(1, dtype=float)
start_speed = np.zeros(1, dtype=float)
end_speed = np.zeros(1, dtype=float)
sz_top = np.zeros(1, dtype=float)
sz_bot = np.zeros(1, dtype=float)
pfx_x = np.zeros(1, dtype=float)
pfx_z = np.zeros(1, dtype=float)
px = np.zeros(1, dtype=float)
pz = np.zeros(1, dtype=float)
x0 = np.zeros(1, dtype=float)
y0 = np.zeros(1, dtype=float)
z0 = np.zeros(1, dtype=float)
vx0 = np.zeros(1, dtype=float)
vy0 = np.zeros(1, dtype=float)
vz0 = np.zeros(1, dtype=float)
ax = np.zeros(1, dtype=float)
ay = np.zeros(1, dtype=float)
az = np.zeros(1, dtype=float)
break_y = np.zeros(1, dtype=float)
break_angle = np.zeros(1, dtype=float)
break_length = np.zeros(1, dtype=float)
type_confidence = np.zeros(1, dtype=float)
zone = np.zeros(1, dtype=int)
nasty = np.zeros(1, dtype=int)
spin_dir = np.zeros(1, dtype=float)
spin_rate = np.zeros(1, dtype=float)












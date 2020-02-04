import numpy as np
import ROOT
from Output import Output

class OutputROOT(Output):
    def __init__(self, output_file):
        self._fout = ROOT.TFile(output_file, "RECREATE")
        self._t = ROOT.TTree("Pitches","Pitches")

        ## game state stuff
        self._year = np.zeros(1, dtype=int)
        self._month = np.zeros(1, dtype=int)
        self._day = np.zeros(1, dtype=int)
        self._hour = np.zeros(1, dtype=int)
        self._minute = np.zeros(1, dtype=int)
        self._DH = np.zeros(1, dtype=int)
        self._inning   = np.zeros(1, dtype=int)
        self._batter   = np.zeros(1, dtype=int)
        self._pitcher  = np.zeros(1, dtype=int)
        self._abidx    = np.zeros(1, dtype=int)
        self._pitchidx = np.zeros(1, dtype=int)
        self._balls    = np.zeros(1, dtype=int)
        self._strikes  = np.zeros(1, dtype=int)
        self._outs     = np.zeros(1, dtype=int)
        self._pitch_count = np.zeros(1, dtype=int)
        self._home_score = np.zeros(1, dtype=int)
        self._away_score = np.zeros(1, dtype=int)
        self._home_score_afterAB = np.zeros(1, dtype=int)
        self._away_score_afterAB = np.zeros(1, dtype=int)
        self._home_score_afterInn = np.zeros(1, dtype=int)
        self._away_score_afterInn = np.zeros(1, dtype=int)
        self._runner_first = np.zeros(1, dtype=int)
        self._runner_second = np.zeros(1, dtype=int)
        self._runner_third = np.zeros(1, dtype=int)
        self._base_state = np.zeros(1, dtype=int)
        self._umpire = np.zeros(1, dtype=int)
        self._is_last_pitch = np.zeros(1,dtype=int)
        self._gamePk = np.zeros(1,dtype=int)

        self._gid = ROOT.std.string()
        self._away_team = ROOT.std.string()
        self._home_team = ROOT.std.string()
        self._half = ROOT.std.string()
        self._batter_hand = ROOT.std.string()
        self._pitcher_hand = ROOT.std.string()
        self._event = ROOT.std.string()

        ## pitchf/x data
        self._des = ROOT.std.string()
        self._type = ROOT.std.string()
        self._pitch_type = ROOT.std.string()
        self._strike_type = ROOT.std.string()  ## C,S,F,FT,FB,MB,B for called, swinging, foul, foul tip, foul bunt, missed bunt, ball

        self._x = np.zeros(1, dtype=float)
        self._y = np.zeros(1, dtype=float)
        self._start_speed = np.zeros(1, dtype=float)
        self._end_speed = np.zeros(1, dtype=float)
        self._sz_top = np.zeros(1, dtype=float)
        self._sz_bot = np.zeros(1, dtype=float)
        self._pfx_x = np.zeros(1, dtype=float)
        self._pfx_z = np.zeros(1, dtype=float)
        self._px = np.zeros(1, dtype=float)
        self._pz = np.zeros(1, dtype=float)
        self._x0 = np.zeros(1, dtype=float)
        self._y0 = np.zeros(1, dtype=float)
        self._z0 = np.zeros(1, dtype=float)
        self._vx0 = np.zeros(1, dtype=float)
        self._vy0 = np.zeros(1, dtype=float)
        self._vz0 = np.zeros(1, dtype=float)
        self._ax = np.zeros(1, dtype=float)
        self._ay = np.zeros(1, dtype=float)
        self._az = np.zeros(1, dtype=float)
        self._break_y = np.zeros(1, dtype=float)
        self._break_angle = np.zeros(1, dtype=float)
        self._break_length = np.zeros(1, dtype=float)
        self._type_confidence = np.zeros(1, dtype=float)
        self._zone = np.zeros(1, dtype=int)
        self._nasty = np.zeros(1, dtype=int)
        self._spin_dir = np.zeros(1, dtype=float)
        self._spin_rate = np.zeros(1, dtype=float)
        # self._pitch_type_id = np.zeros(1, dtype=int)

        # statcast hit data
        self._hit_x = np.zeros(1, dtype=float)
        self._hit_y = np.zeros(1, dtype=float)
        self._hit_launchAngle = np.zeros(1, dtype=float)
        self._hit_launchSpeed = np.zeros(1, dtype=float)
        self._hit_totalDistance = np.zeros(1, dtype=float)
        self._hit_location = np.zeros(1, dtype=int)
        self._hit_trajectory = ROOT.std.string()
        self._hit_hardness = ROOT.std.string()

        # game state stuff
        self._t.Branch("year", self._year, 'year/I')
        self._t.Branch("month", self._month, 'month/I')
        self._t.Branch("day", self._day, 'day/I')
        self._t.Branch("hour", self._hour, 'hour/I')
        self._t.Branch("minute", self._minute, 'minute/I')
        self._t.Branch("DH", self._DH, 'DH/I')
        self._t.Branch("inning", self._inning, 'inning/I')
        self._t.Branch("batter", self._batter, 'batter/I')
        self._t.Branch("pitcher", self._pitcher, 'pitcher/I')
        self._t.Branch("abidx", self._abidx, 'abidx/I')
        self._t.Branch("pitchidx", self._pitchidx, 'pitchidx/I')
        self._t.Branch("balls", self._balls, 'balls/I')
        self._t.Branch("strikes", self._strikes, 'strikes/I')
        self._t.Branch("outs", self._outs, 'outs/I')
        self._t.Branch("pitch_count", self._pitch_count, 'pitch_count/I')
        self._t.Branch("home_score", self._home_score, 'home_score/I')
        self._t.Branch("away_score", self._away_score, 'away_score/I')
        self._t.Branch("home_score_afterAB", self._home_score_afterAB, 'home_score_afterAB/I')
        self._t.Branch("away_score_afterAB", self._away_score_afterAB, 'away_score_afterAB/I')
        self._t.Branch("home_score_afterInn", self._home_score_afterInn, 'home_score_afterInn/I')
        self._t.Branch("away_score_afterInn", self._away_score_afterInn, 'away_score_afterInn/I')
        self._t.Branch("runner_first", self._runner_first, 'runner_first/I')
        self._t.Branch("runner_second", self._runner_second, 'runner_second/I')
        self._t.Branch("runner_third", self._runner_third, 'runner_third/I')
        self._t.Branch("base_state", self._base_state, 'base_state/I')
        self._t.Branch("umpire", self._umpire, 'umpire/I')
        self._t.Branch("is_last_pitch", self._is_last_pitch, 'is_last_pitch/I')
        self._t.Branch("gamePk", self._gamePk, "gamePk/I")
        
        self._t.Branch("gid", self._gid)
        self._t.Branch("away_team", self._away_team)
        self._t.Branch("home_team", self._home_team)
        self._t.Branch("half", self._half)
        self._t.Branch("batter_hand", self._batter_hand)
        self._t.Branch("pitcher_hand", self._pitcher_hand)
        self._t.Branch("event", self._event)
        
        # pitchf/x data
        self._t.Branch("des", self._des)
        self._t.Branch("type", self._type)
        self._t.Branch("pitch_type", self._pitch_type)
        self._t.Branch("strike_type", self._strike_type)

        self._t.Branch("x", self._x, 'x/D')
        self._t.Branch("y", self._y, 'y/D')
        self._t.Branch("start_speed", self._start_speed, 'start_speed/D')
        self._t.Branch("end_speed", self._end_speed, 'end_speed/D')
        self._t.Branch("sz_top", self._sz_top, 'sz_top/D')
        self._t.Branch("sz_bot", self._sz_bot, 'sz_bot/D')
        self._t.Branch("pfx_x", self._pfx_x, 'pfx_x/D')
        self._t.Branch("pfx_z", self._pfx_z, 'pfx_z/D')
        self._t.Branch("px", self._px, 'px/D')
        self._t.Branch("pz", self._pz, 'pz/D')
        self._t.Branch("x0", self._x0, 'x0/D')
        self._t.Branch("y0", self._y0, 'y0/D')
        self._t.Branch("z0", self._z0, 'z0/D')
        self._t.Branch("vx0", self._vx0, 'vx0/D')
        self._t.Branch("vy0", self._vy0, 'vy0/D')
        self._t.Branch("vz0", self._vz0, 'vz0/D')
        self._t.Branch("ax", self._ax, 'ax/D')
        self._t.Branch("ay", self._ay, 'ay/D')
        self._t.Branch("az", self._az, 'az/D')
        self._t.Branch("break_y", self._break_y, 'break_y/D')
        self._t.Branch("break_angle", self._break_angle, 'break_angle/D')
        self._t.Branch("break_length", self._break_length, 'break_length/D')
        self._t.Branch("type_confidence", self._type_confidence, 'type_confidence/D')
        self._t.Branch("zone", self._zone, 'zone/I')
        self._t.Branch("nasty", self._nasty, 'nasty/I')
        self._t.Branch("spin_dir", self._spin_dir, 'spin_dir/D')
        self._t.Branch("spin_rate", self._spin_rate, 'spin_rate/D')
        # self._t.Branch("pitch_type_id", self._pitch_type_id, 'pitch_type_id/I')
        self._t.Branch("hit_x", self._hit_x, "hit_x/D")
        self._t.Branch("hit_y", self._hit_y, "hit_y/D")
        self._t.Branch("hit_launchAngle", self._hit_launchAngle, "hit_launchAngle/D")
        self._t.Branch("hit_launchSpeed", self._hit_launchSpeed, "hit_launchSpeed/D")
        self._t.Branch("hit_totalDistance", self._hit_totalDistance, "hit_totalDistance/D")
        self._t.Branch("hit_location", self._hit_location, "hit_location/I")
        self._t.Branch("hit_trajectory", self._hit_trajectory)
        self._t.Branch("hit_hardness", self._hit_hardness)
        
    def add_entry(self, game_state, pitch):
        # game state
        self._year[0] = game_state.date.year
        self._month[0] = game_state.date.month
        self._day[0] = game_state.date.day
        self._hour[0] = game_state.date.hour
        self._minute[0] = game_state.date.minute
        self._DH[0] = game_state.DH
        self._inning[0] = game_state.inning
        self._batter[0] = game_state.batter
        self._pitcher[0] = game_state.pitcher
        self._abidx[0] = game_state.abidx
        self._pitchidx[0] = pitch.pitchidx
        self._balls[0] = game_state.b
        self._strikes[0] = game_state.s
        self._outs[0] = game_state.o
        self._pitch_count[0] = game_state.cur_pc
        self._home_score[0] = game_state.home_score
        self._away_score[0] = game_state.away_score
        self._home_score_afterAB[0] = game_state.home_score_afterAB
        self._away_score_afterAB[0] = game_state.away_score_afterAB
        self._home_score_afterInn[0] = game_state.home_score_afterInn
        self._away_score_afterInn[0] = game_state.away_score_afterInn
        self._runner_first[0] = game_state.first
        self._runner_second[0] = game_state.second
        self._runner_third[0] = game_state.third
        self._base_state[0] = game_state.base_state
        self._umpire[0] = game_state.umpire
        self._gamePk[0] = game_state.gamePk
        
        n = ROOT.std.string.npos
        self._gid.replace(0, n, game_state.gid)
        self._away_team.replace(0, n, game_state.away_team)
        self._home_team.replace(0, n, game_state.home_team)
        self._half.replace(0, n, game_state.half)
        self._batter_hand.replace(0, n, game_state.BH)
        self._pitcher_hand.replace(0, n, game_state.PH)
        self._event.replace(0, n, game_state.event)
        
        #pitchf/x data
        self._des.replace(0, n, pitch.des)
        self._type.replace(0, n, pitch.type)
        self._pitch_type.replace(0, n, pitch.pitch_type)
        st = Output.get_strike_type(pitch)
        self._strike_type.replace(0, n, st)

        self._x[0] = float(getattr(pitch,"x",-9999))
        self._y[0] = float(getattr(pitch,"y",-9999))
        self._start_speed[0] = float(getattr(pitch,"start_speed",-9999))
        self._end_speed[0] = float(getattr(pitch,"end_speed",-9999))
        self._sz_top[0] = float(getattr(pitch,"sz_top",-9999))
        self._sz_bot[0] = float(getattr(pitch,"sz_bot",-9999))
        self._pfx_x[0] = float(getattr(pitch,"pfx_x",-9999))
        self._pfx_z[0] = float(getattr(pitch,"pfx_z",-9999))
        self._px[0] = float(getattr(pitch,"px",-9999))
        self._pz[0] = float(getattr(pitch,"pz",-9999))
        self._x0[0] = float(getattr(pitch,"x0",-9999))
        self._y0[0] = float(getattr(pitch,"y0",-9999))
        self._z0[0] = float(getattr(pitch,"z0",-9999))
        self._vx0[0] = float(getattr(pitch,"vx0",-9999))
        self._vy0[0] = float(getattr(pitch,"vy0",-9999))
        self._vz0[0] = float(getattr(pitch,"vz0",-9999))
        self._ax[0] = float(getattr(pitch,"ax",-9999))
        self._ay[0] = float(getattr(pitch,"ay",-9999))
        self._az[0] = float(getattr(pitch,"az",-9999))
        self._break_y[0] = float(getattr(pitch,"break_y",-9999))
        self._break_angle[0] = float(getattr(pitch,"break_angle",-9999))
        self._break_length[0] = float(getattr(pitch,"break_length",-9999))
        self._type_confidence[0] = float(getattr(pitch,"type_confidence",-9999))
        self._zone[0] = int(getattr(pitch,"zone",-1))
        self._nasty[0] = int(getattr(pitch,"nasty",-1))
        self._spin_dir[0] = float(getattr(pitch,"spin_dir",-9999))
        self._spin_rate[0] = float(getattr(pitch,"spin_rate",-9999))
        if pitch.pitch_type not in self._unique_pitch_types:
            print "NEW PITCH:", pitch.pitch_type
            self._unique_pitch_types.append(pitch.pitch_type)
        # self._pitch_type_id[0] = int(self._unique_pitch_types.index(pitch.pitch_type)-1)
            
        self._is_last_pitch[0] = Output.is_last_pitch(game_state, pitch)

        # statcast hit data
        self._hit_x[0] = float(getattr(pitch,"hit_x", -9999))
        self._hit_y[0] = float(getattr(pitch,"hit_y", -9999))
        self._hit_launchAngle[0] = float(getattr(pitch,"hit_launchAngle", -9999))
        self._hit_launchSpeed[0] = float(getattr(pitch,"hit_launchSpeed", -9999))
        self._hit_totalDistance[0] = float(getattr(pitch,"hit_totalDistance", -9999))
        self._hit_location[0] = int(getattr(pitch,"hit_location", -1))
        self._hit_trajectory.replace(0, n, getattr(pitch,"hit_trajectory", "NONE"))
        self._hit_hardness.replace(0, n, getattr(pitch,"hit_hardness", "NONE"))

        self._t.Fill()

    def write(self):
        self._fout.cd()
        self._t.Write("Pitches",ROOT.TObject.kWriteDelete)

    def __del__(self):
        self._fout.Close()

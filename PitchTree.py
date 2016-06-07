import ROOT
import VarList as var

t = ROOT.TTree("Pitches","Pitches")

def Init():
    global t
    # game state stuff
    t.Branch("year", var.year, 'year/I')
    t.Branch("month", var.month, 'month/I')
    t.Branch("day", var.day, 'day/I')
    t.Branch("DH", var.DH, 'DH/I')
    t.Branch("inning", var.inning, 'inning/I')
    t.Branch("batter", var.batter, 'batter/I')
    t.Branch("pitcher", var.pitcher, 'pitcher/I')
    t.Branch("balls", var.balls, 'balls/I')
    t.Branch("strikes", var.strikes, 'strikes/I')
    t.Branch("outs", var.outs, 'outs/I')
    t.Branch("home_score", var.home_score, 'home_score/I')
    t.Branch("away_score", var.away_score, 'away_score/I')
    t.Branch("runner_first", var.runner_first, 'runner_first/I')
    t.Branch("runner_third", var.runner_third, 'runner_third/I')
    t.Branch("umpire", var.umpire, 'umpire/I')
    t.Branch("is_last_pitch",var.is_last_pitch, 'is_last_pitch/I')

    t.Branch("gid", var.gid)
    t.Branch("away_team", var.away_team)
    t.Branch("home_team", var.home_team)
    t.Branch("half", var.half)
    t.Branch("batter_hand", var.batter_hand)
    t.Branch("pitcher_hand", var.pitcher_hand)
    t.Branch("event", var.event)

    # pitchf/x data
    t.Branch("des", var.des)
    t.Branch("type", var.type)
    t.Branch("pitch_type", var.pitch_type)
    t.Branch("strike_type", var.strike_type)

    t.Branch("x", var.x, 'x/D')
    t.Branch("y", var.y, 'y/D')
    t.Branch("start_speed", var.start_speed, 'start_speed/D')
    t.Branch("end_speed", var.end_speed, 'end_speed/D')
    t.Branch("sz_top", var.sz_top, 'sz_top/D')
    t.Branch("sz_bot", var.sz_bot, 'sz_bot/D')
    t.Branch("pfx_x", var.pfx_x, 'pfx_x/D')
    t.Branch("pfx_z", var.pfx_z, 'pfx_z/D')
    t.Branch("px", var.px, 'px/D')
    t.Branch("pz", var.pz, 'pz/D')
    t.Branch("x0", var.x0, 'x0/D')
    t.Branch("y0", var.y0, 'y0/D')
    t.Branch("z0", var.z0, 'z0/D')
    t.Branch("vx0", var.vx0, 'vx0/D')
    t.Branch("vy0", var.vy0, 'vy0/D')
    t.Branch("vz0", var.vz0, 'vz0/D')
    t.Branch("ax", var.ax, 'ax/D')
    t.Branch("ay", var.ay, 'ay/D')
    t.Branch("az", var.az, 'az/D')
    t.Branch("break_y", var.break_y, 'break_y/D')
    t.Branch("break_angle", var.break_angle, 'break_angle/D')
    t.Branch("break_length", var.break_length, 'break_length/D')
    t.Branch("type_confidence", var.type_confidence, 'type_confidence/D')
    t.Branch("zone", var.zone, 'zone/I')
    t.Branch("nasty", var.nasty, 'nasty/I')
    t.Branch("spin_dir", var.spin_dir, 'spin_dir/D')
    t.Branch("spin_rate", var.spin_rate, 'spin_rate/D')

def Fill(game_state, pitch):
    global t
    # game state
    var.year[0] = game_state['year']
    var.month[0] = game_state['month']
    var.day[0] = game_state['day']
    var.DH[0] = game_state['DH']
    var.inning[0] = game_state["inning"]
    var.batter[0] = game_state["batter"]
    var.pitcher[0] = game_state["pitcher"]
    var.balls[0] = game_state["b"]
    var.strikes[0] = game_state["s"]
    var.outs[0] = game_state["o"]
    var.home_score[0] = game_state["home_score"]
    var.away_score[0] = game_state["away_score"]
    var.runner_first[0] = game_state["first"]
    var.runner_second[0] = game_state["second"]
    var.runner_third[0] = game_state["third"]
    var.umpire[0] = game_state["umpire"]

    n = ROOT.std.string.npos
    var.gid.replace(0, n, game_state["gid"])
    var.away_team.replace(0, n, game_state["away_team"])
    var.home_team.replace(0, n, game_state["home_team"])
    var.half.replace(0, n, game_state["half"])
    var.batter_hand.replace(0, n, game_state["BH"])
    var.pitcher_hand.replace(0, n, game_state["PH"])
    var.event.replace(0, n, game_state["event"])

    #pitchf/x data
    var.des.replace(0, n, pitch["des"])
    var.type.replace(0, n, pitch["type"])
    var.pitch_type.replace(0, n, pitch["pitch_type"])
    st = pitch['type']
    if st=='S':
        if 'Called' in pitch['des']:
            st = 'C'
        elif 'Swinging' in pitch['des']:
            st = 'S'
        elif 'Foul Tip' in pitch['des']:
            st = 'FT'
        elif 'Foul Bunt' in pitch['des']:
            st = 'FB'
        elif 'Foul'in pitch['des']:
            st = 'F'
        elif 'Missed Bunt' in pitch['des']:
            st = 'MB'
        else:
            raise Exception("Unknown strike description: "+pitch['des'])
    var.strike_type.replace(0, n, st)

    var.x[0] = float(pitch.get("x",-9999))
    var.y[0] = float(pitch.get("y",-9999))
    var.start_speed[0] = float(pitch.get("start_speed",-9999))
    var.end_speed[0] = float(pitch.get("end_speed",-9999))
    var.sz_top[0] = float(pitch.get("sz_top",-9999))
    var.sz_bot[0] = float(pitch.get("sz_bot",-9999))
    var.pfx_x[0] = float(pitch.get("pfx_x",-9999))
    var.pfx_z[0] = float(pitch.get("pfx_z",-9999))
    var.px[0] = float(pitch.get("px",-9999))
    var.pz[0] = float(pitch.get("pz",-9999))
    var.x0[0] = float(pitch.get("x0",-9999))
    var.y0[0] = float(pitch.get("y0",-9999))
    var.z0[0] = float(pitch.get("z0",-9999))
    var.vx0[0] = float(pitch.get("vx0",-9999))
    var.vy0[0] = float(pitch.get("vy0",-9999))
    var.vz0[0] = float(pitch.get("vz0",-9999))
    var.ax[0] = float(pitch.get("ax",-9999))
    var.ay[0] = float(pitch.get("ay",-9999))
    var.az[0] = float(pitch.get("az",-9999))
    var.break_y[0] = float(pitch.get("break_y",-9999))
    var.break_angle[0] = float(pitch.get("break_angle",-9999))
    var.break_length[0] = float(pitch.get("break_length",-9999))
    var.type_confidence[0] = float(pitch.get("type_confidence",-9999))
    var.zone[0] = int(pitch.get("zone",-9999))
    var.nasty[0] = int(pitch.get("nasty",-9999))
    var.spin_dir[0] = float(pitch.get("spin_dir",-9999))
    var.spin_rate[0] = float(pitch.get("spin_rate",-9999))

    var.is_last_pitch[0] = 0
    if var.type=='X' or \
            (var.type=='B' and var.balls[0]==3) or \
            (var.strike_type in ['S','C','FB','FT','MB'] and var.strikes[0]==2) or \
            var.des=="Hit By Pitch":
        var.is_last_pitch[0] = 1

    t.Fill()





import ROOT
import VarList as var

t = ROOT.TTree("Pitches","Pitches")

def Init():
    global t
    t.Branch("inning", var.inning, 'inning/I')
    t.Branch("batter", var.batter, 'batter/I')
    t.Branch("pitcher", var.pitcher, 'pitcher/I')
    t.Branch("balls", var.balls, 'balls/I')
    t.Branch("strikes", var.strikes, 'strikes/I')
    t.Branch("outs", var.outs, 'outs/I')
    t.Branch("pitch_type", var.pitch_type)

def Fill(game_state, pitch):
    global t
    var.inning[0] = game_state["inning"]
    var.batter[0] = game_state["batter"]
    var.pitcher[0] = game_state["pitcher"]
    var.balls[0] = game_state["b"]
    var.strikes[0] = game_state["s"]
    var.outs[0] = game_state["o"]

    #strings
    var.pitch_type.replace(0, ROOT.std.string.npos, pitch["pitch_type"])

    t.Fill()





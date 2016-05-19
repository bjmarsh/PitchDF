import ROOT
import urllib2
import xml.etree.ElementTree as ET
import PitchTree as pt

def processAction(action, game_state):
    att = action.attrib

    if att['event'] == 'Offensive Sub':
        game_state['batter'] = att['player']
    elif att['event'] == 'Pitching Substitution':
        game_state['pitcher'] = att['player']
    elif att['event'] == 'Game Advisory':
        pass
    elif att['event'] == 'Passed Ball':
        pass
    elif att['event'] == 'Wild Pitch':
        pass
    elif att['event'] == 'Defensive Switch':
        pass
    elif att['event'] == 'Stolen Base 2B':
        pass
    elif att['event'] == 'Stolen Base 3B':
        pass
    elif att['event'] == 'Caught Stealing 2B':
        pass
    elif att['event'] == 'Caught Stealing 3B':
        pass
    elif att['event'] == 'Umpire Substitution':
        pass
    else:
        raise Exception("Unknown action: {0}".format(att['event']))


def processRunner(runner, game_state):
    att = runner.attrib

    base_map = {'1B':'first', '2B':'second', '3B':'third'}

    if att['start'] != '':
        game_state[base_map[att['start']]] = ''
    if att['end'] != '':
        game_state[base_map[att['end']]] = att['id']
    

def processPitch(pitch, game_state):
    att = pitch.attrib

    try:
        pitch_type = att['pitch_type']
    except:
        pitch_type = "UN"  #unknown
        att['pitch_type'] = pitch_type

    # print "Inning: {0}, Pitcher: {1}, Batter: {2}, Count: {3}-{4}, Outs: {5}, Pitch Type: {6}, Result: {7}".format(
    #     game_state["inning"], game_state['pitcher'], game_state['batter'], game_state['b'], game_state['s'], game_state['o'], pitch_type, att['type'])

    if 'on_1b' in att.keys():
        game_state['first'] = att['on_1b']
    if 'on_2b' in att.keys():
        game_state['second'] = att['on_2b']
    if 'on_3b' in att.keys():
        game_state['third'] = att['on_3b']

    ## save pitch info here!
    pt.Fill(game_state,att)

    if att['type']=='B':
        game_state['b'] += 1
    if att['type']=='S' and game_state['s']<2:
        game_state['s'] += 1

                                                                                                

def processAtBat(atbat, game_state):
    att = atbat.attrib
    game_state['b'] = 0
    game_state['s'] = 0
    game_state['batter'] = att['batter']
    game_state['pitcher'] = att['pitcher']
    game_state['PH'] = att['p_throws']
    game_state['BH'] = att['stand']
    game_state['home_runs'] = att['home_team_runs']
    game_state['away_runs'] = att['away_team_runs']

    # print att['des']
    # print game_state

    for i in range(len(atbat)):
        evt = atbat[i]
        evt_type = evt.tag

        if evt_type == 'pitch':
            processPitch(evt, game_state)
        elif evt_type == 'runner':
            processRunner(evt, game_state)
        elif evt_type == 'po' and 'Pickoff Attempt' in evt.attrib['des']:
            pass
        else:
            raise Exception('Unknown event within atbat: {0}'.format(evt_type))

    game_state['o'] = att['o']

fout = ROOT.TFile("pitches.root","RECREATE")
pt.Init()

url = "http://gd2.mlb.com/components/game/mlb/year_2016/month_04/day_15/gid_2016_04_15_colmlb_chnmlb_1/inning/inning_all.xml"
response = urllib2.urlopen(url)
xml = response.read()

game = ET.fromstring(xml)

game_state = {'batter':'', 'pitcher':'', 'inning':1, 'half':'top', 'b':0, 's':0, 'o':0, 'first':'', 'second':'', 'third':'', 'home_runs':0, 'away_runs':0, 'umpire':'', 'BH':'R', 'PH':'L'}

for inning in game:
    game_state['inning'] = int(inning.attrib['num'])
    
    # loop over top/bottom
    for i in range(len(inning)):
        half = inning[i]
        game_state['o'] = 0

        if half.tag not in ['top','bottom']:
            raise Exception(half.tag + " is not a valid half-inning name!!")

        game_state['half'] = half.tag
    
        for j in range(len(half)):
            evt = half[j]
            evt_type = evt.tag
            
            if evt_type == 'atbat':
                processAtBat(evt, game_state)
            elif evt_type == 'action':
                processAction(evt, game_state)
            else:
                raise Exception("Unknown event within inning: {0}".format(evt_type))
                
pt.t.Write()
fout.Close()

#! /usr/bin/env python
import ROOT
import glob
import os
import xml.etree.ElementTree as ET
from PitchTree import PitchTree
import VarList as var

def processAction(action, game_state):
    att = action.attrib

    # runner tag should take care of most of these
    ignoreActions=["Game Advisory", "Passed Ball", "Wild Pitch", "Defensive Switch", "Defensive Sub",
                   "Stolen Base 2B", "Stolen Base 3B", "Caught Stealing 2B", "Caught Stealing 3B",
                   "Pickoff 1B", "Pickoff 2B", "Pickoff 3B", "Player Injured", "Runner Out", "Balk",
                   "Manager Review", "Defensive Indiff", "Batter Turn", "Pickoff Error 1B",
                   "Pickoff Error 2B", "Pickoff Error 3B", "Error", "Umpire Review", "Ejection",
                   "Picked off stealing 2B", "Picked off stealing 3B", "Caught Stealing Home",
                   "Runner Advance", "Field Error", "Pitcher Switch", "Picked off stealing home", 
                   "Pickoff Attempt 1B", "Stolen Base Home", "Base Running Double Play",
                   "Pitch Challenge", "Pickoff Attempt 2B"]

    if att['event'].lower() == 'offensive sub':
        game_state['batter'] = att['player']
    elif att['event'] == 'Pitching Substitution':
        game_state['pitcher'] = att['player']
    elif att['event'] == 'Umpire Substitution':
        if "replaces HP umpire" in att['des']:
            game_state['umpire'] = int(att['player'])
    elif att['event'] in ignoreActions:
        pass
    else:
        raise Exception("Unknown action: {0}".format(att['event']))


def processRunner(runner, game_state):
    att = runner.attrib

    base_map = {'1B':'first', '2B':'second', '3B':'third'}

    if att['start'] != '' and game_state[base_map[att['start']]]==int(att['id']):
        game_state[base_map[att['start']]] = -1
    if att['end'] != '':
        game_state[base_map[att['end']]] = int(att['id'])

    if att.get('score','F')=='T' and game_state['home_score']>-1:
        if game_state['half']=='top':
            game_state['away_score'] += 1
        if game_state['half']=='bottom':
            game_state['home_score'] += 1

    game_state["base_state"] = 0
    if game_state["first"] != -1:
        game_state["base_state"] |= (1<<0)
    if game_state["second"] != -1:
        game_state["base_state"] |= (1<<1)
    if game_state["third"] != -1:
        game_state["base_state"] |= (1<<2)
    

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
        game_state['first'] = int(att['on_1b'])
    if 'on_2b' in att.keys():
        game_state['second'] = int(att['on_2b'])
    if 'on_3b' in att.keys():
        game_state['third'] = int(att['on_3b'])

    game_state['pitch_counts'][game_state['pitcher']] += 1
    game_state['cur_pc'] = game_state['pitch_counts'][game_state['pitcher']]

    ## save pitch info here!
    pt.Fill(game_state,att)

    if att['type']=='B':
        game_state['b'] += 1
    if att['type']=='S' and game_state['s']<2:
        game_state['s'] += 1

                                                                                                

def processAtBat(atbat, game_state):
    global unique_events

    att = atbat.attrib
    game_state['b'] = 0
    game_state['s'] = 0
    game_state['batter'] = int(att['batter'])
    game_state['pitcher'] = int(att['pitcher'])
    game_state['PH'] = att['p_throws']
    game_state['BH'] = att['stand']

    try:
        game_state['home_score_after'] = int(att['home_team_runs'])
        game_state['away_score_after'] = int(att['away_team_runs'])
    except KeyError:
        game_state['home_score_after'] = -1
        game_state['away_score_after'] = -1
        print "    WARNING: game scores not listed in XML!"

    if game_state['pitcher'] not in game_state['pitch_counts']:
        game_state['pitch_counts'][game_state['pitcher']] = 0

    game_state['event'] = att['event']

    if game_state['event'] not in unique_events:
        print "{0:25s}:{1}".format(game_state['event'], game_state['gid'])
        unique_events.append(game_state['event'])

    for i in range(len(atbat)):
        evt = atbat[i]
        evt_type = evt.tag

        if evt_type == 'pitch':
            processPitch(evt, game_state)
        elif evt_type == 'runner':
            processRunner(evt, game_state)
        elif evt_type == 'po':
            pass
        else:
            raise Exception('Unknown event within atbat: {0}'.format(evt_type))

    game_state['o'] = att['o']

def parseGame(gameID):

    game_state = {'batter':-1, 'pitcher':-1, 'inning':1, 'half':'top', 'b':0, 's':0, 'o':0, 'first':-1, 'second':-1, 'third':-1, 'base_state':0, 'home_score':0, 'away_score':0, 'home_score_after':0, 'away_score_after':0,
                  'umpire':-1, 'BH':'R', 'PH':'L', 'event':'', 'pitch_counts':{}, 'cur_pc':0}
    game_state['year'] = int(gameID[4:8])

    base_dir = "/nfs-7/userdata/bemarsh/gamelogs/{0}/".format(year) + gameID
    inningXML = open(os.path.join(base_dir,"inning_all.xml"))
    playerXML = open(os.path.join(base_dir,"players.xml"))

    gameData = ET.fromstring(inningXML.read())
    playerData = ET.fromstring(playerXML.read())
    
    inningXML.close()
    playerXML.close()

    game_state['gid'] = gameID
    game_state['month'] = int(gameID[9:11])
    game_state['day'] = int(gameID[12:14])
    game_state['away_team'] = gameID[15:18]
    game_state['home_team'] = gameID[22:25]
    game_state['DH'] = int(gameID[-1])

    for ump in playerData[2]:
        if ump.attrib["position"]=="home":
            game_state["umpire"] = int(ump.attrib["id"])

    for inning in gameData:
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

unique_events = []                
year = 2019

## Open up output root file and initialize tree
fout = ROOT.TFile("pitches_{0}.root".format(year),"RECREATE")
pt = PitchTree()
pt.Init()

curdir = os.getcwd()
os.chdir("/nfs-7/userdata/bemarsh/gamelogs/{0}".format(year))
gameIDs = sorted(glob.glob("*{0}_*".format(year)))
os.chdir(curdir)

for gameID in gameIDs:
    # print "Parsing", gameID, "..."
    parseGame(gameID)

print "Final pitch list:", var.unique_pitch_types

pt.t.Write()
fout.Close()

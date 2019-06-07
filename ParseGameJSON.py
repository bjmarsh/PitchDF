import os,sys
import gzip, json, glob
from PitchTree import PitchTree
import ROOT

ignore_actions = ["Passed Ball", "Wild Pitch", "Caught Stealing 2B",
                  "Caught Stealing 3B", "Offensive Substitution", "Defensive Switch", 
                  "Game Advisory","Stolen Base 2B", "Stolen Base 3B", "Defensive Sub",
                  "Injury", "Runner Out", "Pickoff Error 1B", "Balk", "Pitch Challenge",
                  "Pickoff 1B", "Ejection", "Defensive Indiff", "Stolen Base Home",
                  "Pickoff Error 2B", "Other Advance", "Pickoff Caught Stealing 2B",
                  "Pickoff 2B", "Caught Stealing Home","Error", "Pickoff Caught Stealing Home",
                  "Pickoff 3B", "Pickoff Caught Stealing 3B"]

def processRunner(runner, game_state):
    pid = runner["details"]["runner"]["id"]
    start = runner["movement"]["start"]
    end = runner["movement"]["end"]
    if end not in ["1B","2B","3B","4B","score",None]:
        raise Exception("ERROR unknown runner end state: "+end)
    isScore = (end == "score")
    isOut = runner["movement"]["isOut"]

    base_map = {'1B':'first', '2B':'second', '3B':'third'}

    if start not in [None,"4B"] and game_state[base_map[start]] == pid:
        game_state[base_map[start]] = -1
    if end is not None and end not in ["score","4B"]:
        game_state[base_map[end]] = pid

    if isScore and game_state["home_score"] > -1:
        if game_state["half"] == "top":
            game_state["away_score"] += 1
        if game_state["half"] == "bottom":
            game_state["home_score"] += 1
    
    game_state["base_state"] = 0
    if game_state["first"] != -1:
        game_state["base_state"] |= (1<<0)
    if game_state["second"] != -1:
        game_state["base_state"] |= (1<<1)
    if game_state["third"] != -1:
        game_state["base_state"] |= (1<<2)

    if isOut:
        game_state['o'] += 1
    

def processPitch(pitch, game_state):
    pdict = {}

    pdict["des"] = pitch["details"]["description"]
    pdict["type"] = pitch["details"]["call"]["code"]
    if "type" in pitch["details"]:
        pdict["pitch_type"] = pitch["details"]["type"]["code"]
    elif "Automatic Ball" in pdict["des"]:
        pdict["pitch_type"] = "IN"
    else:
        pdict["pitch_type"] = "UN"

    pdict["x"] = pitch["pitchData"]["coordinates"].get("x",-9999)
    pdict["y"] = pitch["pitchData"]["coordinates"].get("y",-9999)
    pdict["px"] = pitch["pitchData"]["coordinates"].get("pX",-9999)
    pdict["pz"] = pitch["pitchData"]["coordinates"].get("pZ",-9999)
    pdict["pfx_x"] = pitch["pitchData"]["coordinates"].get("pfxX",-9999)
    pdict["pfx_z"] = pitch["pitchData"]["coordinates"].get("pfxZ",-9999)
    pdict["x0"] = pitch["pitchData"]["coordinates"].get("x0",-9999)
    pdict["y0"] = pitch["pitchData"]["coordinates"].get("y0",-9999)
    pdict["z0"] = pitch["pitchData"]["coordinates"].get("z0",-9999)
    pdict["vx0"] = pitch["pitchData"]["coordinates"].get("vX0",-9999)
    pdict["vy0"] = pitch["pitchData"]["coordinates"].get("vY0",-9999)
    pdict["vz0"] = pitch["pitchData"]["coordinates"].get("vZ0",-9999)
    pdict["ax"] = pitch["pitchData"]["coordinates"].get("aX",-9999)
    pdict["ay"] = pitch["pitchData"]["coordinates"].get("aY",-9999)
    pdict["az"] = pitch["pitchData"]["coordinates"].get("aZ",-9999)
    
    pdict["break_y"] = pitch["pitchData"]["breaks"].get("breakY",-9999)
    pdict["break_angle"] = pitch["pitchData"]["breaks"].get("breakAngle",-9999)
    # for some reason the break angle is abs() valued in the JSON... correct based on sign of ax
    if pdict["ax"] > 0 and pdict["break_angle"] > -9998:
        pdict["break_angle"] *= -1
    pdict["break_length"] = pitch["pitchData"]["breaks"].get("breakLength",-9999)
    pdict["spin_dir"] = pitch["pitchData"]["breaks"].get("spinDirection",-9999)
    pdict["spin_rate"] = pitch["pitchData"]["breaks"].get("spinRate",-9999)
    
    pdict["start_speed"] = pitch["pitchData"].get("startSpeed",-9999)
    pdict["end_speed"] = pitch["pitchData"].get("endSpeed",-9999)
    pdict["sz_top"] = pitch["pitchData"].get("strikeZoneTop",-9999)
    pdict["sz_bot"] = pitch["pitchData"].get("strikeZoneBottom",-9999)
    pdict["zone"] = pitch["pitchData"].get("zone",-9999)
    pdict["type_confidence"] = pitch["pitchData"].get("typeConfidence",-9999)

    if "hitData" in pitch:
        pdict["hit_x"] = pitch["hitData"]["coordinates"].get("coordX", -9999)
        pdict["hit_y"] = pitch["hitData"]["coordinates"].get("coordY", -9999)
        pdict["hit_launchAngle"] = pitch["hitData"].get("launchAngle", -9999)
        pdict["hit_launchSpeed"] = pitch["hitData"].get("launchSpeed", -9999)
        pdict["hit_totalDistance"] = pitch["hitData"].get("totalDistance", -9999)
        pdict["hit_location"] = pitch["hitData"].get("location", -9999)
        pdict["hit_trajectory"] = pitch["hitData"].get("trajectory", -9999)


    # print "Inning: {0}, Pitcher: {1}, Batter: {2}, Count: {3}-{4}, Outs: {5}, Pitch Type: {6}, Result: {7}".format(
    #     game_state["inning"], game_state['pitcher'], game_state['batter'], game_state['b'], 
    #     game_state['s'], game_state['o'], pdict["pitch_type"], pdict["type"])


    pt.Fill(game_state, pdict)

    game_state["pitch_counts"][game_state["pitcher"]] += 1
    game_state["cur_pc"] = game_state["pitch_counts"][game_state["pitcher"]]

    if pdict["type"] == "B":
        game_state['b'] += 1
    if pdict['type'] == "S" and (game_state['s'] < 2 or pdict["des"] != "Foul"):
        game_state['s'] += 1


    if pdict["des"] != "Hit By Pitch": 
        # sometimes the ball count is broken after a hit by pitch... 
        # shouldn't matter anyway as it's the last pitch of AB
        if game_state['b'] != pitch["count"]["balls"]:
            raise Exception("Balls mismatch!")
        if game_state['s'] != pitch["count"]["strikes"]:
            raise Exception("Strikes mismatch!")
    

def processAtBat(atbat, game_state):
        game_state["inning"] = atbat["about"]["inning"]
        # if the half-inning changes, reset the runners and outs
        if game_state["half"] != atbat["about"]["halfInning"]:
            game_state["half"] = atbat["about"]["halfInning"]
            game_state["first"] = -1
            game_state["second"] = -1
            game_state["third"] = -1
            game_state["base_state"] = 0
            game_state["o"] = 0

        game_state["b"] = 0
        game_state["s"] = 0
        game_state["batter" ] = atbat["matchup"]["batter"]["id"]
        game_state["pitcher" ] = atbat["matchup"]["pitcher"]["id"]
        game_state["BH"] = atbat["matchup"]["batSide"]["code"]
        game_state["PH"] = atbat["matchup"]["pitchHand"]["code"]

        game_state["home_score_after"] = atbat["result"]["homeScore"]
        game_state["away_score_after"] = atbat["result"]["awayScore"]

        # get event type, check if it's the first time we've seen it
        game_state["event"] = atbat["result"]["event"]
        if game_state["event"] not in unique_events:
            print "{0:25s}:{1}".format(game_state["event"], game_state["gid"])
            unique_events.append(game_state["event"])

        if game_state['pitcher'] not in game_state['pitch_counts']:
            game_state['pitch_counts'][game_state['pitcher']] = 0

        # each at-bat consists of a series of "events". Each event can be a "pitch" or an
        # "action" (e.g. stolen base).
        # "runners" can be concurrent with each event. Store as [event, [runners1,...]]
        events = []
        for event in atbat["playEvents"]:
            events.append([event, []])
        # for the "after at-bat", there can be runners but no official "event"
        events.append([None, []])
        # now insert the runner events at the appropriate spot
        for runner in atbat["runners"]:
            idx = runner["details"]["playIndex"]
            events[idx][1].append(runner)

        for event,runners in events:
            if event is not None:
                if event["type"] == "pitch":
                    processPitch(event, game_state)
                    pass
                elif event["type"] == "action":
                    evttype = event["details"]["event"]
                    if evttype == "Pitching Substitution":
                        game_state["pitcher"] = event["player"]["id"]
                        if game_state["pitcher"] not in game_state["pitch_counts"]:
                            game_state["pitch_counts"][game_state["pitcher"]] = 0
                    elif evttype == "Umpire Substitution":
                        des = event["details"]["description"]
                        if "HP" in des or "home plate" in des.lower():
                            game_state["umpire"] = event["umpire"]["id"]
                    elif evttype == "Pitcher Switch":
                        if "left-handed" in event["details"]["description"]:
                            game_state["PH"] = "L"
                        if "right-handed" in event["details"]["description"]:
                            game_state["PH"] = "R"
                    elif evttype in ignore_actions:
                        pass
                    else:
                        raise Exception("Unknown action: "+evttype)
                elif event["type"] not in ["pickoff"]:
                    raise Exception("Unknown event type "+event["type"])
                
            for runner in runners:
                processRunner(runner, game_state)

        if game_state["home_score_after"] != game_state["home_score"]:
            print game_state
            raise Exception("Home score mismatch!")
        if game_state["away_score_after"] != game_state["away_score"]:
            print game_state
            raise Exception("Away score mismatch!")

        game_state['o'] = atbat["count"]["outs"]
            

def parseGame(gd):
    g = gd["gameData"]
    print g["game"]["id"], g["game"]["pk"], g["datetime"]["dateTime"]
 
    game_state = {"batter":-1, "pitcher":-1, "inning":1, "half":"top", "b":0, "s":0, "o":0, 
                  "first":-1, "second":-1, "third":-1, "base_state":0, "home_score":0, "away_score":0, 
                  "home_score_after":0, "away_score_after":0, "umpire":-1, "BH":"R", "PH":"L", 
                  "event":"", "pitch_counts":{}, "cur_pc":0}

    game_state["gid"] = g["game"]["id"]
    game_state["year"] = int(g["datetime"]["dateTime"].split("-")[0])
    game_state["month"] = int(g["datetime"]["dateTime"].split("-")[1])
    game_state["day"] = int(g["datetime"]["dateTime"].split("-")[2][:2])
    game_state["away_team"] = g["teams"]["away"]["teamCode"]
    game_state["home_team"] = g["teams"]["away"]["teamCode"]
    game_state["DH"] = int(g["game"]["id"].split("-")[-1])

    ld = gd["liveData"]
    umps = ld["boxscore"]["officials"]
    for ump in umps:
        if "home" in ump["officialType"].lower():
            game_state["umpire"] = ump["official"]["id"]

    for play in ld["plays"]["allPlays"]:
        if play["result"]["type"] == "atBat":
            processAtBat(play, game_state)
        else:
            raise Exception("Unknown play type "+events["result"]["type"])


if __name__=="__main__":

    year = 2018
    gids = sorted([x.split("/")[-1] for x in glob.glob("/nfs-7/userdata/bemarsh/gamelogs/{0}/gid*".format(year))])
    # gids = ["gid_2018_04_18_chamlb_oakmlb_1"]

    fout = ROOT.TFile("pitches_{0}_fromJSON.root".format(year),"RECREATE")
    pt = PitchTree()
    pt.Init()

    unique_events = []                

    indir = "/nfs-7/userdata/bemarsh/gamelogs/{0}".format(year)
    for gid in gids:
        fname = os.path.join(indir,gid,"livefeed.json.gz")
        if not os.path.exists(fname):
            print "ERROR: gid {0} does not exist. Skipping.".format(gid)
            continue

        gd = None
        with gzip.open(fname, "rb") as fid:
            gd = json.loads(fid.read().decode("utf-8"))

        parseGame(gd)

    pt.Write(fout)

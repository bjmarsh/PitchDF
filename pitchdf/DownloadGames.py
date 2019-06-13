import os,sys
import requests
import json, gzip
import datetime as dt

def get_gamePks(startdate, enddate, teamId=None):
    # get list of gamePks between given dates
    # if teamId is not None, then only games involving a given team
    # a list of numerical teamIds can be found here (or at list at bottom of this file):
    # http://statsapi.mlb.com/api/v1/teams?sportId=1
    
    url = "http://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={0}&endDate={1}".format(startdate, enddate)
    if teamId:
        url += "&teamId={0}".format(teamId)

    r = requests.get(url=url)
    if r.status_code != 200:
        raise Exception(r.text)
    d = json.loads(r.text)
    pks = []
    for date in d["dates"]:
        for game in date["games"]:
            typ = game["gameType"]
            if typ not in ["R","P","D","L","W","F"]:
                continue
            pks.append(game["gamePk"])

    return pks

def download_single_game(gamePk, output_dir=None, use_gzip=True):
    # download the feed of a single game
    # if output_dir is not None, will write the file to disk at output_dir/game_id
    # returns a dict of the game data

    url = "http://statsapi.mlb.com/api/v1.1/game/{0}/feed/live".format(gamePk)

    r = requests.get(url=url)

    if r.status_code != 200:
        raise Exception(r.text)

    d = json.loads(r.text)

    gid = "gid_"+d["gameData"]["game"]["id"].replace("/","_").replace("-","_")

    if d["gameData"]["status"]["statusCode"] != "F":
        print "game not completed! skipping."
        return None

    typ = d["gameData"]["game"]["type"]
    if typ not in ["R","P","D","L","W","F"]:
        print "game type not recognized! (probably spring training or all-star game). Skipping"
        return None

    if output_dir:
        os.system("mkdir -p " + output_dir)
        outfile = "{0}/{1}.{2}".format(output_dir,gid, "json.gz" if use_gzip else "json")
        if use_gzip:
            with gzip.open(outfile, 'wb') as f:
                f.write(r.text.encode('utf-8'))
        else:
            with open(outfile, 'w') as f:
                f.write(r.text.encode('utf-8'))

    return d 


def download_gamePks(gamePks, output_dir=None, use_gzip=True):
    ds = []
    for gamePk in gamePks:
        ds.append(download_single_game(gamePk, output_dir, use_gzip))
    return ds


def download_dates(startdate, enddate, teamId=None, output_dir=None, use_gzip=True):
    pks = get_gamePks(startdate, enddate, teamId)
    return download_gamePks(pks, output_dir, use_gzip)


##############
## Team IDs ##
##############
# 108 Los Angeles Angels
# 109 Arizona Diamondbacks
# 110 Baltimore Orioles
# 111 Boston Red Sox
# 112 Chicago Cubs
# 113 Cincinnati Reds
# 114 Cleveland Indians
# 115 Colorado Rockies
# 116 Detroit Tigers
# 117 Houston Astros
# 118 Kansas City Royals
# 119 Los Angeles Dodgers
# 120 Washington Nationals
# 121 New York Mets
# 133 Oakland Athletics
# 134 Pittsburgh Pirates
# 135 San Diego Padres
# 136 Seattle Mariners
# 137 San Francisco Giants
# 138 St. Louis Cardinals
# 139 Tampa Bay Rays
# 140 Texas Rangers
# 141 Toronto Blue Jays
# 142 Minnesota Twins
# 143 Philadelphia Phillies
# 144 Atlanta Braves
# 145 Chicago White Sox
# 146 Miami Marlins
# 147 New York Yankees
# 158 Milwaukee Brewers

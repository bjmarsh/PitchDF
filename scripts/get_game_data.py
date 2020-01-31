import os,sys,glob,gzip,json
sys.path.append("..")
from pitchdf.GameJSONParser import GameJSONParser
from pitchdf.OutputROOT import OutputROOT
from pitchdf.OutputDF import OutputDF, OutputCSV
from pitchdf.GameState import GameState
# from pitchdf.DownloadGames import *


year = 2018

gids = sorted([x.split("/")[-1] for x in glob.glob("/nfs-7/userdata/{0}/gamelogs/{1}/gid*".format(os.environ["USER"],year))])
# gids = ["gid_2017_06_29_nyamlb_chamlb_1"]

# output = OutputROOT("../output_fromJSON/pitches_{0}.root".format(year))
output = OutputDF("../output_fromJSON/pitches_{0}.pkl".format(year))
parser = GameJSONParser(output)

indir = "/nfs-7/userdata/{0}/gamelogs/{1}".format(os.environ["USER"],year)
for gid in gids:
    # if "2019_1" not in gid:
    #     continue
    fname = os.path.join(indir,gid,"livefeed.json.gz")
    if not os.path.exists(fname):
        print "ERROR: gid {0} does not exist. Skipping.".format(gid)
        continue

    gd = None
    with gzip.open(fname, "rb") as fid:
        gd = json.loads(fid.read().decode("utf-8"))

        parser.parse_game(gd)

output.write()

import os,sys
sys.path.append("..")
import gzip
import json
import glob
from tqdm import tqdm

if os.path.exists("personIds.json"):
    ids = json.load(open("personIds.json",'r'))
else:
    ids = {}

for year in range(2010,2020):
    print year
    for dname in tqdm(glob.glob("/nfs-7/userdata/{0}/gamelogs/{1}/*".format(os.environ["USER"],year))):
        fname = os.path.join(dname,"livefeed.json.gz")
        if not os.path.exists(fname):
            continue
        with gzip.open(fname, 'rb') as f:
            d = json.loads(f.read())
            
        for p in d["liveData"]["boxscore"]["officials"]:
            first, last = p["official"]["fullName"].rsplit(None, 1)
            ids[p["official"]["id"]] = {
                "firstName" : first,
                "lastName" : last,
                "position" : "Umpire"
                }
        for k,p in d["gameData"]["players"].items():
            ids[p["id"]] = {
                "firstName" : p["useName"],
                "lastName" : p["lastName"],
                "position" : p["primaryPosition"]["abbreviation"]
                }

json.dump(ids, open("personIds.json",'w'), indent=4, sort_keys=True)

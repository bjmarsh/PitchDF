import os,sys
sys.path.append("..")
import gzip
import json
import glob

year = 2015
types = []
for dname in glob.glob("/nfs-7/userdata/{0}/gamelogs/{1}/*".format(os.environ["USER"],year)):
    fname = os.path.join(dname,"livefeed.json.gz")
    if not os.path.exists(fname):
        continue
    with gzip.open(fname, 'rb') as f:
        d = json.loads(f.read())

    for play in d["liveData"]["plays"]["allPlays"]:
        for event in play["playEvents"]:
            if not event["type"] == "pitch":
                continue
            if "type" in event["details"]:
                code = event["details"]["type"]["code"]
                des = event["details"]["type"]["description"]
                x = (code,des)
                if x not in types:
                    print x
                    types.append((code,des))


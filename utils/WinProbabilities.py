import cPickle as pickle
import json
import numpy as np
from Histogram import *

win_probs = {}
count_outcomes = {}
run_exp = {}

def LoadWinProbFile(fname, year_group=(2014,2019)):
    global win_probs
    with open(fname, 'rb') as fid:
        win_probs = pickle.load(fid)[year_group]

def LoadCountOutcomeFile(fname, year_group=(2014,2019)):
    global count_outcomes
    ys = str(year_group[0]) if len(year_group)==1 else "{0}-{1}".format(*year_group)
    with open(fname) as fid:
        count_outcomes = json.load(fid)[ys]

def LoadRunExpectancies(fname, year_group=(2014,2019)):
    global run_exp
    with open(fname, 'rb') as fid:
        run_exp = pickle.load(fid)[year_group]
    

def GetHomeWinProb(inning, half, base_state, outs, ascore, hscore):
    sdiff = hscore-ascore
    h = win_probs[(min(9,inning),half,base_state,outs)]["wprob"]
    return h.GetContents(h.FindBin(sdiff))


def GetCountBasedWinProb(inning, half, base_state, outs, ascore, hscore, balls, strikes):
    sdiff = hscore-ascore
    co = count_outcomes["{0}-{1}".format(balls,strikes)]
    h_wp = win_probs[(min(9,inning+(1 if half=="bottom" else 0)), "bottom" if half=="top" else "top", 0, 0)]["wprob"]

    iw_corr = 1.0
    if "Intent Walk" in co and ("Intent Walk", base_state, outs) not in run_exp:
        iw_corr *= 1.0 / (1.0 - co["Intent Walk"])

    prob = 0.0
    for outcome in co:
        key = (outcome, base_state, outs)
        if key not in run_exp:
            continue
        h_runexp = run_exp[key]
        
        for iruns in range(h_runexp.nbins):
            pruns = h_runexp.GetContents(iruns+1)
            margin = (hscore-ascore) + (1 if half=="bottom" else -1) * iruns
            if inning>=9 and half=="bottom":
                prob += co[outcome] * pruns * (1.0*(margin>0) + 0.5*(margin==0))
            else:
                prob += co[outcome] * pruns * h_wp.GetContents(h_wp.FindBin(margin))

    return prob*iw_corr

if __name__=="__main__":
    
    LoadWinProbFile("../data/win_probabilities.pkl")
    LoadCountOutcomeFile("../data/count_outcomes.json")
    LoadRunExpectancies("../data/run_expectancies_by_event.pkl")

    # from itertools import product
    # from tqdm import tqdm
    # diffs = {}
    # for inning, half, base_state, outs, sdiff, balls, strikes in tqdm(product(range(1,10), ('top','bottom'), range(8), range(3), range(-3,4), range(4), range(3))):
    #     ascore = 10
    #     hscore = ascore + sdiff
        
    #     wp = GetHomeWinProb(inning, half, base_state, outs, ascore, hscore)
    #     cb = GetCountBasedWinProb(inning, half, base_state, outs, ascore, hscore, balls, strikes)
    #     diffs[(inning, half, base_state, outs, sdiff, balls, strikes)] = (cb-wp, wp, cb)

    # states = sorted(diffs.keys(), key=lambda x:diffs[x][0], reverse=True)
    # for s in states[:10]:
    #     print "{0:+.4f} {1:.4f} {2:.4f}".format(*diffs[s]), s
    # print "-----"
    # for s in states[-1:-11:-1]:
    #     print "{0:+.4f} {1:.4f} {2:.4f}".format(*diffs[s]), s

    for b in range(4):
        for s in range(3):
            print "{0}-{1}  {2:.3f}".format(b,s, GetCountBasedWinProb(9, 'bottom', 7, 2, 5, 4, b, s))



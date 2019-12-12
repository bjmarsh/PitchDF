# PitchDF
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bjmarsh/PitchDF/master?filepath=notebooks)

Retrieve PitchFX/Statcast data from MLB's stats-api and store in pandas dataframes or ROOT trees.

### Downloading game data
Download all game JSON's from MLB's database, for games between given dates, and store in a local directory:
```python
import datetime as dt
import pitchdf.DownloadGames as dl
dl.download_dates(dt.date(2019, 3, 20), dt.date(2019,11,1), output_dir="./gamedata")
```
Get the game ID's (referred to by MLB as gamePk's) for a given team between certain dates:
```python
pks = dl.get_gamePks(dt.date(2019, 4, 16), dt.date(2019, 4, 23), teamId=112)
# teamId=None will give all teams
# teamId's are listed at the bottom of pitchdf/DownloadGames.py
```
Return a `dict` corresponding to the JSON for a single game:
```python
gamedict = dl.download_single_game(pks[0], output_dir=None)
# if output_dir is not None, it will also write the json to a file for later use
```

### Parse JSON into a dataframe
```python
import gzip
from pitchdf.GameJSONParser import GameJSONParser
from pitchdf.OutputDF import OutputDF

output = OutputDF("output_dfs/pitches.pkl")
parser = GameJSONParser(output)

# let's say we have a collection of gzipped game jsons (downloaded using examples above)
# "game_files" is a list containing all of their filenames
game_files = [ ... ]

for fname in game_files:
    with gzip.open(fname, "rb") as fid:
        gd = json.loads(fid.read().decode("utf-8"))
        parser.parse_game(gd)

output.write() #by default gzips the pickle file

# now the dataframe is stored in a (gzipped) pickled file output_dfs/pitches.pkl.gz
# load the data frame with

import pandas as pd
df = pd.read_pickle("output_dfs/pitches.pkl.gz", compression="gzip")

```

### Analyzing the data
Now we have a dataframe containing one row for every pitch in the games we parsed!

See [this file](docs/df_columns.md) for a description of the column names.

See the binder link above (or just the `notebooks` directory) to browse a few sample notebooks with some basic analysis.

# PitchDF
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bjmarsh/PitchDF/master)

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

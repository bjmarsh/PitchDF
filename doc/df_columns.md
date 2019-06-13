### List of column definitions

Note on coordinate system: PITCHf/x uses Cartesian coordinate system centered on center of front of plate at ground-level. x-axis points towards LH batter's box, y-axis towards the pitchers mound, and z-axis vertically upwards

All pitch attributes get a value of -9999 if they aren't specified in the game data (stadium didn't have tracking devices, system failed to track pitch, etc.), unless specified otherwise. So it is usually a good idea to skim on e.g. `px > -999` before looking at those fields

Some definitions of PITCHf/x fields taken from Mike Fast's post [here](https://fastballs.wordpress.com/2007/08/02/glossary-of-the-gameday-pitch-fields/).


| name | dtype | notes |
|------|-------|-------|
|`date`                | `datetime64[ns]` | scheduled game start time|
|`gamePk`              |         `uint32` | integer game identifier used by MLB stats-api|
|`DH`                  |          `uint8` | 1 for most games; 2 if the 2nd game of a double-header|
|`away_team`           |       `category` | 3-letter identifier for away team (`teamCode` [found here](http://statsapi.mlb.com/api/v1/teams?sportId=1))|
|`home_team`           |       `category` | 3-letter identifier for home team (see above)|
|`inning`              |          `uint8` | inning number|
|`half`                |       `category` | `"top"` or `"bottom"`|
|`balls`               |          `uint8` | number of balls before current pitch|
|`strikes`             |          `uint8` | number of strikes before current pitch|
|`outs`                |          `uint8` | number of outs before current pitch|
|`base_state`          |          `uint8` | 0-7, three binary bits representing third,second,first. e.g. 110 = 6 means runners on second and third|
|`batter`              |         `uint32` | integer `playerId` used by MLB stats-api|
|`pitcher`             |         `uint32` | integer `playerId` used by MLB stats-api|
|`BH`                  |       `category` | handedness of batter, "L" or "R"|
|`PH`                  |       `category` | handedness of pitcher, "L" or "R"|
|`pitch_count`         |          `uint8` | game pitch count of current pitcher|
|`home_score`          |          `uint8` | home score before current pitch|
|`away_score`          |          `uint8` | away score before current pitch|
|`home_score_afterAB`  |          `uint8` | home score after conclusion of current at-bat|
|`away_score_afterAB`  |          `uint8` | away score after conclusion of current at-bat|
|`home_score_afterInn` |          `uint8` | home score after conclusion of current half-inning|
|`away_score_afterInn` |          `uint8` | away score after conclusion of current half-inning|
|`runner_first`        |          `int32` | integer `playerId` of runner on first; -1 if first is empty|
|`runner_second`       |          `int32` | integer `playerId` of runner on second; -1 if second is empty|
|`runner_third`        |          `int32` | integer `playerId` of runner on third; -1 if third is empty|
|`umpire`              |          `int32` | integer `playerId` of HP umpire|
|`is_last_pitch`       |           `bool` | is this the last pitch of an at-bat? (strikeout, walk, HBP, or in-play. Note this is False if at-bat not completed (e.g. if inning ends on caught stealing))|
|`event`               |       `category` | string indicating outcome of at-bat (e.g. "Single","Home Run","Caught Stealing 2B")|
|`des`                 |       `category` | description of pitch outcome. One of `['Automatic Ball', 'Ball', 'Ball In Dirt', 'Called Strike', 'Foul', 'Foul Bunt', 'Foul Tip', 'Hit By Pitch', 'In play, no out', 'In play, out(s)', 'In play, run(s)', 'Missed Bunt', 'Pitchout', 'Swinging Strike',  'Swinging Strike (Blocked)']`|
|`strike_type`         |       `category` | `B`: ball, `C`: called strike, `S`: swinging strike, `F`: foul ball, `FT`: foul tip, `FB`: foul bunt, `MB`: missed bunt, `X`: in play|
|`pitch_type`          |       `category` | 2-letter description of the type of pitch (4-seam fastball, slider, etc.). Including but potentially not limited to `['UN', 'SI', 'SL', 'FF', 'FC', 'CU', 'CH', 'FT', 'FS', 'KC','EP', 'FO', 'PO', 'SC', 'KN', 'AB', 'IN', 'FA']`. Note `'UN'` means "unknown"|
|`x`                   |        `float32` | x-coot given|
|`spin_dir`            |        `float32` | ball spin direction. Need to investigate what coordinate system this is in|
|`spin_rate`           |        `float32` | ball spin rate. Given in rpm??|
|`hit_x`               |        `float32` | Statcast x location of hit. Note NOT the same coordinate system as for PITCHf/x. Home plate seems to be centered on something random, need to investigate|
|`hit_y`               |        `float32` | Statcast y location of hit, see above.|
|`hit_launchAngle`     |        `float32` | Statcast launch angle of hit trajectory. Given in degrees, measured with respect to ground|
|`hit_launchSpeed`     |        `float32` | Statcast launch speed (exit velocity) of hit, given in MPH|
|`hit_totalDistance`   |        `float32` | Statcast-measured distance of hit, given in feet|
|`hit_location`        |           `int8` | integer location encoding region of field where hit was; need to investigate mapping|
|`hit_trajectory`      |       `category` | one of `['NONE', 'U', 'bunt_grounder', 'bunt_line_drive', 'bunt_popup', 'fly_ball', 'ground_ball', 'line_drive', 'popup']`. `'NONE'` is used for pitches that weren't hit into play|
|`hit_hardness`        |       `category` | one of `['NONE', 'soft', 'medium', 'hard']`|

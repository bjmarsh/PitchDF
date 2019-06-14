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
|`x`                   |        `float32` | x-coordinate of pitch in old gameday system. Out-dated, do not use.|
|`y`                   |        `float32` | y-coordinate of pitch in old gameday system. Out-dated, do not use.|
|`px`                  |        `float32` | horizontal location of pitch as it crosses plate. Measured in feet from center of plate|
|`pz`                  |        `float32` | vertical location of pitch as it crosses plate. Measured in feet from ground. Can be negative if ball hits ground before crossing plate.|
|`pfx_x`               |        `float32` | the horizontal movement, in inches, of the pitch between the release point and home plate, as compared to a theoretical pitch thrown at the same speed with no spin-induced movement.|
|`pfx_z`               |        `float32` | the vertical movement, in inches, of the pitch between the release point and home plate, as compared to a theoretical pitch thrown at the same speed with no spin-induced movement.|
|`start_speed`         |        `float32` | the pitch speed, in miles per hour and in three dimensions, measured at the initial point, `y0`. Of the two speeds, this one is closer to the speed measured by a radar gun and what we are familiar with for a pitcher's velocity|
|`end_speed`           |        `float32` | the pitch speed measured as it crossed the front of home plate|
|`sz_top`              |        `float32` | the distance in feet from the ground to the top of the current batter's "rulebook" strike zone|
|`sz_bot`              |        `float32` | the distance in feet from the ground to the bottom of the current batter's "rulebook" strike zone|
|`x0`                  |        `float32` | the left/right distance, in feet, of the pitch, measured at the initial point.|
|`y0`                  |        `float32` | the distance in feet from home plate where the PITCHf/x system is set to measure the initial parameters. Seems to be set at a constant 50, at least recently|
|`z0`                  |        `float32` | the height, in feet, of the pitch, measured at the initial point.|
|`vx0`                 |        `float32` | the x-component of velocity (ft/s) measured at initial point|
|`vy0`                 |        `float32` | the y-component of velocity (ft/s) measured at initial point|
|`vz0`                 |        `float32` | the z-component of velocity (ft/s) measured at initial point|
|`ax`                  |        `float32` | the x-component of acceleration (ft/s^2) measured at initial point|
|`ay`                  |        `float32` | the y-component of acceleration (ft/s^2) measured at initial point|
|`az`                  |        `float32` | the z-component of acceleration (ft/s^2) measured at initial point|
|`break_y`             |        `float32` | the distance in feet from home plate to the point in the pitch trajectory where the pitch achieved its greatest deviation from the straight line path between the release point and the front of home plate|
|`break_angle`         |        `float32` | the angle, in degrees, from vertical to the straight line path from the release point to where the pitch crossed the front of home plate, as seen from the catcher's/umpire's perspective|
|`break_length`        |        `float32` | the greatest distance, in inches, between the trajectory of the pitch at any point between the release point and the front of home plate, and the straight line path from the release point to the front of home plate|
|`type_conf`           |        `float32` | the "confidence" of MLB's pitch-classification algorithm that it got `pitch_type` correct|
|`zone`                |           `int8` | 1-9 are the 9 zones within strikezone, starting at upper left and moving left-to-right, top-to-bottom. 11 is out-of-zone upper-left, 12 is upper-right, 13 is lower-left, 14 is lower-right. Set to -1 if not given|
|`nasty`               |          `int16` | MLB's "nastiness" rating for each pitch. Don't ask how it's calculated. Seems to be an integer between 0 and 100. Set to -1 if not given|
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

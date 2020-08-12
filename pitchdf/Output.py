class Output:
    def __init__(self):
        print "Shouldn't call this! Use one of the derived classes"

    def add_entry(self, game_state, pitch):
        pass

    _unique_pitch_types = [
        'UN', 'SI', 'SL', 'FF', 'FC', 'CU', 'CH', 'FT', 'FS', 'KC', 
        'EP', 'FO', 'PO', 'SC', 'KN', 'AB', 'IN', 'FA'
        ]

    @staticmethod
    def get_strike_type(pitch):
        st = pitch.type
        if st=='V':
            st = 'I' # Automatic Ball
        elif st in ['B', '*B', 'H', 'P']:
            st = 'B'
        elif 'In play' in pitch.des:
            st = 'X'
        else:
            if 'Called' in pitch.des:
                st = 'C'
            elif 'Swinging' in pitch.des:
                st = 'S'
            elif 'Foul Tip' in pitch.des:
                st = 'FT'
            elif 'Foul Bunt' in pitch.des:
                st = 'FB'
            elif 'Foul' in pitch.des:
                st = 'F'
            elif 'Missed Bunt' in pitch.des:
                st = 'MB'
            else:
                raise Exception("Unknown strike description: "+pitch.des)
        return st
        
    @staticmethod
    def is_last_pitch(game_state, pitch):
        if pitch.type=='X' or \
                (pitch.type=='B' and game_state.b==3) or \
                (Output.get_strike_type(pitch) in ['S','C','FB','FT','MB'] and game_state.s==2) or \
                pitch.des=="Hit By Pitch":
            return True
        return False
        

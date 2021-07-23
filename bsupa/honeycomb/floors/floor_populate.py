#
#
#
#
'''
    This is to update and populate database values
    ...
'''

import floor

class Floor_populate:
    '''Add Doc String Here.'''  # TODO: do this

    def __init__(self, floor_name, sections):
        ''' Will take value from live_data server (daily values will be fed
        back in to training database Add Doc String here.
        '''  # TODO: do this
        floors = floor.Floor()
        floors.floor_name = floor_name
        floors.sections = sections

    def populate(self):
        '''This will be called to update/create cell values in database.'''
        # TODO: do this
        pass

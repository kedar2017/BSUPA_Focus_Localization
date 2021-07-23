#
#
#
#
'''
    This is to update and populate database values
    ...
'''

import section

class section_populate:
    '''Add Doc String Here.'''  # TODO: do this

    def __init__(self, cells, section_name):
        ''' Will take value from live_data server (daily values will be fed
        back in to training database Add Doc String here.
        '''  # TODO: do this
        sections = section.Section()
        sections.cells = cells
        sections.section_name = section_name

    def populate(self):
        '''This will be called to update/create cell values in database.'''
        # TODO: do this
        pass

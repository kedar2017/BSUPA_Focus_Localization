#  License
#  Gota Count
#  @author(s)
#
from copy import copy

class Section():
    '''Add Doc String Here.'''  # TODO: DO this!


    def __init__(self, section_name='section'):
        '''Add Doc String Here.'''  # TODO: DO this!
        self.section_name = section_name
        self.cells = []

    def add(self, cell_obj):
    	'''
    	Adds Cell instances into a list
	    '''
    	self.cells.append(copy(cell_obj))

    def add_cell_list(self, cell_list):
        '''
        Add a complete cell_list to a section
        '''
        self.cells = cell_list[:]

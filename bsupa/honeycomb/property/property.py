'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

from blip.honeycomb.floors import floor

class Mall:
    '''Add Doc String Here.'''  # TODO: DO this!


    def __init__(mall_name):
        '''Add Doc String Here.'''  # TODO: DO this!

        self.mall_name = mall_name
        self.floors = []

    def populate_mall(self, number_floors, floor_names=None):
    	'''
    	Populates self.floors with blank Floor instances
	    number_floor is number of floors mapped in that mall
    	'''

	if floor_names == None:
		self.floor_names = [ str(i+1) for i in range(number_floors) ]
	else:
		self.floor_names = floor_names

        # Length of self.floors = number of floors automatically
        self.floors = [ floor.Floor(self.floor_name) for self.floor_name in self.floor_names]

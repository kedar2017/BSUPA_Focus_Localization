'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''


'''
    tcell is training cell class which is used in analytics tools
    for calculation in spatial variation
'''

from copy import copy
from collections import OrderedDict

class APCell:
    def __init__(self, bssid_name):
        '''
        APCell contains bssid-name, list_of_cell_coordinates, 
        '''       
        self.bssid_name=bssid_name

        # length of self.list_coordinates and self.list_mu SHOULD be equal 
        self.list_coordinates=[] #Will contain tuple (pos_x, pos_y)
        self.list_mu = [] # will contain mu in order with coordinates in list_coordinates
        self.list_sigma = [] # will contain sigmas in order like in list_mu
    def return_position_and_mu(self):
        '''
        returns dictionary of format:
        { (x1,y1): mu1, (x2,y2):mu2 .. }
        '''
        self.position_mu = OrderedDict({ coordinate : self.list_mu[self.list_coordinates.index(coordinate)]  for coordinate in self.list_coordinates })
        return self.position_mu

    def return_position_and_sigma(self):
        '''
        returns dictionary of format:
        { (x1,y1): sigma1, (x2,y2):sigma2 .. }
        '''
        self.position_sigma = OrderedDict({ coordinate : self.list_sigma[self.list_coordinates.index(coordinate)]  for coordinate in self.list_coordinates })
        return self.position_sigma

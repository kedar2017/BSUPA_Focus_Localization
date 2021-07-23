'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

'''
    Add doc string desc
    add doc string desc
'''

from copy import copy
class LiveCell:
    def __init__(self):
        '''
        Add Doc String Here.
        '''
        #TODO:
        # Predictions of point_x and point_y are lists so as to maintain
        # beliefs
        self.point_x = []
        self.point_y = []

        # Predicted Section
        self.section = None

        # NOTE floor and mall data will be added on the FLY

        self.mob_hash = None
        self.timestamp = None
        # Ssid Class definition
        '''
        Add Doc String Here.
        '''
        #TODO: do this
        class Ssid:
            def __init__(self):
                '''
                Add doc string here.
                '''
                #TODO: do this
                self.ssid_name = ''
                self.signal_strength = []

            def clear(self):
                self.__init__()

        # Create ssid_objects
        self.ssid_obj = Ssid()
        self.ssids = []  # Will contain objects of Ssid type

    def add_ssids(self):
        self.ssids.append(copy(self.ssid_obj))
        self.ssid_obj.clear()

    def return_ap_names_and_values(self):
        '''
        Returns a list of SSID names, and list of list of SSID values
        '''
        return [ [ssid_obj.ssid_name for ssid_obj in self.ssids], [ssid_obj.signal_strength for ssid_obj in self.ssids] ]

    def return_ap_data(self):
        '''
        Returns a dictionary of { ssid_name : list_of_ssid_values,  .. }
        '''
        return { ssid_obj.ssid_name : ssid_obj.signal_strength for ssid_obj in self.ssids }

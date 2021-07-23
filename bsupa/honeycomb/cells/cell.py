'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''


'''
    Cell Definition Object
'''

from copy import copy, deepcopy
from collections import OrderedDict

class Cell:
    def __init__(self):
        '''
        Add Doc String Here.
        '''
        #TODO: do this
        self.x = 0
        self.y = 0

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
                self.bssid           = ''
                self.frequency       = 0
                self.signal_strength = []

            def add_strength(self, strength):
                self.signal_strength = strength[:]

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
        return [ [ssid_obj.bssid for ssid_obj in self.ssids], [ssid_obj.signal_strength for ssid_obj in self.ssids] ]

    def return_ap_data(self):
        '''
        Returns a dictionary of { ssid_name : list_of_ssid_values,  .. }
        '''
        return OrderedDict({ ssid_obj.bssid : ssid_obj.signal_strength for ssid_obj in self.ssids })

    def return_str_data(self):
        '''
        Returns data in this cell as a formatted string
        '''
        # TODO Later format the data to fit in template string
        template_string =  '{"f":"t","g":[18.9293738,72.8331877],"m":"Motorola XT1068","t":1410831870794,"h":"3c37db5846","i":{"00:25:5e:2f:0f:bc2462":-70,"b4:75:0e:14:d6:4e2462":-37,"ec:43:f6:3e:0f:6c2412":-45,"80:a1:d7:27:6a:d02417":-91,"80:56:f2:37:9d:f82437":-64}}'
        return str(self.return_ap_data()) + "X:%d Y:%d" %(self.x, self.y)

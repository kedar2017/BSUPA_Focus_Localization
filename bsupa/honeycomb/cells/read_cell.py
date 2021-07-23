from copy import copy, deepcopy
from collections import OrderedDict

class ReadCell:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.floor = 0
        self.section= 'section'
        self.prop  = 'property'
        self.shop  = 'shop'

        class Rssi:
            def __init__(self):

                self.mean = 0.0
                self.std  = 0.0
                self.address = ''

            def add_strength(self, mean):
                self.mean = strength[:]
            def clear(self):
                self.__init__()

        self.rssi_obj = Rssi()
        self.rssids   = [] # Contains objects if Rssi type

    def add_rssi(self):
        self.rssids.append(copy(self.rssi_obj))
        self.rssi_obj.clear()

    def return_data(self):
        return OrderedDict({ rssi_obj.address : rssi_obj.mean for rssi_obj in self.rssids})


    def return_str_data(self):
        temp_string = '{"shop":"yo", "floor":0, "section":"yo", "property":"yo", "x": 0.0, "y": 0.0, "address":"yo", "signal_strength":"yo"}'
        print str(self.return_data()) + "X:%d Y:%d" %(self.x, self.y)
        return str(self.return_data()) + "X:%d Y:%d" %(self.x, self.y)

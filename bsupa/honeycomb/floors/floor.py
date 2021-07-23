'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

from blip.honeycomb.sections import section
from copy import copy

class Floor:
    '''Add Doc String Here.'''  # TODO: DO this!


    def __init__(self, floor_name):
        '''Initializes Floor instance.'''  # TODO: Correct method of passing section_name
        self.floor_name = floor_name
        self.sections = []

    def add(self, section_obj):
        '''
        Add Section object to self.sections list
        '''
        self.sections.append(copy(section_obj))
        # Clear the object values
        section_obj.__init__()


    def populate_floor(self, number_sections, section_names=None):
        '''If a section_names list is given then use it;
        if section_names is None, generate it.
        '''
        if section_names == None:
            # Get names like sec1, sec2 ..
            self.section_names = [ str('sec'+ str(i+1)) for i in range(number_sections)]
        else:
            self.section_names = section_names

        # Length of self.sections = number of sections automatically
        self.sections = [ section.Section(section_name) for section_name in self.section_names ]


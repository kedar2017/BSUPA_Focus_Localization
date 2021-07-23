'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

import traceback

from cells import cell
from floors import floor
from sections import section


from copy import copy,deepcopy
from uuid import uuid1

from blip.database.dbxactions.training_data.dbO import TrainingDbO

from blip.common.debugging import line_trace

## Will do class_instances to db interaction
class honeycomb:
    '''
    Honeycomb reads database (if not blank), and creates python objects if not created
    Also updates the database with LiveCell object information
    '''

    def __init__(self, keyspace_name, session_obj):

        '''
        Objects init in blip.py
        Honeycomb uses objects returned by blip.py

        Honeycomb won't init mapping database/tables | Just the live database/tables
        '''

        type_name_dict = table_type_name_dict = {
                                "ssid"     : "ssid_t",
                                "cell"     : "cell_t",
                                "section"  : "section_t",
                                "floor"    : "floor_t",
                                "property" : "property_t" }

        # Create Training Data dbO
        self.training_dbO = TrainingDbO('blip/database/dbxactions/training_data/training_schema.json', keyspace_name, type_name_dict, session_obj)

        self.session_obj   = session_obj
        self.keyspace_name = keyspace_name

        # TODO
        # Init Live Tables if not already


    def getAllCells(self):
        """
        Returns all cell data in Cell Table

        getCells method to get cells by their cids
        """
        # Create new object
        self.cell = cell.Cell()
        list_cells = []

        data = self.training_dbO.readTable('cell')

        # Check if data is not False(Null)
        if data:
            i = 0
            ### Populating Cell Object
            for cell_data in data:
                self.cell.x           = cell_data.x
                self.cell.y           = cell_data.y
                self.cell.raw_section = cell_data.raw_section

                list_ssid_ids = cell_data.ssid_ids
                for ssid_id in list_ssid_ids:
                    ssid_data = self.training_dbO.readTableWithCondition('ssid', column="*", condition=[ssid_id])

                    if ssid_data != []:
                        ap = ssid_data[0]
                        self.cell.ssid_obj.bssid          = ap.bssid
                        self.cell.ssid_obj.frequency      = ap.frequency
                        self.cell.ssid_obj.signal_strengh = self.cell.ssid_obj.add_strength(ap.signal_strength)

                        self.cell.add_ssids()

                # Add copy of cell object to list_cells
                list_cells.append(copy(self.cell))
                # Call the init and clear existing values
                self.cell.__init__()

            return list_cells

        else:
            print "Cell couldn't be read", line_trace()


    def populate_sections(self, keyspace_name, section_table_name, floor_name, cell_list, session_obj ):
        '''
        Takes cell_list and populates those in sections
        Returns Floor Object
        '''

        # Init Floor Object
        self.floor = floor.Floor(floor_name)
        self.section = section.Section()

        # Query returns section tuples
        self.query_return = self.training_dbO.read_table(table_type='section', keyspace_name=keyspace_name, table_name=section_table_name, session_obj=session_obj, ssid_id=None, query="*")

        if self.query_return:
            for self.section_info in self.query_return:

                # Assign values to self.section
                self.section.section_name = self.section_info.name

                # Add all cells to that section
                for self.unassigned_cell in cell_list:
                    for self.assigned_cell_uuid in self.section_info.cell_ids:

                            # NOTE Inherently uses copy method
                        self.section.add(self.unassigned_cell)

                # NOTE Inherently copies the object and clears section_obj
                self.floor.add(self.section)

            return self.floor

        else:
            print "Couldn't read sections"
            return False

    def is_unique(self, msg_dict, keyspace_name, session_obj, table_name='cell_temp'):
        '''
        Is the msg_dict unique (i.e. is PRIMARY VALUES different)
        If yes, return True else False
        Either ways create a Cell obj after querying
        '''
        try:
            # Splice msg_dict['l'] and extract section_name
            self.queryCell = self.temp_training_dbO.read_table('each_cell', keyspace_name, table_name, session_obj, ssid_id=None, mallname=msg_dict['M'], floornumber=msg_dict['F'], raw_section=msg_dict['l'].split(";")[0], x=msg_dict['x'][0], y=msg_dict['x'][1]) 
        except:
            traceback.print_exc()

        if len(self.queryCell) == 0:
            return True
        else:
            return False

    # XXX Do we need this?
    def populate_floors(self, keyspace_name, table_name):
        # should take populate_sections return and pull values from floor table
        # should return floor names, number of floors
        pass
    def populate_malls(self, keyspace_name, table_name):
        # self.mall = training_dbO.read_table(query="*", 'mall', keyspace_name, table_name, session_obj)
        pass

    ### METHOD FOR LIVE DATABASE MANIPULATIONS

    def live_init(self, live_keyspace, session_obj):
        '''
        Init live_cell database
        '''
        table_name_list = ['lss_ssid_t', 'lc_cell_t']
        # NOTE Can you reuse the function below from __init__

        # Create Tables if not present in Cassandra
        if keyspace_exists(live_keyspace, session_obj) and table_exists(live_keyspace, session_obj, table_name_list, for_module='live'):
            print 'Live keyspace and all Live tables exists'
        else:
            # Create Keyspace
            CreateKeyspace(live_keyspace, session_obj, self.ld_dbO)
            # Create Tables
            CreateLiveTable(live_keyspace, session_obj)
            # Update cell values from training_data_path

    ### METHOD FOR TEMPORARY DATABASE MANIPULATIONS

    def temporary_init(self, keyspace_name, table_name, session_obj):
        '''
        Initialize temporary database used by trainer script
        The schema and everything(dbO) will be same as training_data
        except CreateTables function
        '''
        # Create Temporary Training Tables if not present
        table_name_list = ['c_cell_temp', 'f_floor_temp', 'se_section_temp', 'ss_ssid_temp']

        if keyspace_exists(keyspace_name, session_obj) and table_exists(keyspace_name, session_obj, table_name_list, for_module='temp_training') :
            print 'Temp Training Keyspace and all tables exists'
        else:
            # If honeycomb is called by blip.py then Use this in init
            # XXX Why should this be in honeycomb_init ?? Make a new function like temporary_init
            CreateKeyspace(keyspace_name, session_obj, self.temp_training_dbO)
            # Create Tables
            CreateTemporaryTables(keyspace_name, session_obj)

    def update_db(self, keyspace_name, session_obj, cellObj, type_db = "live", cell_list=None):
        '''
        Write contents of live_cell and its prediction back to database
        cellObj is instance of LiveCell if type_db is live
        cellObj is instance of temp_dict if type_db is temp
        '''

        if type_db == 'live':
            if PopulateLiveTable(keyspace_name, session_obj, cellObj):
                print "Updated live_cell database"
            else:
                print "Error writing to live database"

        elif type_db == "temp_training":
            if PopulateTemporaryTables(keyspace_name, session_obj, cellObj):
                print "Updated training_temp database"
            else:
                print "Error writing to Temp training database"

        elif type_db == "training":
            if PopulateTrainingTables(keyspace_name, session_obj, cell_list):
                print "Updated Training database"
            else:
                print "Error writing to Training database"


        else:
            print "Incorrect type_db | type_db should either be \"live\" or \"temp_training\""


    def update_record(self, keyspace_name, session_obj, set_column, set_value, where_column, where_value, record_type="ssid"):
        '''
        Updates record of Table (Using update CQLStatment from dbO)
        Table name is set to by ssid_temp
        '''
        if record_type == "ssid":
            # NOTE LOCAL table_name
            self.ssid_table_name = 'ssid_temp'
            if self.temp_training_dbO.update_record(table_type='ssid', keyspace_name=keyspace_name, table_name=self.ssid_table_name, session_obj=session_obj, set_column=set_column, set_value=set_value, where_column=where_column, where_value=where_value):
                print "Updated %s Table " %(self.ssid_table_name)
                return True
            else:
                print "Failed updating %s Table" %(self.ssid_table_name)
                return False

        elif record_type == 'cell':
            self.cell_table_name = 'cell_temp'
            # NEED to add this in dbO
            if self.temp_training_dbO.update_record(table_type='cell', keyspace_name=keyspace_name, table_name=self.cell_table_name, session_obj=session_obj, set_column=set_column, set_value=set_value, where_column=where_column, where_value=where_value):
                print "Updated %s Table" %(self.cell_table_name)
                return True
            else:
                print "Failed updating %s Table " %(self.cell_table_name)
                return False

        else:
            print "Invalid table_type %s in update_record" %(table_type)
            return False


    def merge_record(self, msg_dict, queryCell, table_type, keyspace_name, session_obj, ssid_id):
        '''
        Takes data from msg_dict, merges it with queryCell data (if it's unique) and writes back to database

        ## VARIABLES initialized:
        self.ssid_table_name
        '''
        # NOTE LOCAL table_name
        self.ssid_table_name = 'ssid_temp'

        self.new_ssid_list = []
        if table_type == 'ssid':
            # Can you avoid this read?
            # XXX is the return value a list?
            self.ssid_record = self.temp_training_dbO.read_table(table_type, keyspace_name, self.ssid_table_name, session_obj, ssid_id= ssid_id)[0]
            #print "SSID Record ",self.ssid_record
           # Iterate over msg_dict for bssid match
            for self.bssid in msg_dict['i'].keys():
                if self.bssid == self.ssid_record.name:
                    self.update_record(keyspace_name, session_obj, set_column='signal_strength', set_value=msg_dict['i'][self.bssid], where_column='id', where_value=self.ssid_record.id)
                else:
                    # that BSSID is a new AP reading, Writing it to ssid_temp table
                    self.new_ssid_uuid = uuid1()
                    self.new_ssid_list.append( copy(self.new_ssid_uuid) )
                    self.values = (self.new_ssid_uuid, self.bssid, msg_dict['i'][self.bssid])
                    self.temp_training_dbO.insert_value(keyspace_name, 'ssid', self.ssid_table_name, self.values, session_obj)

            # Update all the new_ssid_uuid in  cell Tables
            self.update_record(keyspace_name, session_obj, set_column='ssid_ids', set_value=self.new_ssid_list, where_column=['mallname', 'floornumber','raw_section', 'x','y'], where_value=[str(queryCell.mallname), queryCell.floornumber, str(queryCell.raw_section), queryCell.x, queryCell.y], record_type='cell')

                    # Add this in ssid_table, and then do self.update_Record(cell_table) Append ssid_id uuid
                    # to cellrecord

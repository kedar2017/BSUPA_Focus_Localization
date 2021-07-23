'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

import traceback
import time
import json

from dbo import dbO

from uuid import uuid1, uuid4
dbO_instance = dbO()

'''
CreateKeyspace function is absent here | It is being reused from ../training_data/create_tables.py
'''

def CreateLiveTable( keyspace_name, session_obj):
    '''
    Create Initial Tables
    Tries to create Live Table, if any error, shutdown session cluster
    '''
    # ssid table
    r1 = dbO_instance.create_table(keyspace_name, 'ssid', 'ssid_t', session_obj)
    # cell table
    r2 = dbO_instance.create_table(keyspace_name, 'cell', 'cell_t', session_obj)
    # section table

    # Shutdown if either of tables couldn't be created
    if not (r1 and r2):
        print " COULDN'T create tables in database"
        print " Was it SSID? %r, CELL? %r" %(r1, r2)
        print "Shutting down cluster"
        session_obj.cluster.shutdown()

def StrFy(string):
    '''
    Stringi'fy the message
    '''
    return(string.__repr__())


def PopulateLiveTable(keyspace_name, session_obj, LiveCell):
    '''
    Take LiveCell Object and write it back to database
    '''
    # Extra Details for __future__
    extra_details = {}
    extra_details2 = {}

    list_ssid_uuids = []

    for ssid_obj in LiveCell.ssids:
        ssid_uuid = uuid1()
        list_ssid_uuids.append(ssid_uuid)
        values = (ssid_uuid, ssid_obj.ssid_name, ssid_obj.signal_strength)
        
        # Making a JSON string to store additional information 
        extra_details['mdoel'] = LiveCell.model

        # Insert into ssid table
        dbO_instance.insert_value(keyspace_name, 'ssid', 'ssid_t', values, session_obj)


    ### INTERNAL FUNCTION
    def t( list_ssid ):
        return str(list_ssid).replace("UUID(","").replace(")","").replace("'",'')
    
    # If timestamp is None by any chance, assign it system epoch time
    if LiveCell.timestamp == None:
        LiveCell.timestamp = int(time.time()*1000)

    # Extra detail should contain model number etc..
    values = ( StrFy(str(LiveCell.mob_hash)), LiveCell.timestamp, LiveCell.gps, StrFy(str(LiveCell.mall_name)), StrFy(str(LiveCell.floor_name)), LiveCell.section_name, LiveCell.point_x, LiveCell.point_y, t(list_ssid_uuids), StrFy(json.dumps(extra_details)), StrFy(json.dumps(extra_details2)) )
    dbO_instance.insert_value(keyspace_name, 'cell', 'cell_t', values, session_obj)
    return True


import json

from copy import deepcopy, copy

from glob import glob
from blip.database.common.db_functions import returnSession, keyspaceExists, tableExists
from blip.database.dbxactions.training_data.dbO import TrainingDbO

from blip.database.dbxactions.training_data.create_tables import createKeyspace, createTables
from blip.database.dbxactions.training_data.populate_tables import populateCellTable, populateSectionTable, populateFloorTable, populatePropertyTable

def initDatabase(host_ips, db_user, db_password, keyspace_name, schema_path, type_name_dict):
    """
    Takes database and creates them if they dont exist

    Returns Well initialized Training dbO as it will be used by other functions
    """

    session_obj  = returnSession(host_ips, db_user, db_password)
    training_dbO = TrainingDbO(schema_path, keyspace_name, type_name_dict, session_obj)


    # Create Training database object
    if keyspaceExists(keyspace_name, session_obj) and tableExists(training_dbO, type_name_dict.values(), for_module='training'):
        print "Training Keyspace and all its tables already exist"
    else:
        createKeyspace(training_dbO)
        createTables(training_dbO, type_name_dict)

    return training_dbO


def uploadReading(cell, training_dbO):
    """
    convert the reading to json and upload it to database
    """

    cid, section_name, floor_number, property_name = populateCellTable(cell, training_dbO)


def appendReadingDict(ssid_dict, reading):
    """
    Appends each reading to ssid_dict
    and returns ssid_dict
    """
    for ap_id, signal_strength in [(reading['Address']+"1234", reading['RSSI'])]:
        ssid_dict.setdefault(ap_id, []).append(signal_strength)

    return ssid_dict


def convertToCells(list_readings):
    """
    Takes list of readings, and collates all readings of each (X,Y) to form one cell
    """

    list_cells = []

    while list_readings != []:

        # Initialize variables
        cell = {"timestamp" : None,
                "hash"      : None,
                "section"   : None,
                "floor"     : -1,
                "property"  : None,
                "coords"    : [],
                "ssid"      : {},
                "gps"       : [],
                "model"     : None
        }
        ssid_dict = {}
        gps       =[0,0]
        timestamp = -1


        # Take first reading and update ssid_dict
        first_reading = list_readings.pop()
        thrash        = []
        ssid_dict     = appendReadingDict(ssid_dict, first_reading)

        # Collate ssid readings
        for each_reading in list_readings:
            # If x,y match append the data to ssid dictionary
            index = list_readings.index(each_reading)

            # If section is same and coordinates are same
            if each_reading['X'] == first_reading['X'] and each_reading['Y'] == first_reading['Y']: # and each_reading['l'] == first_reading['l']:
                # Append readings
                ssid_dict = appendReadingDict(ssid_dict, each_reading)
                timestamp = each_reading['Time']

                thrash.append(each_reading['Time'])

        # New List contains all the reaadings which dont have first_reading's coords
        new_list = []
        # Clean up
        for each_reading in list_readings:
            if not each_reading['Time'] in thrash:
                new_list.append(copy(each_reading))

        list_readings = copy(new_list)

        if timestamp != -1:
            cell['timestamp'] = timestamp
        else:
            cell['timestamp'] = first_reading['Time']

        cell['hash']      = '1234567890'
        cell['section']   = 'section_name'
        cell['floor']     = -1
        cell['property']  = 'property_name'
        cell['model']     = 'model_name'
        cell['coords']    = map(float, [(first_reading['X']),  first_reading['Y']])
        cell['ssid']      = copy(ssid_dict)
        cell['gps']       = [0,0]

        # Finally append to list
        list_cells.append(copy(cell))

    return list_cells

def dataParsing(data_file_path, training_dbO):
    """
    Takes data file path and returns a cell_list

    Cell format

    cell = {"timestamp" : epochtime_in_milli,
            "section"   : section_name,
            "property"  : Ryerson,
            "floor"     : -1,
            "x"         : x,
            "y"         : y,
            "ssid"      : {"ap1_name"  : [values1, value2 ..], "ap2" : [value1, val..],..}
            "gps"       : [lat, long],
            "model"     : Xiaomi
     }
    """
    data = open(data_file_path).read()

    # Ignore the last 2 null reading
    list_readings = [json.loads(i) for i in  data.split("\n")[:-1] ]


    list_cells = convertToCells(list_readings)

    print "CELL ", len(list_cells)
    print "-----UPDATING DATABASE------"
    [ uploadReading(cell, training_dbO) for cell in list_cells ]


def main():
    """
    Feed dat file to database
    """
    dat_path = "/home/kedar/Focus/Experiment2"
    list_of_files = glob(dat_path + "/*.dat")

    # XXX Remove absolute path
    schema_path    = "blip/database/dbxactions/training_data/training_schema.json"
    keyspace_name  = "training_bt_kd"

    # Table Type <-> Table Name mapping
    table_type_name_dict = {
                                "ssid"     : "ssid_t",
                                "cell"     : "cell_t",
                                "section"  : "section_t",
                                "floor"    : "floor_t",
                                "property" : "property_t" }


    training_dbO = initDatabase(["127.0.0.1"], "cassandra", "cassandra", keyspace_name, schema_path, table_type_name_dict)

    dataParsing(list_of_files[0], training_dbO)

if __name__ == "__main__":
    main()

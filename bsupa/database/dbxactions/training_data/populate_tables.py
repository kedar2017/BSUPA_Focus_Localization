from uuid import uuid1
# Populate Cell Table
def populateCellTable(cell, training_dbO):
    """
    Assuming all tables are already initialized, this function fills out

    cell is a dictionary loaded from json-data sent by android
    """
    list_bt_uuid = []
    bt_data_insertion = False

    for address, rssi in cell['info'].items():
        bt_uuid = uuid1()
        list_bt_uuid.append( bt_uuid )

        # Insert SSID
        if not training_dbO.insertValue('raw_data', [bt_uuid, address, rssi] ):
            print "Couldn't update raw_data table"
            bt_data_insertion = True

    cid = uuid1()
    flag = populateLocationTable(cell, training_dbO, cid)
    if not training_dbO.insertValue('cell', [cid, cell['hash'], cell['timestamp'], cell['x'], cell['y'], list_bt_uuid, cell['gps']]):
        print "Couldn't update cell table"
        return False
    else:
        return bt_data_insertion

def populateLocationTable(cell, training_dbO, cid):
    flag = True
    check = training_dbO.checkExistance('list_processed_cids', [cell['shop'], cell['property'], cell['floor'], cell['x'], cell['y'],cell['section']])
    training_dbO.setBool('is_processed', [False, cell['shop'], cell['property'], cell['floor'], cell['x'], cell['y'],cell['section']])
    if check == []:
	
        if not training_dbO.insertValue('location', [cell['property'], cell['floor'], cell['shop'], cell['section'], cell['x'], cell['y'], False,uuid1()]):
            print " Couldn't update location table"
            flag = False
    if not training_dbO.updateRecord('location', 'list_raw_cids',[ [cid], cell['shop'], cell['property'], cell['floor'],cell['x'],cell['y'],cell['section']], True):
        print " Couldn't update the cid in location table for cid list"
        flag = False	
    return flag

def populateProcessedTable():
    pass



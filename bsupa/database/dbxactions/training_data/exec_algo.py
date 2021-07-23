from uuid import uuid1

def algoExec(training_dbO):
    for proc_cids_obj in list(training_dbO.readTable('location','list_processed_cids',[])):
        proc_cids = proc_cids_obj.list_processed_cids
        proc_add_list = training_dbO.readTableWithCondition('processed_data','ble_id',[proc_cids])
        proc_strength_list = training_dbO.readTableWithCondition('processed_data','mean',[proc_cids])
        proc_stdev_list = training_dbO.readTableWithCondition('processed_data','std',[proc_cids])
        list_address = proc_add_list[0].ble_id
        list_strength= proc_strength_list[0].mean
        list_stdev = proc_stdev_list[0].std

        for i in range(len(list_address)):
            print "ADDRESS", list_address[i]
            print "STRENGTH", list_strength[i]
            print "STDEV", list_stdev[i]
    return True

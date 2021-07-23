from uuid import uuid1
import statistics
import math


#inserts mean and std into the processed_data table with the cids given
def processData(training_dbO):
    flag = True
    data = []
    count = 0

    # list of row objects of location table
    for location_row in list(training_dbO.readTable('location', 'list_raw_cids, is_processed, shop, property, floor, x, y,section', [])):
	is_processed  = location_row.is_processed
        if not is_processed:
	    raw_cids = location_row.list_raw_cids
	    shop = location_row.shop
            sect = location_row.section
	    proper = location_row.property
	    floor = location_row.floor
       	    x = location_row.x
	    y = location_row.y
	    key_val = {}
            add_list = []
	    mean_list = []
      	    std_list  = []
	    maxi_list = []
	    mini_list = []
            uuid_list = training_dbO.readTable('location', 'list_processed_cids', [])
            uuid = uuid_list[count].list_processed_cids
     	    training_dbO.insertValue('processed_data', [uuid])
            for element_cids in location_row.list_raw_cids:
            	for cell_cids in list(training_dbO.readTableWithCondition('cell', 'bt_id', [element_cids])):
                    for cids in cell_cids:
		        if cids == None:
			    break
                    	for e in cids:
                            signal_strength = training_dbO.readTableWithCondition('raw_data', 'signal_strength', [e])
                            add = training_dbO.readTableWithCondition('raw_data', 'ble_id', [e])
                            address = add[0].ble_id
			    if address not in key_val:
			    	key_val[address] = ([],[])
			    	add_list.append(address)
                            try:
			        for signal_elem in signal_strength[0].signal_strength:
                            	    key_val[address][0].append(signal_elem)
			  	    key_val[address][1].append(signal_elem)
                            except:
                                print "yo"
            for key in key_val.keys():
	    	mean = statistics.mean(key_val[key][0])
	    	if len(key_val[key][1])!= 1 and len(key_val[key][1])!= 0: 
		    	std  = statistics.variance(key_val[key][1])
		else:
		    	std  = 0.0
		maxi = max(key_val[key][0])
		mini = min(key_val[key][1])
	    	std = math.sqrt(std)
	    	mean_list.append(mean)
	    	std_list.append(std)
		maxi_list.append(maxi)
		mini_list.append(mini)
      	    training_dbO.setBool('is_processed', [True, shop, proper, floor, x,y,sect])
	    training_dbO.updateRecord('processed_data', 'ble_id', [add_list, uuid], False)
	    training_dbO.updateRecord('processed_data', 'mean' , [mean_list, uuid], False)
            training_dbO.updateRecord('processed_data', 'std', [std_list,uuid], False)
	    training_dbO.updateRecord('processed_data', 'max', [maxi_list,uuid], False)
	    training_dbO.updateRecord('processed_data', 'min', [mini_list,uuid], False)
	count = count + 1
    return True
#http://goo.gl/forms/h2FSsiDyBC

def predictShop(shop_list,addr_list, rssi_list,train_list):
	'''
	Predict the shop name based on minimum RSSI values
	inputs -
	shop_list - list of shops ??
	addr_list - list of addresses in live cell
	rssi_list - list of mean rssis of bles with these addresses in live cell
	train_list - training data ??
	'''
	print "RSSI LIST", rssi_list
	const = 3                       #Not used in current algo
        THRESHOLD = 20                  #Threshold to check if live rssi of BLE of interest is not less by this value than trained rssi
	LIMIT = 600.0
	shop_name = ""                  #For predicted shop
	sect_name = ""                  #For predicted section
	compare_list = []               #Stores uuid's of mapped plocations, used to compare it with live uuid's
	final_dict = {}                 #Stores key value pairs of those plocations which
	maxima = 0                      #variable which counts the number of BLEs common in live and given plocation
	addr_true = addr_list[rssi_list.index(max(rssi_list))]          #Get address of BLE with max (mean?) rssi
	for key in train_list.keys():                                   # iterate of the keys of ble_dict, which is the list of shops
        for list_elem in train_list[key]:                               # iterate over the values of a shop in ble_dict, which is train_dict
			for addr_key in list_elem[0].keys():            # iterate over the keys of temp_dict which is col1[size] which is 
				compare_list.append(addr_key)
			num_list = list(set(compare_list).intersection(addr_list))
			list_elem[2] = len(num_list)
			compare_list = []
			if list_elem[2] > maxima:
				maxima = list_elem[2]
	final_dict = {k: [] for k in train_list.keys()}                 # final_dict is intended to create a dictionary with key-value for the shop with max intersetion of traininf and live addresses
	for key in train_list.keys():
		for list_elem in train_list[key]:
			if list_elem[2] == maxima:
				final_dict[key].append(list_elem)
		if not final_dict[key]:
			del final_dict[key]
	minima = 100000.0
	max_max= 0.0
	num    = 0.0
	count  = 0
	for key in final_dict.keys():
		for list_elem in final_dict[key]:
			for i in range(len(addr_list)):
				'''
				if (list_elem[0][addr_list[i]][0] - const*list_elem[0][addr_list[i]][1]) < rssi_list[i] and rssi_list[i] < (list_elem[0][addr_list[i]][0] + const*list_elem[0][addr_list[i]][1]):
				'''
				num = num + (rssi_list[i] - list_elem[0][addr_list[i]][0])*(rssi_list[i] - list_elem[0][addr_list[i]][0])       #sum of squares of differences of rssis in live and training
				'''
				else:
					count = count + 1
				'''
			print "NUM", num
			if num < minima:
				minima = num
			'''
			if num > LIMIT:
				sect_name = "Intergalactic"
				shop_name = "transition"
				print "max_max", max_max
				return (shop_name, sect_name)
			'''
			list_elem[2] = num
			max_max= 0.0
			num = 0
	for key in final_dict.keys():
		for list_elem in final_dict[key]:
			if list_elem[2] == minima:
				shop_name = key                                                         #Predicted sop
				sect_name = list_elem[1]                                                #Predicted section
				rs_list   = [list_elem[0][addr][0] for addr in list_elem[0].keys()]     #get a list of mean rssi's of ble's in the location with minimum num ??
				rs_mini   = max(rs_list)                                                # strongest rssi among xxx
				for addr in list_elem[0].keys():
					if list_elem[0][addr][0] == rs_mini:                            #The strongest BLE
						min_addr = addr
				if min_addr != addr_true:                                               #is strongest BLE in live same as that found in xxx
                                        shop_name = "FALNF"
                                        sect_name = "FALNF"
                                        break
                                else:
                                        if list_elem[0][min_addr][0]-rssi_list[addr_list.index(min_addr)] > THRESHOLD:  #check if difference in one direction is greater than threshold 
                                                shop_name = "FALNF"
                                                sect_name = "FALNF"
                                                break
                                        '''
					for key1 in final_dict1.keys():
						for list_elem1 in final_dict1[key1]:
							for addr_keys in list_elem1[0]:
								if addr_keys == addr_true:
									maxi_rssi = rssi_list[rssi_list.index(max(rssi_list))]
									if maxi_rssi-list_elem1[0][addr_keys] < -20:
										shop_name = "Out of"
										sect_name = "universe"
									shop_name = key1
									sect_name = list_elem1[0][addr_true]
                                        '''
				break
	return (shop_name, sect_name)

import traceback
import statistics
import math
from bsupa.honeycomb.cells.read_cell import ReadCell
from copy import copy, deepcopy
from uuid import uuid1
from bsupa.database.dbxactions.training_data.dbO import TrainingDbO
from bsupa.database.common.db_functions          import keyspaceExists, tableExists
from bsupa.database.dbxactions.training_data.create_tables import createTables, createKeyspace
from bsupa.common.debugging import line_trace
import numpy as np  

class HoneycombPredict:
	def __init__(self, keyspace_name, session_obj):
		type_name_dict = {
				"raw_data"       : "raw_data_t",
				"cell"           : "cell_t",
				"location"       : "location_t",
				"processed_data" : "processed_data_t",
				"ble_modules"    : "ble_modules_t"
		}
		self.count = 0
		self.keyspace_name = keyspace_name
		self.session_obj   = session_obj
		self.training_dbo  = TrainingDbO('bsupa/database/dbxactions/training_data/training_schema.json', keyspace_name, type_name_dict, session_obj)
		if keyspaceExists(keyspace_name, session_obj) and tableExists(self.training_dbo, type_name_dict.values()):
			print "Training keyspace and all its tables already exists"
		else:
			createKeyspace(self.training_dbo)
		#self.training_dbo.createType("b_data")
			createTables(self.training_dbo, type_name_dict)
		#createTables(self.training_dbo, type_name_dict)

	def getAllCells(self):
		key = {}
		cell = ReadCell()
		count = 0
		list_cells = []
		for uuid1 in self.training_dbo.readTable('location','*',[]):
			uuid = uuid1.list_processed_cids
			shop = uuid1.shop

			# Populate ble data
			ble_data  = self.training_dbo.readTableWithCondition('processed_data', 'ble_id, mean, std', [uuid])
			addr_list = ble_data.processed_data
			mean_list = ble_data.mean
			std_list  = ble_data.std

			# Populate location data
			location_data = self.training_dbo.readTableWithCondition('location', 'x, y, floor, section, property', [shop])
			x_list        = location_data.x
			y_list        = location_data.y
			floor_list    = location_data.floor
			section_list  = location_data.section
			prop_list     = location_data.property

			count += 1
			ble_list = [ row.ble_id for row in self.training_dbo.readTable('ble_modules','*', []) ]

			for elem in range(len(addr_list[0].ble_id)):
				if addr_list[0].ble_id[elem] in ble_list :
					cell.rssi_obj.address = addr_list[0].ble_id[elem]
					cell.rssi_obj.mean    = mean_list[0].mean[elem]
					cell.rssi_obj.std     = std_list[0].std[elem]
					cell.x                = x_list[0].x
					cell.y                = y_list[0].y
					cell.shop             = shop
					cell.prop             = prop_list[0].property
					cell.floor            = floor_list[0].floor
					cell.section          = section_list[0].section
					cell.add_rssi()
			# Keys correspond to the required Address : RSSI pairs for a row of location table
			#keys = cell.return_str_data()

		return cell.rssids

	def predictCells(self,msg):
		'''
		Get the cell objects from the message
		'''
		cell = ReadCell()
		for key in msg.keys():
			cell.rssi_obj.address = key
			cell.rssi_obj.mean    = statistics.mean(msg[key])
			cell.rssi_obj.std     = math.sqrt(statistics.variance(msg[key]))
			cell.add_rssi()
		return cell

	def getShopList(self):
		'''
		Get the shop list
		'''
		shop_list = [shop_name.shop for shop_name in self.training_dbo.readTable('location', 'shop',[])]
		return shop_list

	def getAddrDict(self,shop_list):
		shop_dict = {}
		for j in range(len(shop_list)):
			ble_var = self.training_dbo.readTableWithCondition('ble_modules','ble_id',[shop_list[j]])
			ble_addr= ble_var[0].ble_id
			shop_dict[shop_list[j]] = ble_addr
		return shop_dict
		
	def getSectDict(self,shop_list):
		'''
		Get section dictionary for each of the shops
		'''
		shop_dict = {}
		for j in range(len(shop_list)):
			ble_var = self.training_dbo.readTableWithCondition('ble_modules','section',[shop_list[j]])
			ble_sect= ble_var[0].section
			shop_dict[shop_list[j]] = ble_sect
		return shop_dict

	def getPosDict(self, shop_list):
		'''
		Get position dict with shop name
		'''
		shop_dict = {}
		for j in range(len(shop_list)):
			ble_var = self.training_dbo.readTableWithCondition('ble_modules','x,y',[shop_list[j]])
			ble_pos_x = ble_var[0].x
			ble_pos_y = ble_var[0].y
			shop_dict[shop_list[j]] = (ble_pos_x, ble_pos_y)
		return shop_dict


	def getTraining(self,shop_list):
		'''
		To get the training data in the form of a dictionary of shops and address, position
		'''
		ble_dict = {}
		train_pos= {}
		for j in range(len(shop_list)):
			cid_shop       = [cid.list_processed_cids for cid in self.training_dbo.readTableWithCondition('location','list_processed_cids',[shop_list[j]])]
			sect_shop = [sect.section for sect in self.training_dbo.readTableWithCondition('location','section',[shop_list[j]])]
			train_dict = []
			count = 0
			for cid in cid_shop:
				temp_dict = {}				
				for col1,col2,col3 in self.training_dbo.readTableWithCondition('processed_data','ble_id,mean,std',[cid]):
					for size in range(len(col1)):
						temp_dict[col1[size]]=(col2[size],col3[size])
				train_dict.append([temp_dict,sect_shop[count],0])
				count = count + 1
			list_x    = [pos.x for pos in self.training_dbo.readTableWithCondition('location','x',[shop_list[j]])]
			list_y    = [pos.y for pos in self.training_dbo.readTableWithCondition('location','y',[shop_list[j]])]
			ble_dict[shop_list[j]] = train_dict
			train_pos[shop_list[j]]= (list_x, list_y)
		return (ble_dict,train_pos)
	
	# To get the live cell, to be given to FKF
	def getLive(self,cell, shop_name):
		dev_final_list = self.training_dbo.readTableWithCondition('ble_modules','ble_id, x, y',[shop_name])
		dev_addr       = dev_final_list[0].ble_id
		num_dev        = len(dev_addr)
		live_dict      = {}
		rssi_given     = []
		addr_list      = self.getADDR(cell)
		rssi_list      = self.getRSSI(cell)
		for k in range(len(dev_addr)):
			try:
				index = addr_list.index(dev_addr[k])
				rssi_given.append(rssi_list[index])
				live_dict[dev_addr[k]] = rssi_list[index]
			except:
				pass			
		return live_dict
		
	# To get the ADDR list from live packet
	def getADDR(self,cell):
		addr_list = []
		dev_list = cell.rssids
		for i in range(len(dev_list)):
			addr_list.append(dev_list[i].address)
		return addr_list
	
	# To get the RSSI list from live packet
	def getRSSI(self,cell):
		rssi_list = []
		dev_list = cell.rssids
		for i in range(len(dev_list)):
			rssi_list.append(dev_list[i].mean)
		return rssi_list
	
	# To get the STD of all the BLE's from training data
	def getSTD(self, shop_list):
		std_dict = {}
		for j in range(len(shop_list)):
			cid_shop       = [cid.list_processed_cids for cid in self.training_dbo.readTableWithCondition('location','list_processed_cids',[shop_list[j]])]
			train_dict = []
			for cid in cid_shop:
				temp_dict = {}
				for col1,col2 in self.training_dbo.readTableWithCondition('processed_data','ble_id,std',[cid]):
					for size in range(len(col1)):
						temp_dict[col1[size]]=2*col2[size]
				train_dict.append(temp_dict)
			std_dict[shop_list[j]] = train_dict
		print std_dict
		return std_dict
	
	# To get the Log-Distance model
	def logDist(self,addr, dict_train, pos_train):
		dist1 = 0.0
		fin1   = {}
		x1 = []
		y1 = []
		ble_pos = (0.0,0.0)
		for i in range(len(dict_train)):
			x = pos_train[0][i]/100.0
			y = pos_train[1][i]/100.0
			dist = math.sqrt((x-ble_pos[0])*(x-ble_pos[0]) + (y-ble_pos[1])*(y-ble_pos[1]))
			mean = dict_train[i][addr]
			fin1[dist] = mean
		for key in fin1.keys():
			x1.append(math.log10(float(key)))
			y1.append(fin1[key])
		print "LOG(X)", x1
		print "RSSI", y1
		x1=np.array(x1)
		y1=np.array(y1)
		slope1, intercept1 =  np.polyfit(x1, y1, 1)
		print "SLO,INT", (slope1,intercept1)
		return (slope1,intercept1)

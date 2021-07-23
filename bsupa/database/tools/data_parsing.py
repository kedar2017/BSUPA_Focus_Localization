
from glob import glob
from os.path import isfile, join


'''
	cell = {"timestamp": None,
			"section":section,
			"x":x,
			"y":y,
			"ssidFreq_val": {"ap1_name" : [values1, value2 ..], "ap2": [value1, val..],..}
			}

'''

def extract_x_y_section(filename):
	try:
		filename_split = filename.split("_")
		section = filename_split[0]
		x = int(filename_split[1])
		y = int(filename_split[2])
		return [section, x, y]
	except:
		print "File Name parsing failed: ", filename_split

def get_unique_ssid(list_reading):
	ssid = []
	for readings in list_reading:
		list_each_reading = readings.split(",")
		# If epoch values in data 1 should replace 0 in list_each_reading[index]
		if list_each_reading != ['']:
			if list_each_reading[1] != "" :
				ssidFreq = str(list_each_reading[1] +  list_each_reading[2])
				#ssid.append(list_each_reading[1], list_each_reading[2])
				ssid.append(ssidFreq)
	ssid = list(set(ssid))
	return ssid

def return_cell_list(path_training_data):

	list_of_files = glob(path_training_data+"/*.dat")
	cell_list = []

	for cell_file in list_of_files:

		[section, x, y] = extract_x_y_section(cell_file)

		cell = {"timestamp": None,
			"section":section,
			"x":x,
			"y":y,
			"ssidFreq_val":None
			}

		ssid_val = {}
		strength = []

		data = open(path_training_data+"/"+cell_file,'r').read()
		list_reading = data.split("\n")

		ssids = get_unique_ssid(list_reading)

		for readings in list_reading:
			list_each_reading = readings.split(",")
			# When data has epoch values
			last_time_stamp = list_each_reading[0]

			for ssid in ssids:
				# When data has epoch values this should be 1 else it should be 0
				if list_each_reading != ['']:
					if ssid == str(list_each_reading[1])+str(list_each_reading[2]):
						ssid_val.setdefault(ssid, []).append(int(list_each_reading[3])) #This should be 3 instead of 2 when epoch vales exist in data

		cell["ssidFreq_val"] = ssid_val

		cell_list.append(cell)

	return cell_list

if __name__ == "__main__":


	'''
	# For pretty printing
	import pprint
	pp = pprint.PrettyPrinter(depth=3)
	pp.pprint(return_cell_list("./pc_mob/"))
	'''

	for cell in return_cell_list('./test_data'):
		print cell
		print "-----------"

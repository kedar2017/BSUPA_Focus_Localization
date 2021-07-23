import json
import os
import requests
import socket
import time
import fnmatch
import glob
import json
import sys
sys.path.insert(0, '../../')
#from cip.cip          import message_map, message_dmap
#from common.debugging import logDeltaTime

#from predictor.store.filter_aps import get_malformed_reading
'''
# Check supa bssid-ssid
message =  {u'info': {u'PQRS': [-97,-67,-78], u'CAT': [-5967,-909],  u'CHEETAH':[12,34]}, u'shop': u'oreo', u'hash': u'a8ab7731f9', u'floor': -1, u'timestamp': 1432391013217, u'section': u'van', u'y': 90, u'x': 245, u'property': u'mall', u'gps': [0, 0], u'ble_one':'LION', u'ble_two':'PQRS',u'ble_thr':'CHEETAH'}
msg = { u'22222222-2222-2222-2222-222222222222': [-5967,-9019]}
# message to check clean_live_ap_filter
'''
count = 0

message = {"22222222-2222-2222-2222-222222222222":[-88,-91,-86,-88,-92,-92,-96,-97,-91,-87,-84,-83,-86,-87,-97,-81,-80,-82,-83,-86,-83,-84,-88,-90,-94,-84,-93,-84,-86,-87]}

check = ["mod_in",
"mod_out",
"papa_in",
"papa_out",
"subway_out"]
path = '/home/kedar/Focus/Expt_HN_Jun_12/'
list_fl = glob.glob(path+'Prediction.txt')
all_readings = [ json.loads(reading) for fl in list_fl for reading in open(fl).read().split("\n")[:-1]]
count = 0
#print "ALLLLLL", all_readings
for msg in all_readings:
	json_message = json.dumps(msg) + "END"
	print json_message
	#json_message = message_map(json_message, message['h']) + str(message['h']) + "END"
	#print "DCIP ", message_map(json_message[:-10],  json_message[-10:] )
	#itime = time.time()
	try:
		response = requests.post(r'http://192.168.0.8:13234', data=json_message)
	except:
		pass
	raw_input("==================")
	print response
	count = count +1 
		#dT = time.time()-itime
		#print "Delta time ", dT
		#logDeltaTime(str(dT))
		#print "Message Received", response.text
		#time.sleep(1)
	'''
	for info in all_readings:
		json_message = json.dumps(info) + "END"
		print json_message
		itime = time.time()

		response = requests.post(r'http://192.168.0.8:13234', data=json_message)
		raw_input("==================")
		dT = time.time()-itime
		print "Delta time ", dT, count
		logDeltaTime(str(dT))
		print "Message Received", response.text
		time.sleep(1)
	'''

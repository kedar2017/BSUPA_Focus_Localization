import argparse
import json
import operator
import pipes
import random
import SocketServer
import threading
import time
import traceback
import yaml
import collections
from time import strftime, localtime

from itertools import groupby

from common.debugging  import get_logger
from common.networking import writeTime, recvEnd

from database.common.db_functions import returnSession
from honeycomb.honeycomb_test  import HoneycombPredict
from prediction.kalman_filter     import kalman
from prediction.matrix_multiplication import apply_algo
from prediction.shop_predict      import predictShop

class Predictor:
	def __init__(self, keyspace_name, host_ips=('127.0.0.1',), username='username', password='password'):
		'''
		Mapper listens on for mapping packets of a location using RabbitMQ system
		'''
		self.session = returnSession(host_ips, username, password)
		self.honeycomb_test = HoneycombPredict(keyspace_name, self.session)

		# Init message to blank
		self.message = ''
		self.count = 1
		self.shop_list = self.honeycomb_test.getShopList()
		_dict_pos   = self.honeycomb_test.getTraining(self.shop_list)
		self.train_dict= _dict_pos[0]
		self.train_pos = _dict_pos[1]
		def shutdown_session(self, session_obj):
			session_obj.cluster.shutdown()
		self.sect_check = []

class MyTCPServer(SocketServer.ThreadingTCPServer):
	allow_reuse_address = True

def main():
	# ARGPARSE code
	parser = argparse.ArgumentParser(description = "SUPA or Spatial User Position and Analytics script. Interns will write more description")
	parser.add_argument('file', help="Takes a valid json file to configure variables")
	args = parser.parse_args()
	Rand = random.Random()

	# Config File
	config_file = open(args.file)
	# yaml library returns data as strings instead of unicode unlike in json lib
	getconfig = yaml.load(config_file) # This is a json file, json is subset of yaml

	# TODO(GPS) Use GPS to figure out mall name
	mall_name     = "mall_name"  # will be coming from mall filter
	keyspace_name = getconfig['keyspace']  # will be coming from mall filter
	host_ips      = getconfig['cassandra_ips']  # Cassandra host IPs
	uname         = getconfig['cassandra_uname']
	passwd        = getconfig['cassandra_passwd']

	# Instance Name = Client ID
	instance_prop = {"instance_name": getconfig['client_id']}

	# HTTP Variables
	box_ip   = getconfig['box_ip']
	box_port = getconfig['box_port']

	# Create Logger instance
	Log = get_logger('FocusAnalyticsMapper', 'mapper_dbg.log', instance_prop)

	# Create mapper instance
	predict = Predictor(keyspace_name, host_ips, uname, passwd)

	# Initializing mapper
	init_string = '\n\n========== Initializing FocusAnalyticsMapper(TM) at %s ==========\n\n'%(strftime("%Y-%m-%d %H:%M:%S", localtime()))
	print init_string
	Log.info(init_string)
	print predict.train_dict

	class MyTCPServerHandler(SocketServer.BaseRequestHandler):
		def handle(self):
			response_template = '''HTTP/1.1 200 OK
			Content-Type: application/json
			Access-Control-Allow-Origin: *\r\n\r\n%s
		'''
			try:
				data = recvEnd(self.request, "END")
				data = data.strip()
				data = data.split('\r\n\r\n')[-1]
				#json_msg = json.loads(data)
				#Log.info("[x] Decoded Data %s"%data)
				try:
					flag = True
					
					print "Response"
					# mode = weekly
					# 3:43pm, Friday, Jun 12-2015
					# 6 pm Monday, Jun 22-2015	 
					#response = {"LIVE":{"ap1":10,"ap2":20,"ap3":30,"ap4":10,"ap5":5,"ap6":40,"ap7":50},"PRED":{"ap3":30,"ap4":10,"ap5":5,"ap6":40},"MAPP":{"ap2":20,"ap6":40,"ap7":50}}
					response = {"DATA":[["ap1",[10,20,30]], ["ap2",[20,50,40]],["ap3",[23,45,68]]]}
					print response
					#response = {"ap2": 20,"ap3":10}
				except:
					# Response
					response = "FALNF"

					err_id = str(Rand.getrandbits(35))
					Log.error(" Failed Decoding message\nID: %s"%(err_id))
					print "Failed decoding message ID: %s\n"%(err_id)
					traceback.print_exc()

			except:
				print "Exception while receiving message:"
				# Response
				response = "FAException: decoding err"

				traceback.print_exc()
			finally:
				# Added to respond..
				
				encip_response = json.dumps(response)
				response       = response_template%(encip_response)
				self.request.sendall(response)
				
	server = MyTCPServer((box_ip, box_port), MyTCPServerHandler)
	server.serve_forever()

	server_thread = threading.Thread(target = server.serve_forever)

	#Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()
	server.shutdown()

if __name__ == "__main__":
	main()




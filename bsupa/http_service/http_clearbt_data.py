#!/usr/bin/python
#
#
#
import argparse
import base64
import json
import operator
import pipes
import random
import SocketServer
import threading
import time
import traceback
import yaml



from bsupa.common.debugging  import getLogging
from bsupa.common.networking import writeTime, recvEnd


from bsupa.common.networking import networking
from bsupa.common.db_functions import returnSession
from bsupa.honeycomb.honeycomb_mapper import HoneycombMapper

class ClearDataTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class ClearData:
    def __init__(self, keyspace_name, live_keyspace_name, host_ips=('127.0.0.1',), username='username', password='password'):
        '''
        ClearData listens on for mapping packets of a location using http
        '''
        # Init HoneyCombMapper
        self.session          = returnSession(host_ips, username, password)
        self.honeycomb_mapper = HoneycombMapper(keyspace_name, self.session)

        # Init message to blank
        self.message = ''

        def shutdown_session(self, session_obj):
            session_obj.cluster.shutdown()

def main():
    # ARGPARSE code
    parser = argparse.ArgumentParser(description = "SUPA or Spatial User Position and Analytics script. Interns will write more description")
    parser.add_argument('file', help="Takes a valid json file to configure variables")
    args   = parser.parse_args()
    Rand   = random.Random()

    # Config File
    config_file = open(args.file)
    # yaml library returns data as strings instead of unicode unlike in json lib
    getconfig   = yaml.load(config_file) # This is a json file, json is subset of yaml

    # TODO(GPS) Use GPS to figure out mall name
    mall_name          = "mall_name"  # will be coming from mall filter
    keyspace_name      = getconfig['keyspace']  # will be coming from mall filter
    live_keyspace_name = getconfig['live_keyspace']

    host_ips      = getconfig['cassandra_ips']  # Cassandra host IPs
    uname         = getconfig['cassandra_uname']
    passwd        = getconfig['cassandra_passwd']

    # Instance Name = Client ID
    instance_prop = {"instance_name": getconfig['client_id']}

    # HTTP Variables
    box_ip   = getconfig['box_ip']
    box_port = getconfig['box_port']

    # Create mapper instance
    mapper = ClearData(keyspace_name, live_keyspace_name, host_ips, uname, passwd)

    # CONSTANTS
    # NOTE Error codes | EC1 for malformed json | EC 2 for malformed request
    EC1 = "FAERR1"
    EC2 = "FAERR2"

    # Initializing mapper
    init_string = '\n\n========== Initializing FocusAnalyticsClearData(TM) at %s ==========\n\n'%(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    logI(init_string)


    class ClearDataTCPServerHandler(SocketServer.BaseRequestHandler):
        def handle(self):
            response_template = '''HTTP/1.1 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *\r\n\r\n%s
        '''
            try:
                self.request.settimeout(1)

                # get http packet
                data = self.request.recv(2048)
                data = data.strip()
                data = data.split('\r\n\r\n')[-1]

                # Data message
                json_msg = json.loads(data)
                logI(" [x] Decoded Data %s" %data)

            except:
                print "Exception while receiving message:"
                # Response
                logE(" Failed Decoding Request\n%s"%(traceback.format_exc()))

            finally:
                # Added to respond..
                logI(" Response %s"%(response))

                pf_data = json.dumps(response)

                encip_response = json.dumps( {"response":message_map(pf_data, key)} )
                response       = response_template%(encip_response)

                self.request.sendall(response)
                self.request.close()

    server = ClearDataTCPServer((box_ip, box_port), ClearDataTCPServerHandler)
    server.serve_forever()

    server_thread = threading.Thread(target = server.serve_forever)

    #Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    server.shutdown()

if __name__ == "__main__":
    main()

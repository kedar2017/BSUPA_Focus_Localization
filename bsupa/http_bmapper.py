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

from time import strftime, localtime

from common.debugging  import getLogging
from common.networking import writeTime, recvEnd

from database.common.db_functions import returnSession
from honeycomb.honeycomb_mapper   import HoneycombMapper

class Mapper:
    def __init__(self, keyspace_name, host_ips=('127.0.0.1',), username='username', password='password'):
        '''
        Mapper listens on for mapping packets of a location using RabbitMQ system
        '''
        # Init HoneyCombMapper
        self.session = returnSession(host_ips, username, password)
        self.honeycomb_mapper = HoneycombMapper(keyspace_name, self.session)

        # Init message to blank
        self.message = ''
        self.count = 1

        def shutdown_session(self, session_obj):
            session_obj.cluster.shutdown()


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
    Log = getLogging('FocusAnalyticsMapper', 'mapper_dbg.log', instance_prop)

    # Create mapper instance
    mapper = Mapper(keyspace_name, host_ips, uname, passwd)

    # Initializing mapper
    init_string = '\n\n========== Initializing FocusAnalyticsMapper(TM) at %s ==========\n\n'%(strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print init_string
    Log.info(init_string)


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
                json_msg = json.loads(data)
                Log.info("[x] Decoded Data %s"%data)
                print "Data", json_msg

                if sum(json_msg['gps']) == 0:
                    response = "GPS -> 0 | enable gps/restart phone"
                else:
                    response = "FAOk: valid gps"
                try:
                    # mode = weekly
                    mapper.honeycomb_mapper.updateDB(json_msg)
                    mapper.count = mapper.count + 1
                    if (mapper.count % 3 == 0):			
                        flag = mapper.honeycomb_mapper.calcMean()		
                    # Response
                    response += "|updated db"
                except:
                    # Response
                    response = "FAException: database err "

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
                encip_response = json.dumps({"response": response})
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




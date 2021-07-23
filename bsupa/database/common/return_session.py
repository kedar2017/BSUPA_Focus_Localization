'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

import traceback

from cassandra.auth import PlainTextAuthProvider as PTAP
from cassandra.cluster import Cluster


def return_session(host_ips, uname, passwd, keyspace = None):
    '''
    Create and return a cassandra server session | Will be used by many
    '''
    credentials = PTAP(username=uname, password=passwd)
    cluster = Cluster(host_ips, auth_provider=credentials)
    
    # Is this really necessary?
    if keyspace != None:
        try:
            session_obj = cluster.connect(keyspace_name)
        except:
            print "Keyspace %s NOT FOUND"%(keyspace) 
            traceback.print_exc()
    else:
        session_obj = cluster.connect()

    return session_obj

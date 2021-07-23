'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

import traceback
import operator

from cassandra.auth import PlainTextAuthProvider as PTAP
from cassandra.cluster import Cluster

def returnSession(host_ips, uname, passwd, keyspace_name = None):
    '''
    Create and return a cassandra server session | Will be used by many
    '''
    credentials = PTAP(username=uname, password=passwd)
    cluster = Cluster(host_ips, auth_provider=credentials)

    # Is this really necessary?
    if keyspace_name != None:
        try:
            session_obj = cluster.connect(keyspace_name)
        except:
            print "Keyspace %s NOT FOUND"%(keyspace_name)
            traceback.print_exc()
    else:
        session_obj = cluster.connect()

    return session_obj


def keyspaceExists(keyspace_name, session_obj):
    '''
    Returns True if keyspace exists else False
    '''
    all_keyspaces = session_obj.execute("""
        SELECT * FROM system.schema_keyspaces""")

    return keyspace_name in [ i.keyspace_name for i in all_keyspaces ]


def tableExists(dbO, table_name_list):
    '''
    Takes a table_name_list and2823 check if each table_name in table_name_list exists
    Returns True if all tables exists in keyspace, else returns False

    for_module = 'training' or 'temp_training' or 'live'

    for_module='training' used by trainer.py to create training tables
    '''
    table_list = dbO.listTables()

    bool_results = [ table_name in table_list for table_name in table_name_list ]

    #print 'b results',bool_results
    return reduce(operator.and_, bool_results ,True)


def executeStatement(statement, values, session_obj):
    """
    First it prepares statement and then it executes
    values should be a list

    returns True if successful else False
    """
    try:
       prepared_statement = session_obj.prepare(statement)
       session_obj.execute(prepared_statement, values)
       return True
    except:
        traceback.print_exc()
        return False

def executeAndReturnData(statement, values, session_obj):
    """
    First it prepares statement and then it executes
    MOSTLY used by readTable
    values should be a list

    returns data if successful else False
    """
    try:
        prepared_statement = session_obj.prepare(statement)
        return session_obj.execute(prepared_statement, values)	
    except:
        traceback.print_exc()
        return False

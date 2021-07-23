'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''
from uuid import uuid1, uuid4
from data_parsing import return_cell_list
from cassandra.cluster import Cluster
import sys, traceback



def create_index(session):
    '''
    create primary index
    '''
    try:
        session.execute("""create INDEX ssid_callref on testdb.ssid(cellref);""")
    except:
        pass


def main(session):
    '''
    Reading from database
    '''

    cell_list = session.execute("""
        SELECT * FROM testdb.cells;
            """)

    for cell in cell_list:

        cell_uuid = cell.id
        print cell.point_x
        print type(cell.point_x)
        ssid_list = cell.ssid_ids

        for ssid_id in ssid_list:
            ssid = session.execute('''
               SELECT * FROM testdb.ssid WHERE id=%s
                ''' %(ssid_id) )
            
            # ssid object is a list with single element
            print "SSID ", ssid
            print "NAME ",ssid[0].name
        # THIS ssid can now be used
        #print cell
        #print ssid

if __name__ == "__main__":
    try:
        cluster = Cluster()
        session = cluster.connect()
        main(session)
    except:
        traceback.print_exc(file=sys.stdout)
    finally:
        session.cluster.shutdown()

from uuid import uuid1, uuid4
from data_parsing import return_cell_list
from cassandra.cluster import Cluster
import sys, traceback


def update_cell( cell_list, session_obj, keyspace ):
    '''
    Adds entire cell_list created by
    '''

    for cell in cell_list:
        list_ssid_uuids = []

        cell_uuid =  uuid1()

        ## Update ssid table
        for AP in cell['ssidFreq_val'].keys() :

            # Get AP name and AP Frequency by splitting AP name
            ap_name, ap_frequency = AP[:-4], AP[-4:]

            ssid_uuid = uuid4()
            list_ssid_uuids.append(ssid_uuid)

            session_obj.execute("""INSERT INTO """ + keyspace + """.ssid(
                id, name, frequency, signal_strength)
                VALUES(%s, %s, %s, %s)""", ( ssid_uuid, ap_name, ap_frequency, cell['ssidFreq_val'][AP]  ))

        ## Update cell table

	## WHAT is the difference between executing q and directly doing it
	q = "INSERT INTO %s.cells( id, point_x, point_y, ssid_ids )  VALUES (%s, %s, %s, %s)" %('testdb', cell_uuid, cell['x'], cell['y'], str(list_ssid_uuids).replace("UUID(","").replace(")","").replace("'",'')  ) 
	#session_obj.execute("INSERT INTO " + keyspace + ".cells( id, point_x, point_y, ssid_ids ) \
        #        VALUES (%s, %s, %s, %s)", (cell_uuid, cell['x'], cell['y'], list_ssid_uuids ) )
	print "Query ", q
	session_obj.execute(q)



def main(session):

    #Training path
    path='../inorbit_map_test'
    cell_list = return_cell_list(path)

    keyspace = ''' CREATE KEYSPACE testdb WITH replication =
            { 'class':'SimpleStrategy',
            'replication_factor':3};
    '''

    ssid_schema = ''' CREATE TABLE testdb.ssid(
            id uuid PRIMARY KEY,
            name text,
            frequency text,
            signal_strength list<int>

        );'''

    cell_schema = ''' CREATE TABLE  testdb.cells(
            id uuid PRIMARY KEY,
            point_x int,
            point_y int,
            ssid_ids list<uuid>
    );
    '''

    try:
        session.execute(keyspace)
        session.execute(ssid_schema)
        session.execute(cell_schema)
    except:

        print "DB and Table already created"
        session.execute("DROP KEYSPACE testdb ;")
        traceback.print_exc()

        # Create New
        session.execute(keyspace)
        session.execute(ssid_schema)
        session.execute(cell_schema)

    update_cell( cell_list, session, 'testdb')


if __name__ == "__main__":

    try:
        cluster = Cluster()
        session = cluster.connect()
        main(session)
    except:

        traceback.print_exc(file=sys.stdout)
    finally:
        session.cluster.shutdown()

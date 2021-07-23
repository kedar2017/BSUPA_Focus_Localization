'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''
''' 
This will all go inside Cluster_section python module

basically populates section table
fills it will cell-uuid list
'''

from copy import copy
from uuid import uuid1, uuid4
from cassandra.cluster import Cluster
import traceback
from data_parsing import return_cell_list

# NOTE Entire file is temporary
'''
This will be taken down as and when clustering is written
'''
def populate_section_table( session_obj, keyspace, cell_table_name,  db_cell_x_y_tuple, csv_cell_list ):
    '''
    gets uuid_list
    '''

    uniq_sec = set( [i['section'] for i in csv_cell_list] )

    # sec_dict finally be { 'sec1' : [cid1, cid2, cid3..], 'sec2: [cid1, cid2,..]..   }
    sec_dict = {}

    for csv_cell in csv_cell_list:
        for db_cell_tuple in db_cell_x_y_tuple:

            if db_cell_tuple[0] == csv_cell['x'] and db_cell_tuple[1] == csv_cell['y']:
                sec_dict.setdefault(csv_cell['section'], []).append( copy(db_cell_tuple[2]) )

    import pprint
    p = pprint.PrettyPrinter()
    p.pprint(sec_dict)

    for sec_name in sec_dict.keys():
        session_obj.execute("""INSERT INTO """ + keyspace + """.se_section_t(
                id, cell_ids, name)
                VALUES(%s, %s, %s)""", ( uuid1(), sec_dict[sec_name],sec_name ))

def main():

    from cassandra.cluster import Cluster
    c = Cluster()
    session = c.connect()

    #Training path
    path='../inorbit_map_test'
    cell_list = return_cell_list(path)


    db_cell_list = session.execute(" select * from mykeyspace.c_cell_t")

    db_cell_x_y_tuple = []

    for cell_element in db_cell_list:
        db_cell_x_y_tuple.append( copy((cell_element.x, cell_element.y, cell_element.cid) ))

    populate_section_table( session, 'mykeyspace', 'c_cell_t', db_cell_x_y_tuple, cell_list) 

    session.cluster.shutdown()

if __name__ == '__main__':
    main()

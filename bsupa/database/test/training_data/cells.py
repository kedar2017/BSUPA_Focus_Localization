'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''
from cassandra.cluster import Cluster

keyspace = ''' CREATE KEYSPACE training_data WITH replication =
                { 'class':'SimpleStrategy',
                'replication_factor':3};
'''

cell_schema = ''' CREATE TABLE  training_data.cell (
        id uuid PRIMARY KEY,
        point_x int,
        point_y int,
        ssid text
);
'''

ssid_schema = ''' CREATE TABLE training_data.ssid (
        name text,
        frequency int,
        signal_strength list<int>
        );
        '''

mall_schema = ''' CREATE TABLE training_data.mall (
        name text PRIMARY KEY,
        floor text
        );
'''

floor_schema = ''' CREATE TABLE training_data.floor (
        name text PRIMARY KEY,
        section text

'''

section_schema = ''' CREATE TABLE training_data.section (

        name text PRIMARY KEY,
        cell text
        );
'''

def conn(host="127.0.0.1"):
    cluster = Cluster()
    session = cluster.connect()

    return session


def close(session_obj):
    return session_obj.cluster.shutdown()


def create_schema(session_obj, schema_name):
    session_obj.execute("""
        CREATE TABLE """ + schema_name + """.songs(
            id int PRIMARY KEY,
            title text,
            album text,
            artist text,
            some_list list<int>
        );
        """)

    session_obj.execute("""
        CREATE TABLE """ + schema_name + """.playlists(
            id int PRIMARY KEY,
            title text,
            album text,
            artist text,
        );
    """)
    #  logObj.info('Simplex keyspace and schema')


def delete_schema(session_obj, schema_name):
    '''Delete Cassandra Schema.'''

    session_obj.execute("""DROP KEYSPACE  """ + schema_name + """;""")


def load_data(session_obj, schema_name):
        session_obj.execute("""
            INSERT INTO """ + schema_name + """.songs (
                                id,
                                title,
                                album,
                                artist,
                                some_list
                            )

                            VALUES (
                                46,
                                'La Petite',
                                'Bye Bye',
                                'Josephine',
                                [3,5,78]
                            );
        """)
        session_obj.execute("""
                            INSERT INTO """ + schema_name + """.playlists(
                                id,
                                title,
                                album,
                                artist)

                            VALUES (
                                123,
                                'La Petite',
                                'Bye Bye',
                                'Josephine'
                            );
        """)

if __name__ == '__main__':

    session = conn()
    name = 'simplex'
    try:
        create_schema(session, name)
        load_data(session, name)

    except Exception:
        delete_schema(session, name)
        create_schema(session, name)
        load_data(session, name)

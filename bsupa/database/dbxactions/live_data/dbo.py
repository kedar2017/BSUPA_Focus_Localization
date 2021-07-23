'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

from schema import Schema as Schema

from cassandra import AlreadyExists
import traceback

class dbO:
    def __init__(self, schema_path='./database/dbxactions/live_data/schema.json'):
        self.schema = Schema(schema_path)
        pass

    def create_db(self, session_obj, db_name, RF=3, strategy='SimpleStrategy'):
        '''
        Creates database with parameters given
        Returns True if database is successfully created
        '''
        try:
            session_obj.execute(self.schema.keyspace('create', (db_name, strategy, RF)))
            print "Created DB %s" %(db_name)
            return True
        except AlreadyExists:
            print "Keyspace %s already exists"%(db_name)
            return True
        except:
            traceback.print_exc()
            return False

    def drop_db(self):
        '''
        Deletes database with parameters given
        Returns True if database is successfully deleted
        '''
        try:
            session_obj.execute(self.schema.keyspace('delete', (db_name)))
            print "Deleted database %s" %(db_name)
            return True
        except:
            traceback.print_exc()
            return False

    def create_table(self, keyspace_name, table_type, table_name, session_obj):
        '''
        Creates table according to table_type and returns True if successfully created
        Else return False
        table_type can be 'cell', 'ssid'

        Checkout schema.py __main__ to know how getattr is used to call function by its string value
        '''
        try:
            session_obj.execute( getattr(self.schema, table_type)('create', (keyspace_name, table_name)))
            return True
        except AlreadyExists:
            print "Table %s already exists in %s"%(table_name, keyspace_name)
            return True
        except:
            traceback.print_exc()
            return False

    def drop_table(self, keyspace_name, table_type, table_name, session_obj):
        '''
        Delete the table according to table_type and returns True if successfully deleted
        Else return False
        table_type can be 'cell', 'ssid', 'floor', 'section'

        Checkout schema.py __main__ to know how getattr is used to call function by its string value

        '''
        try:
        # Elegant Code, Dont Touch
            session_obj.execute( getattr(self.schema, table_type)('drop', (keyspace_name, table_name)))
            return True

        except:
            traceback.print_exc()
            return False

    def insert_value(self, keyspace_name, table_type, table_name, values, session_obj):
        '''
        Insert values in table:
        Value has to be a tuple according to table_type
        Return True if successful else False
        table_type can be 'cell', 'ssid', 'floor', 'section'

        For :
            ssid: value -> (id uuid,  name text, signal_strength int
            cell: value -> (hash text, timestamp bigint, gps map<float, float>,
                            mall_name text, floor_name text,
                            sec_prediction map<text, float>, predicted_x list<int>,
                            predicted_y list<int>, ssids_list list<uuid>,
                            PRIMARY KEY(hash, timestamp))
                            TOTAL VALUES => 09

        '''
        ### INTERNAL FUNCTION
        def t( list_ssid ):
            return str(list_ssid).replace("UUID(","").replace(")","").replace("'",'')


        # TODO Can somebody write this in a better way?
        try:

            def write_callback(results):
                print "SUCCESS ", results
            def write_err_callback(exc):
                print "FAIL ",exc

            # WHY DO I HAVE TO transform values[8] i.e. ssids_uuid list | check csv_to_db.py in test/
            if table_type == 'cell' :
                # Debugging
                print "CHECK ",getattr(self.schema, table_type)('insert', (keyspace_name, table_name, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10])) 

                session_obj.execute( getattr(self.schema, table_type)('insert', (keyspace_name, table_name, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10])) )
                return True

            elif table_type == 'ssid' :
                #Debugging
                #print "CHECK ", getattr(self.schema, table_type)('insert', (keyspace_name, table_name, values[0], values[1], values[2]))
                
                session_obj.execute( getattr(self.schema, table_type)('insert', (keyspace_name, table_name, values[0], values[1], values[2])))
                return True

            else:
                print "Wrong table_type: ",table_type
                return False

        except:
            print "Error Inserting Value in Table ", table_type
            traceback.print_exc()
            return False

    # Read Values from table
    def read_table(self, table_type, keyspace_name, table_name, session_obj, ssid_id=None, read_what="hash", query="*"):
        '''
        Read values from tables | Do it using linked lists/tables
        Return objects/instances of classes..

        Default value of query is asterisk (i.e. Select all)
        Returns True if read command is successful

        For ssid table_type specify ssids_id
        '''
        if table_type == 'ssid':
            try:
                self.result = session_obj.execute( getattr(self.schema, table_type)('select', (query, keyspace_name, table_name, ssid_id)) )
                return self.result
            except:
                traceback.print_exc()
                return False
        
        #This section is used by secondary_delete python script when filtering all the results
        elif table_type=='cell':
            # TODO Can this be written in a better fashion? May be a dictionary?
            if read_what == "hash":
                read_what = "select_hash"
            elif read_what == "timestamp":
                read_what = "select_timestamp"
            elif read_what == "all":
                read_what = "select_all"

            try:
                print "execute statement: ",  getattr(self.schema, table_type)(read_what, (query, keyspace_name, table_name)) 
                self.result = session_obj.execute( getattr(self.schema, table_type)(read_what, (query, keyspace_name, table_name)) )
                return self.result
            except:
                traceback.print_exc()
                return False
        else:
            print "Not Found table_type %s"%(table_type) 
    
    def delete_value(self, keyspace_name, session_obj, table_name, table_type="cell", value=None):
        '''
        delete_value deletes cell table as well as all the entries linked with it in ssid table type

        table_type and table_name are lists
        For ssid and cell, example:
            table_type = ['cell', 'ssid'] # Main table_type followed by dependent table_type
            table_name = ['cell_t', 'ssid_t'] # Main table_name followed by dependent table_name

        '''

        if table_type[0] == "cell":
            try:
                # For Debugging
                #print "STATEMENT CELL", getattr(self.schema, table_type[0])('delete', (keyspace_name, table_name[0], value[0], value[1])) 
                self.result = session_obj.execute( getattr(self.schema, table_type[0])('delete', (keyspace_name, table_name[0], value[0], value[1])) )
                
                #  Get ssids_list
                self.ssids_list = value[2]
                # Delete the ssids from ssids_list too
                for self.ssid_uuid in self.ssids_list:
                    # TODO Is there a way to assign 'ssid' through a variable
                    
                    # For Debugging
                    #print "SSID STATEMENT ", getattr(self.schema, table_type[1])('delete', (keyspace_name, table_name[1], self.ssid_uuid))
                    self.ssid_result = session_obj.execute( getattr(self.schema, table_type[1])('delete', (keyspace_name, table_name[1], self.ssid_uuid)) )
                
                return self.result
            except:
                traceback.print_exc()
                return False
        else:
            print "Invalid table_type: %s" %(table_type)
            return False

    def list_tables(self, keyspace_name, session_obj):
        '''
        Returns list of all table_names in that keyspace
        '''
        try:
            self.table_names = session_obj.execute( self.schema.keyspace('list_tables', keyspace_name.__repr__()) )
            return [ self.row.columnfamily_name for self.row in self.table_names ]
        except:
            traceback.print_exc()
            return False

    # TODO Implement:
    def update_table(self, table_type):
        '''
        Updates according to table_type('cell', 'section'..) and returns True if successfully written
        '''
        pass

    def write_table(self):
        pass

'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

import traceback

from schema import Schema as Schema
from cassandra import AlreadyExists

from bsupa.database.common.db_functions import executeStatement, executeAndReturnData

class TrainingDbO:
    """
    Training Database Operations Class File

    Contains code to perform insert / add / drop etc.. operations on database
    """
    def __init__(self, schema_path, keyspace_name, table_type_name_dict, session_obj):
        self.schema         = Schema(schema_path)
        self.keyspace_name  = keyspace_name
        self.session_obj    = session_obj
        self.type_name_dict = table_type_name_dict

    def createDB(self, RF=3, strategy='SimpleStrategy'):
        '''
        Creates database with parameters given
        Returns True if database is successfully created
        '''
        try:
            self.session_obj.execute(self.schema.keyspace('create', (self.keyspace_name, strategy, RF)))
            print "Created DB %s" %(self.keyspace_name)
            return True
        except AlreadyExists:
            print "Keyspace %s already exists"%(self.keyspace_name)
            return True
        except:
            traceback.print_exc()
            return False

    def createTable(self, table_type, table_name):
        '''
        Creates table according to table_type and returns True if successfully created
        Else return False
        table_type can be 'cell', 'ssid', 'floor', 'section' or 'property'


        Checkout schema.py __main__ to know how getattr is used to call function by its string value
        '''
        keyspace_name = self.keyspace_name
        session_obj   = self.session_obj

        try:
	    #print "CT DEBUG: ",getattr(self.schema, table_type)('create', (keyspace_name, table_name))
            session_obj.execute( getattr(self.schema, table_type)('create', (keyspace_name, table_name)))
            return True          

        except AlreadyExists:
            print "Table %s already exists in %s"%(table_name, keyspace_name)
            return True
        except:
            traceback.print_exc()
            return False

    def createType(self):
        keyspace_name = self.keyspace_name
        session_obj   = self.session_obj

        try:
            session_obj.execute( getattr(self.schema, 'processed_data')('create_type', keyspace_name))
            return True
        except AlreadyExists:
            print " Already exists "
            return True
        except:
            traceback.print_exc()
            return False

    # Insert values in table
    def insertValue(self, table_type, values):
        """
        Insert values in table
        table_types are keys of training_schema.json

        values have to be a ordered list (check schema to know the order)

        Returns True if insertion successful else False
        """
        statement = getattr(self.schema, table_type)('insert', (self.keyspace_name, self.type_name_dict[table_type]))
        return executeStatement(statement, values, self.session_obj)

    # Read values from table
    def readTable(self, table_type, column="*", condition=[]):
        """
        column name to select or asterisk to select all columns
        """

        statement = getattr(self.schema, table_type)('select', (column, self.keyspace_name, self.type_name_dict[table_type]))
        #print "STATEMENT ",statement
        return executeAndReturnData(statement, condition, self.session_obj)

    def readTableWithCondition(self, table_type, column="*", condition=[]):
        """
        """
        statement = getattr(self.schema, table_type)('con_select', (column, self.keyspace_name, self.type_name_dict[table_type]))
        return executeAndReturnData(statement, condition, self.session_obj)

    def checkExistance(self, column = "*", condition=[]):
	statement = getattr(self.schema, 'location')('cid_select', (column, self.keyspace_name, self.type_name_dict['location']))
        return executeAndReturnData(statement, condition, self.session_obj)

    def setBool(self, column, values):
	statement = getattr(self.schema, 'location')('set_bool', (self.keyspace_name, self.type_name_dict['location'], column))
	return executeStatement(statement, values, self.session_obj)

    def listTables(self):
        '''
        Returns list of all table_names in that keyspace
        '''
        try:
            self.table_names = self.session_obj.execute( self.schema.keyspace('list_tables', self.keyspace_name.__repr__()) )
            return [ self.row.columnfamily_name for self.row in self.table_names ]
        except:
            traceback.print_exc()
            return False


    def truncateTable(self, table_type):
        """
        Returns true if table was deleted/truncated successfully
        """
        statement = getattr(self.schema, table_type)('truncate', (self.keyspace_name))
        return executeStatement(statement, values, self.session_obj)


    # TODO Implement:
    def updateRecord(self, table_type, set_column, values, append = False):
        '''
        Updates record according to table_type('cell', 'section'..) and returns True if successfully written
        values will contain a [ set_value, where_value ]
        '''
	if not append:
	        statement = getattr(self.schema, table_type)('update', (self.keyspace_name, self.type_name_dict[table_type], set_column))

	else:
		statement = getattr(self.schema, table_type)('update_app', (self.keyspace_name, self.type_name_dict[table_type], set_column,  set_column))
        return executeStatement(statement, values, self.session_obj)

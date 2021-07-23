'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

"""
    self class file is supposed to provide required schemas to other database
    related python programs to keep modularity intact and the module robust and
    independent of file specific design changes.
"""

import traceback
import json


class Schema:
    '''Add doc string here.'''  # TODO(Doc1): Do self
    def __init__(self, schema_path='./database/dbxactions/live_data/schema.json'):
        self.schema_path = schema_path

    def keyspace(self, action, values, ):
        '''Returns string containing keyspace schema.'''
        element = 'keyspace'
        query = self._generate_query(element, action, values, self.schema_path)
        return query

    def ssid(self, action, values, ):
        '''Returns string containing ssid schema.'''
        element = 'ssid'
        query = self._generate_query(element, action, values, self.schema_path)
        return query

    def cell(self, action, values, ):
        '''Returns string containing cell schema.'''
        element = 'cell'
        query = self._generate_query(element, action, values, self.schema_path)
        return query

    def mall(self, action, values, ):
        '''Returns string containing mall schema.'''
        element = 'mall'
        query = self._generate_query(element, action, values, self.schema_path)
        return query

    def floor(self, action, values, ):
        '''Returns string containing floor schema.'''
        element = 'floor'
        query = self._generate_query(element, action, values, self.schema_path)
        return query

    def section(self, action, values, ):
        '''Returns string containing section schema.'''
        element = 'section'
        query = self._generate_query(element, action, values, self.schema_path)
        return query

    @staticmethod
    def _generate_query(element, action, values, path):
        '''Returns required values via. query format.'''
        
        try:
            json_schema = open(path)
            generic_schema = json.load(json_schema)
            raw_schema = generic_schema[element][action]
            final_schema = (raw_schema) % values
            return final_schema

        except Exception:
            traceback.print_exc()
            raise Exception("Invalid Schema\n")


if __name__ == "__main__":

    schema = Schema(schema_path='./schema.json')

    # Check statement returned for keyspace
    print schema.keyspace('create', ('testdb', 'SimpleStrategy', 3)) #Values always should be in tuple

    # Check statment returned for create table
    table_type = 'cell'
    print getattr(schema, table_type)('select_hash', ('*', 'keyspace_name','cell_table', 'abc'))
    
    # Check statement for Insert table
    table_type = 'cell'
    print getattr(schema, table_type)('insert',('keyspace_name', 'cell_table', 'hash', 1123871238, [123,423] ,'macd', 'floor1', "{'sec1':0.1231, 'sec2':0.142}", [1,2], [3,2], 'ssid-uuids'   ) )

    # Check statement returned for ssid table
    table_type = 'ssid'
    print getattr(schema, table_type)('create', ('keyspace_name','ssid_table',))


#
#
#
#
"""
	self class file is supposed to provide required schemas to other database
	related python programs to keep modularity intact and the module robust and
	independent of file specific design changes.
"""

import traceback
import json


class Schema:
	'''Add doc string here.'''  # TODO(Doc1): Do self
	def __init__(self, schema_path='./database/dbxactions/training_data/training_schema.json'):
		self.schema_path = schema_path

	def keyspace(self, action, values, ):
		'''Returns string containing keyspace schema.'''
		element = 'keyspace'
		query = self._generate_query(element, action, values, self.schema_path)
		return query

	def raw_data(self, action, values, ):
		'''Returns string containing ssid schema.'''
		element = 'raw_data'
		query = self._generate_query(element, action, values, self.schema_path)
		return query

	def cell(self, action, values, ):
		'''Returns string containing cell schema.'''
		element = 'cell'
		query = self._generate_query(element, action, values, self.schema_path)
		return query

	def location(self, action, values, ):
		'''Returns string containing property schema.'''
		element = 'location'
		query = self._generate_query(element, action, values, self.schema_path)
		return query

	def processed_data(self, action, values, ):
		'''Returns string containing floor schema.'''
		element = 'processed_data'
		query = self._generate_query(element, action, values, self.schema_path)
		return query
	def ble_modules(self, action, values, ):
		'''Returns string containing floor schema.'''
		element = 'ble_modules'
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

	schema = Schema(schema_path='./training_schema.json')

	# Check statement returned for keyspace
	print schema.keyspace('create', ('testdb', 'SimpleStrategy', 3)) #Values always should be in tuple

	# Check statment returned for create table
	table_type = 'cell'
	print getattr(schema, table_type)('select', ('*', 'keyspace_name','cell_table'))

	# Check statement returned for ssid table
	table_type = 'raw_data'
	print getattr(schema, table_type)('create', ('keyspace_name','raw_table',))

	table_type = 'location'
	print getattr(schema, table_type)('create', ('keyspace_name','location_table',))


	print getattr(schema, 'processed_data')('create_type')
	table_type = 'processed_data'
	print getattr(schema, table_type)('create', ('keyspace_name','processed_table',))

	table_type = 'ble_modules'
	print getattr(schema, table_type)('create', ('keyspace_name','ble_modules_table',))

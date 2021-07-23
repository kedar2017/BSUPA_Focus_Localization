from bsupa.database.dbxactions.training_data.dbO             import TrainingDbO
from bsupa.database.dbxactions.training_data.populate_tables import populateCellTable, populateLocationTable
from bsupa.database.common.db_functions                      import keyspaceExists, tableExists
from bsupa.database.dbxactions.training_data.create_tables   import createKeyspace, createTables
from bsupa.database.dbxactions.training_data.calc_mean       import processData

from uuid import uuid1
class HoneycombMapper:
	"""
	Honeycomb Mapper Class
	used by http_bmapper to update live readings
	"""
	def __init__(self, keyspace_name, session_obj):
		type_name_dict = {
				"raw_data"       : "raw_data_t",
				"cell"           : "cell_t",
				"location"       : "location_t",
				"processed_data" : "processed_data_t",
				"ble_modules"    : "ble_modules_t"
		}
		self.count = 0
		self.keyspace_name = keyspace_name
		self.session_obj   = session_obj
		self.training_dbo  = TrainingDbO('bsupa/database/dbxactions/training_data/training_schema.json', keyspace_name, type_name_dict, session_obj)
		if keyspaceExists(keyspace_name, session_obj) and tableExists(self.training_dbo, type_name_dict.values()):
			print "Training keyspace and all its tables already exists"
		else:
			createKeyspace(self.training_dbo)
		#self.training_dbo.createType("b_data")
			createTables(self.training_dbo, type_name_dict)
		#createTables(self.training_dbo, type_name_dict)

	def updateDB(self, cell):
		"""
		Updates each reading
		Returns True if successful else returns False
		"""

		return populateCellTable(cell, self.training_dbo)

	def calcMean(self):
		"""
		calculates the mean and fills the processed_data table
		"""
		return processData(self.training_dbo)

    def truncateAllTable(self):
        """
        Truncate all tables
        """
        truth_values = []
        for table_type in type_name_dict:
            truth_values.append(self.training_dbO.truncateTable(table_type))

        return all(truth_values)

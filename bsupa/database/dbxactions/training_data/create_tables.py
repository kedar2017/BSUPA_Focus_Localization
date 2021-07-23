
import traceback

def createKeyspace(dbO_instance):
    '''
    Create Keyspace function
    Tries to create a db, if any error, shutsdown session cluster
    '''
    keyspace_name = dbO_instance.keyspace_name
    session_obj   = dbO_instance.session_obj

    # Create a New Keyspace
    try:
        if not dbO_instance.createDB(RF=1):
            raise Exception("Couldn't Create Database")
    except:
        # Shutdown cluster
        traceback.print_exc()
        session_obj.cluster.shutdown()

def createTables(dbO_instance, type_name_dict):
    '''
    Create Initial Tables
    Tries to create a table, if any error, shutdown session cluster

    type_name_dict has table_type as keys and table_name as values for ex:
        {
            "ssid" : "ssid_t",
            "cell" : "cell_t",
            "section":"section_t",
            "floor" : "floor_t",
            "property":"property_t"
        }
    '''
    # Try creating ssid-cell-section-floor table in that Order
    # NOTE Will have to create a name generator function if you plan to have dynamic tables
    #dbO_instance.createType()
    keyspace_name = dbO_instance.keyspace_name
    session_obj   = dbO_instance.session_obj
    for table_type, table_name in type_name_dict.items():
        if not dbO_instance.createTable(table_type, table_name):
	
            print "Couldn't create table for type %s\n Shutting cluster down"%(table_type)
            # Shutdown cluster
            session_obj.cluster.shutdown()
    
	

#!/usr/bin/python

'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

# Accessing Data from Database to manipulate further

# command line arguments
import argparse

# standard libraries to import
import yaml
import operator

# Database libraries
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider as PTAP
from copy import copy


# Access local libraries

# Honeycomb contains Object defintions
from honeycomb import honeycomb
from honeycomb.cells import cell
from honeycomb.sections import section
from honeycomb.floors import floor

# Database contains methods to access data
from database.common.db_functions import returnSession

# Import lib for analysis of training data
#from predictor.position.tools import training_analysis

# Import custom print module
from common.print_colors import cprint

# Take command line arguments
parser = argparse.ArgumentParser(description = "A template script which shows how to access data from database")
parser.add_argument('file', help="Takes a valid json file to configure variables")
args = parser.parse_args()
def mean(l):
    n=len(l)
    sum=0.0
    for item in l:
        sum+=item
    return (sum/n)
def std_dev(l):
    mean_val=mean(l)
    n=len(l)
    sum=0.0
    for item in l:
        sum+=(item-mean_val)**2
    var=sum/n
    return(var**0.5)

class AccessData:
    def __init__(self, training_keyspace, host_ips=('127.0.0.1'), username='username', password='password'):
        '''
        Constructor for lass for spatial variation
        '''
        self.session = returnSession(host_ips, username, password)
        self.keyspace_name = training_keyspace

        self.honeycomb  = honeycomb.honeycomb(self.keyspace_name, self.session)
        self.list_cells = self.honeycomb.getAllCells()


    def shutdown(self):
        self.session.cluster.shutdown()

    
def main():
    '''
    Entry point
    '''
    # Read json configuration file
    config_file = open(args.file)
    # yaml library returns data as strings instead of unicode unlike in json lib
    getconfig = yaml.load(config_file) # This is a json file, json is subset of yaml

    # Print Object
    c = cprint(True)

    training_keyspace = getconfig['training_keyspace']

    # Cassandra credentials
    cassandra_host_ips      = getconfig['cassandra_ips']
    cassandra_uname         = getconfig['cassandra_uname']
    cassandra_passwd        = getconfig['cassandra_passwd']
    cassandra_credentials   = PTAP(username=cassandra_uname, password=cassandra_passwd)

    # Create AccessData Object
    access_mydata = AccessData(training_keyspace, cassandra_host_ips, cassandra_uname, cassandra_passwd)
    for cell in access_mydata.list_cells:
        if cell.x==5 and cell.y==5:
            d=cell.return_ap_data()
            for key in d.keys():
                c.unset()
                c.prnt(key,'r')
                c.prnt(d[key],'y')
                c.set()
                c.prnt(key,'r')
                c.prnt(mean(d[key]),'b')
                c.prnt(std_dev(d[key]),'g')
    
            
    #access_mydata.list_cells[4].x
    # cprint example
    #c.prnt(("print length of data", len(access_mydata.list_cells), access_mydata.list_cells[17].return_ap_data() ), 'r')
    #c.prnt(("print length of data", len(access_mydata.list_cells), access_mydata.list_cells[18].return_ap_data() ), 'y')

    # Traversing through all cells in cell_list
    #for cell in access_mydata.list_cells:
    #    c.prnt(("Cell data", cell.x, cell.y), 'y')


if __name__ == '__main__':
    main()

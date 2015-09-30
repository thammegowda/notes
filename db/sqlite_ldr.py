#!/usr/bin/env python
__author__ = "ThammeGowda N <tgowdan@gmail.com>"
__date__ = "September 30, 2015"

import csv
import sqlite3
import argparse

def load_table(csv_file, db_file, table_name, header=True):
    """
    Loads CSV file into SQLite table
    """
    db_con = sqlite3.connect(db_file)
    cur = db_con.cursor()
    r = csv.reader(open(csv_file))
    #first rec is header
    field_names = r.next()    
    query = "INSERT INTO %s(%s) VALUES (%s)" % (table_name, ", ".join(field_names),\
                                ", ".join(["?" for i in range(len(field_names))]))
    print query
    cur.executemany(query, r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SQLite Loader')
    parser.add_argument('-d','--db', help='SQLite DB File; Example: employee.db', required=True)
    parser.add_argument('-i','--in', help='Input Csv File; Example: user.csv', required=True)
    parser.add_argument('-t','--table', help='Table Name; Example: user', required=True)
    args = vars(parser.parse_args())
    print args['db']
    print args['in']
    load_table(args['in'], args['db'], args['table'])
    

#!/usr/bin/env python
__author__ = "Thamme Gowda N <tgowdan@gmail.com>"
__date__ = "September 30, 2015"

import sys
import xlrd
import csv
from datetime import datetime

"""
Requirements
# Install xlrd
sudo pip install xlrd
"""
DATE_ONLY_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def read_cell_value(xl_cell, dt_mode=0):
   """
   Reads Value of Excel cell and formats properly based on value type
   """
   res = None
   val = xl_cell.value
   if xl_cell.ctype == xlrd.XL_CELL_NUMBER:
      # Dont convert everything to float
      res = int(val) if val.is_integer() else val
   elif xl_cell.ctype == xlrd.XL_CELL_DATE:
      tup = xlrd.xldate_as_tuple(val, dt_mode)
      dt = datetime(*tup)
      # IF no time portion is present then skip time format
      res = dt.strftime(DATE_ONLY_FORMAT if val.is_integer() else DATE_TIME_FORMAT)
   elif xl_cell.ctype == xlrd.XL_CELL_EMPTY or xl_cell.ctype == xlrd.XL_CELL_BLANK:
      res = None
   else:
      res = val
   return res

def convert(src, dest):
   """
   Converts all the sheets in given XLS|XLSX file to csv
   """
   workbook = xlrd.open_workbook(src)
   sheets = workbook.sheets()
   print("Found %d sheets in %s"% (len(sheets), src))
   for sheet in sheets:
      file_name = "%s%s.csv" % (dest, sheet.name)
      print "%s : Writing %d rows to %s" % (sheet.name, sheet.nrows, file_name)
      with open(file_name, 'w') as raw_wr:
         wr = csv.writer(raw_wr, quoting=csv.QUOTE_NONNUMERIC)
         for i in xrange(sheet.nrows):
            # dt_mode=workbook.datemode
            vals = [read_cell_value(sheet.cell(i, j)) for j in range(sheet.ncols)]
            wr.writerow(vals)

if __name__ == "__main__":
   if len(sys.argv) != 3:
      print "Usage::" + sys.argv[0] + " <SRC.xls> <DEST>"
      sys.exit(1)
   src, dest = sys.argv[1], sys.argv[2]
   convert(src, dest)

   
   

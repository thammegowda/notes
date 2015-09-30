#!/usr/bin/env python
__author__ = "Thamme Gowda N <tgowdan@gmail.com>"
__date__ = "September 30, 2015"

import sys
import xlrd
import csv

"""
Requirements
# Install xlrd
sudo pip install xlrd
"""

def convert(src, dest):
   """
   Converts given XLS|XLSX file to csv
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
            wr.writerow(sheet.row_values(i))

if __name__ == "__main__":
   if len(sys.argv) != 3:
      print "Usage::" + sys.argv[0] + " <SRC.xls> <DEST>"
      sys.exit(1)
   src, dest = sys.argv[1], sys.argv[2]
   convert(src, dest)

   
   

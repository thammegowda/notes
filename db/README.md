# Data Base Play Ground
   Here are scripts for db related operations

## Load Excel file to SQLite
```
#Create destination directory
mkdir csv

# Convert to CSV
xls2csv.py dataset1.xlsx csv/
# This should create a csv file for each sheet in excel


# Create the db and tables
sqlite3 db/hw2.db < db/createdb.sql  

# Load
sqlite_ldr.py -d db/hw2.db -t users -i csv/users.csv 
# this loads all records from 'csv/users.csv' to 'users' to db



```

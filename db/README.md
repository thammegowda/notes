# Data Base Play Ground
   Here are scripts for db related operations

## Load Excel file to SQLite
```
# Convert to CSV
xls2csv.py dataset1.xlsx csv/

# Create the db and tables
sqlite3 db/hw2.db.sqlite < db/createdb.sql

# Load
sqlite_ldr.py -d db/hw2.db.sqlite -t users -i csv/users.csv 

```

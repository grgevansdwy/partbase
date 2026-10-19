import sqlite3
from pathlib import Path
import csv

DB_PATH = Path(__file__).parent/"parts.db"
# if db exist, then delete
if DB_PATH.exists():
    DB_PATH.unlink()
# create new db - start fresh
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# create table from each file in data/
DATA_DIR = Path(__file__).parent/ "data"
for p in DATA_DIR.glob("*.csv"):
    table_name = p.stem
    with open(p, newline = '') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        count_header = len(header)

        cols = []
        for h in header:
            if h == "Part Number":
                cols.append('"' + h + '" TEXT PRIMARY KEY NOT NULL')
            else:
                cols.append('"' + h + '" TEXT NOT NULL')
        
        header_str = ",".join(cols)
        cur.execute(f'''CREATE TABLE "{table_name}" 
                    ({header_str})
                    ''')
        
        # insert all data on each csv -> table accordingly
        value_str = ""
        for i in range(0, count_header):
            value_str += "?"
            if i != count_header-1:
                value_str += ","

        for row in csv_reader:
            cur.execute(f'INSERT INTO "{table_name}" VALUES ({value_str})', row)
    
conn.commit()
conn.close()
import sqlite3 
import pandas as pd
dbFile = "alt-tab-macos.db"
conn = sqlite3.connect(dbFile)
df = pd.read_sql_query("select state from ISSUES", conn)
print(df)

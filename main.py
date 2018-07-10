import sqlite3

sqlite_file = 'my_db.sqlite' # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

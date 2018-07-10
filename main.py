import sqlite3

sqlite_file = 'my_db.sqlite' # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn='Ingredients', nf='ingredient_name', ft='STRING'))

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
        .format(tn='Recipes', nf='recipe_name', ft='STRING'))

conn.commit()

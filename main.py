import sqlite3

sqlite_file = 'recipes_db_file.sqlite' # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Check to see if tables have been created already or not
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Ingredients'")
all_rows = c.fetchall()
print(all_rows)

if len(all_rows) == 0:
    print("== Database file does not exist, creating new database file ==")
    # Creating a new SQLite table with 1 column
    c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
            .format(tn='Ingredients', nf='ingredient_name', ft='TEXT'))

    # Creating a new SQLite table with 1 column
    c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
            .format(tn='Recipes', nf='recipe_name', ft='TEXT'))

conn.commit()
conn.close()

import sqlite3

sqlite_file = 'recipes_db_file.sqlite' # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Check to see if tables have been created already or not
# Creating the SQLite table 'Ingredients'
c.execute('CREATE TABLE IF NOT EXISTS ingredients (ingredientName TEXT PRIMARY KEY)')

# Creating the SQLite table 'Recipes'
c.execute('CREATE TABLE IF NOT EXISTS recipes (recipeName TEXT PRIMARY KEY)')

# Creating the SQLite table 'Recipe_Contains'
create_table_query = (
    "CREATE TABLE IF NOT EXISTS recipe_contains ( "
    "ingredientName TEXT, "
    "recipeName TEXT, "
    "PRIMARY KEY (ingredientName, recipeName), "
    "   FOREIGN KEY (ingredientName) REFERENCES ingredients(ingredientName), "
    "   FOREIGN KEY (recipeName) REFERENCES recipes(recipeName)"
    ")"
    )
c.execute(create_table_query)

conn.commit()
conn.close()

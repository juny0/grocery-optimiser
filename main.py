#!/usr/bin/env python
#
#
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
# Authors:
#    Jun Yu <juny0@vt.edu>

import sqlite3
from cmd import Cmd

sqlite_file = "recipes_db_file.sqlite"  # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

"""
This is a helper method to execute queries on the database,
and does error handling so the program does not crash.
"""
def execute_db_query(q):
    try:
        c.execute(q)
        conn.commit()
    except sqlite3.Error as er:
        print('er:', er)
        print("If error is 'UNIQUE constraint failed', you may ignore")


class EntryPrompt(Cmd):

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit

    def do_addrecipe(self, args):
        """
        Add a recipe to your recipe book!
        This method only takes one argument initially, and that is the recipe name.
        Spaces are allowed.
        """
        if len(args) == 0:
            print("ERROR: No recipe name was specified")
        else:
            print("Adding %s to your recipe book." % args)
            print("Input ingredients line by line here. Enter STOP to terminate.")

            # Ingredients are read from user input line by line, and temporarily stored
            # in a set. After program is done reading from user input, program adds ingredients
            # to the 'recipe_contains' table.

            ingredients = set()

            # == Read from user input
            while (True):
                inpt = input(">> ").strip().lower()
                if (inpt != "stop"):
                    ingredients.add(inpt)
                else:
                    print("%s was added to your recipe book." % args)
                    break

            # == Push recipe to database
            # add recipe to 'recipes' table
            add_recipe_query = "INSERT INTO recipes (recipeName) VALUES ('{fargs}')" \
                .format(fargs=args)
            execute_db_query(add_recipe_query)

            # add ingredients to 'ingredients' table and 'recipe_contains' table.
            for entry in ingredients:
                add_ingredient_query = "INSERT INTO ingredients (ingredientName) VALUES ('{ingr}')" \
                    .format(ingr=entry)
                execute_db_query(add_ingredient_query)
                add_ingredient_query = "INSERT INTO recipe_contains (recipeName, ingredientName) VALUES ('{rn}', '{ingr}')" \
                    .format(rn=args, ingr=entry)
                execute_db_query(add_ingredient_query)

    def do_ingredients_usage(self):
        """
        Get a list of all the ingredients used by all of the recipes in your catalog, ordered from most used to least used.
        """


######################## ENTRY POINT ########################

# Check to see if tables have been created already or not
# Creating the SQLite table 'Ingredients'
create_table_query = "CREATE TABLE IF NOT EXISTS ingredients (ingredientName TEXT PRIMARY KEY)"
execute_db_query(create_table_query)

# Creating the SQLite table 'Recipes'
create_table_query = "CREATE TABLE IF NOT EXISTS recipes (recipeName TEXT PRIMARY KEY)"
execute_db_query(create_table_query)

# Creating the SQLite table 'Recipe_Contains'
create_table_query = (
    "CREATE TABLE IF NOT EXISTS recipe_contains ( "
    "recipeName TEXT, "
    "ingredientName TEXT, "
    "PRIMARY KEY (recipeName, ingredientName), "
    "   FOREIGN KEY (ingredientName) REFERENCES ingredients(ingredientName), "
    "   FOREIGN KEY (recipeName) REFERENCES recipes(recipeName)"
    ")"
)
execute_db_query(create_table_query)

# == Start command line interpreter
if __name__ == "__main__":
    prompt = EntryPrompt()
    prompt.prompt = "> "
    prompt.cmdloop("Starting prompt...")

conn.close()

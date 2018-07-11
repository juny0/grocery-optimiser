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

sqlite_file = "recipes_db_file.sqlite" # name of the sqlite database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

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
    "ingredientName TEXT, "
    "recipeName TEXT, "
    "PRIMARY KEY (ingredientName, recipeName), "
    "   FOREIGN KEY (ingredientName) REFERENCES ingredients(ingredientName), "
    "   FOREIGN KEY (recipeName) REFERENCES recipes(recipeName)"
    ")"
    )
c.execute(create_table_query)

conn.commit()

def execute_db_query(q):
    try:
        c.execute(q)
        conn.commit()
    except sqlite3.Error as er:
        print('er:', er)
        print("If error is 'UNIQUE constraint failed', you may ignore")

# == Start command line interpreter
class entry_prompt(Cmd):
    def do_addRecipe(self, args):
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
            inpt = ""
            ingredients = set()

            # == Read from user input
            while(True):
                inpt = input(">> ").strip().lower()
                if (inpt != "stop"):
                    print("YAY~")
                    ingredients.add(inpt)
                else:
                    print("%s was added to your recipe book." % args)
                    break

            # == Push recipe to database
            # add recipe to 'recipes' table
            add_recipe_query = "INSERT INTO recipes (recipeName) VALUES ('{fargs}')"\
                               .format(fargs=args)
            try:
                c.execute(add_recipe_query)
                conn.commit()
            except sqlite3.Error as er:
                    print('er:', er)
                    print("If error is 'UNIQUE constraint failed', you may ignore")
            
            for entry in ingredients:

                # add ingredients to 'ingredients' table.
                add_ingredient_query = "INSERT INTO ingredients (ingredientName) VALUES ('{ingr}')"\
                                       .format(ingr=entry)
                print(add_ingredient_query)
                try:
                    c.execute(add_ingredient_query)
                    conn.commit()
                except sqlite3.Error as er:
                    print('er:', er)
                    print("If error is 'UNIQUE constraint failed', you may ignore")

                

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit


if __name__ == "__main__":
    prompt = entry_prompt()
    prompt.prompt = "> "
    prompt.cmdloop("Starting prompt...")

conn.close()

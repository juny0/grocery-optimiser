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
        print('THE DATABASE SAYS --> er:', er)
        print("If error is 'UNIQUE constraint failed', you may ignore")

'''
This is a helper method to print out results from SQL queries
'''
def print_results(query):
    c.execute(query)
    rows = c.fetchall()
    if (len(rows) == 0):
        print("NO RESULTS FOUND. What you are looking for does not exist")
        return

    for entry in rows:
        for entry2 in entry:
            str = '{0: <20}'.format(entry2)
            print(str, end='')
        print('')


class EntryPrompt(Cmd):

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit

    def do_add_recipe(self, args):
        """
        Add a recipe to your recipe book!
        This method only takes one argument initially, and that is the recipe name.
        Spaces are allowed.
        """
        if len(args) == 0:
            print("ERROR: No recipe name was specified")
        else:
            args = args.strip().lower()
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
                add_ingredient_query = "INSERT INTO recipe_contains (recipeName, ingredientName) VALUES ('{rn}', '{ingr}')" \
                    .format(rn=args, ingr=entry)
                execute_db_query(add_ingredient_query)
                add_ingredient_query = "INSERT INTO ingredients (ingredientName) VALUES ('{ingr}')" \
                    .format(ingr=entry)
                execute_db_query(add_ingredient_query)

    def do_delete_recipe(self, args):
        """
        Delete a recipe to your recipe book!
        This method only takes one argument, and that is the recipe name.
        Spaces are allowed.
        """
        if len(args) == 0:
            print("ERROR: No recipe name was specified")
        else:
            args = args.strip().lower()
            print("Deleting %s from your recipe book (if it exists)." % args)
            # Delete recipe from the table 'recipes'
            query = """
            DELETE FROM recipes
            WHERE recipeName = '{}'
            """.format(args)
            execute_db_query(query)
            # TODO: Delete ingredient entries from the table 'ingredients' if there are no more references to it

    def do_view(self, args):
        """
        View the ingredients of a specified recipe.
        This method only takes one argument, and that is the recipe name.
        Spaces are allowed.
        """
        if len(args) == 0:
            print("ERROR: No recipe name was specified")
        else:
            args = args.strip().lower()
            # Print ingredients of recipe
            query = """
            SELECT ingredientName FROM recipe_contains
            WHERE recipeName = '{}'
            ORDER BY ingredientName
            """.format(args)
            print_results(query)

    def do_recipes_using(self,args):
        """
        View the recipes that use ALL the specified ingredient(s).
        This method takes unlimited comma-separated arguments.
        """
        if len(args) == 0:
            print("ERROR: No ingredients were specified")
        else:
            args = args.strip().lower().split(',')
            query = """
            SELECT DISTINCT recipeName FROM recipe_contains
            WHERE 
            """
            # build query string containing all ingredients
            numIngredients = len(args)
            str = ""
            count = 0
            for entry in args:
                count = count + 1
                str = str + "ingredientName = '{}'".format(entry)
                if (count < numIngredients):
                    str = str + " OR "
            query = query + str
            print_results(query)


    def do_list_recipes(self,args):
        """
        List all recipes in your catalog.
        """
        query = """
        SELECT * FROM recipes
        ORDER BY recipeName
        """
        print_results(query)

    def do_list_ingredients(self,args):
        """
        Get a list of all the ingredients used by all of the recipes in your catalog, ordered from most used to least used.
        """
        get_ingredients_query = """
        SELECT ingredientName, count(ingredientName) 
        FROM recipe_contains
        GROUP BY ingredientName
        ORDER BY count(ingredientName) DESC;
        """
        header = '{0: <20}{1: <20}'.format("Ingredient", "Number of recipes that use this")
        print(header)
        print_results(get_ingredients_query)


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
    "   FOREIGN KEY (recipeName) REFERENCES recipes(recipeName) ON DELETE CASCADE"
    ")"
)
execute_db_query(create_table_query)

# == Start command line interpreter
if __name__ == "__main__":
    prompt = EntryPrompt()
    prompt.prompt = "🍉 "
    prompt.cmdloop("Starting Grocery Optimiser, type 'help' for available commands...")

conn.close()

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
c.execute("CREATE TABLE IF NOT EXISTS ingredients (ingredientName TEXT PRIMARY KEY)")

# Creating the SQLite table 'Recipes'
c.execute("CREATE TABLE IF NOT EXISTS recipes (recipeName TEXT PRIMARY KEY)")

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

# Start command line interpreter
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
            inpt = ""
            while(True):
                inpt = input(">> ").strip().lower()
                if (inpt != "stop"):
                    # add ingredient to recipe
                    print("YAY~")
                else:
                    print("%s was added to your recipe book." % args)
                    break
            print("")

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit


if __name__ == "__main__":
    prompt = entry_prompt()
    prompt.prompt = "> "
    prompt.cmdloop("Starting prompt...")

conn.close()

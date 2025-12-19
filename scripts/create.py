import sqlite3
import os
#Define class for creating database
class DBcreator:
    #method toinitialise the database with path to sql file 
    def __init__(self, db_file):
        self.db_file = db_file
    #method to create database from your specific sql file stored in directory 
    def create_database( self):
            sql_file = os.path.join('schema', 'transcriptomics_schema.sql')
          # The SQL script to create the schema
        
            # Establishing connection to the SQLite database
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            #handle errors while creating a datbase from sql file 
            try:
                with open(sql_file, 'r') as file:
                    sql_script = file.read()
                    cursor.executescript(sql_script)  # Execute the entire script
                    conn.commit()  # Commit changes to the database
            except Exception as e:
                print(f"Error creating database: {e}")
            finally:
                conn.close()  # Close the database connection
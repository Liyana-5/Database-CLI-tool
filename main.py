import argparse
import os 
from create import DBcreator
from load import DBloader
from query import DBquery

#use agparser for commandline arguments 
def main():
    parser = argparse.ArgumentParser(description="Create and load and query a datbase" )
    parser.add_argument("--createdb", action="store_true")#stores the option --createdb
    parser.add_argument("--loaddb", action="store_true")#stores option --loaddb
    parser.add_argument("--querydb", type=int)#stores option --querydb=n 
    parser.add_argument("db_file") #take in  .db file 
    args = parser.parse_args()
    
    #create a list of files for lodaing database 
    files = [
        "Subject_example.csv",
        "HMP_transcriptome_abundance_example.tsv",
        "HMP_proteome_abundance_example.tsv",
        "HMP_metabolome_abundance_example.tsv",
        "HMP_metabolome_annotation_example.csv"
    ]

    #check if datafiles in the list for loading datas are inside the directory or not 
    for file in files:
        if not os.path.exists(file):
            print(f"Required file: '{file}' is missing from the directory.")
            return
    
    #define classes and link with agpasre
    db_creator = DBcreator(args.db_file)
    db_load = DBloader(args.db_file)
    db_query= DBquery(args.db_file)
    
    
    #check if atleast one operation is given 
    if not (args.createdb or args.loaddb or args.querydb):
        print("You must specify at least one operation")
        return

    #checks if the .db file is already present or not if the operation is not create database
    if args.createdb:
        if os.path.exists(args.db_file):
            print(f"Database '{args.db_file}' already exists.")
        else:
            db_creator.create_database()
    
    #load the datas into database only if the db exists in the directly 
    if args.loaddb:
            if not os.path.exists(args.db_file):
               print(f"Database file '{args.db_file}' does not exist. Create it first")
            else:
                db_load.connect()
                db_load.load_data()
                db_load.close()
                
    #query data only if datbase exists         
    if args.querydb:
        if not os.path.exists(args.db_file):
            print(f"Database file '{args.db_file}' does not exist. Create it first")
        else:
            db_query.connect()
            db_query.execute_query(args.querydb)
            db_query.close()    

if __name__ == "__main__":
    main()
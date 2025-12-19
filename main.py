import argparse
import os
from scripts.create import DBcreator
from scripts.load import DBloader
from scripts.query import DBquery


def check_data_files(files):
    """Check if all required data files exist."""
    missing = [f for f in files if not os.path.exists(f)]
    if missing:
        print("Missing required files:")
        for f in missing:
            print(f" - {f}")
        return False
    return True


def create_database(db_file):
    """Create the database if it does not exist."""
    if os.path.exists(db_file):
        print(f"Database '{db_file}' already exists.")
    else:
        print("Creating database...")
        db_creator = DBcreator(db_file)
        db_creator.create_database()
        print("Database created successfully.")


def load_database(db_file, files):
    """Load data into the database."""
    if not os.path.exists(db_file):
        print(f"Database '{db_file}' does not exist. Create it first.")
        return
    if not check_data_files(files):
        return

    print("Loading data into the database...")
    db_loader = DBloader(db_file)
    db_loader.connect()
    db_loader.load_data()
    db_loader.close()
    print("Data loaded successfully.")


def query_database(db_file, query_number):
    """Query the database based on the provided query number."""
    if not os.path.exists(db_file):
        print(f"Database '{db_file}' does not exist. Create it first.")
        return

    print(f"Executing query #{query_number}...")
    os.makedirs("results", exist_ok=True)  # ensure results folder exists
    db_query = DBquery(db_file)
    db_query.connect()
    db_query.execute_query(query_number)
    db_query.close()
    print(f"Query #{query_number} completed.")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create, load, and query a bioinformatics database"
    )
    parser.add_argument("--createdb", action="store_true", help="Create the database")
    parser.add_argument("--loaddb", action="store_true", help="Load data into the database")
    parser.add_argument("--querydb", type=int, help="Query the database by number")
    parser.add_argument("db_file", help="SQLite database file path")
    return parser.parse_args()


def main():
    # Define example data files
    data_files = [
        "data/Subject_example.csv",
        "data/HMP_transcriptome_abundance_example.tsv",
        "data/HMP_proteome_abundance_example.tsv",
        "data/HMP_metabolome_abundance_example.tsv",
        "data/HMP_metabolome_annotation_example.csv"
    ]

    args = parse_arguments()

    # Ensure at least one operation is specified
    if not (args.createdb or args.loaddb or args.querydb):
        print("Error: You must specify at least one operation (--createdb, --loaddb, --querydb).")
        return

    # Perform requested operations
    if args.createdb:
        create_database(args.db_file)

    if args.loaddb:
        load_database(args.db_file, data_files)

    if args.querydb is not None:
        query_database(args.db_file, args.querydb)


if __name__ == "__main__":
    main()

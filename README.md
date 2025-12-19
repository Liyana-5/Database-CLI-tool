# Bioinformatics Database CLI Tool

A **command-line Python tool** for creating, loading, and querying a biological SQLite database.  
This project uses example datasets for demonstration and produces visual outputs such as scatter plots.

## Folder Structure
```
Database-CLI-tool/
├── main.py
├── scripts/
│ ├── create.py
│ ├── load.py
│ └── query.py
├── data/
│ └── *_example.csv / .tsv # example input files
├── results/
│ └── age_bmi_scatterplot.png # example output
├── sql/
│ └── transcriptomics_schema.sql # database schema
├── README.md
├── requirements.txt
└── .gitignore
```

- The `data/` folder contains **small example datasets** to demonstrate functionality.  
- **Full datasets** are not included for size/privacy reasons.  
- Users can place real datasets in `data/` locally.

## How to Run

1. **Create the database**

```bash
python main.py --createdb my_database.db
```
2. **Load example data**

```bash
   python main.py --loaddb my_database.db
```
3. **Query the database**

```bash 
 python main.py --querydb 9 my_database.db
```


This will generate a scatter plot of age vs BMI in the results/ folder.


## Requirements

- Python 3.7+

- External packages:

  * pandas

  * matplotlib
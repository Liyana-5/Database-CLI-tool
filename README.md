# Bioinformatics Database CLI Tool

A **command-line Python tool** for creating, loading, and querying a bioinformatic SQLite database using multi-omics data.  
This utility allows users to store transcriptomics, proteomics, and metabolomics data in a structured database, and query it to extract specific insights. It also generates visual outputs such as scatter plots.

---

## Project Overview

This project implements a **bioinformatics database utility** to:

- Create a SQLite database based on a predefined schema.
- Load data from CSV and TSV files into the database.
- Execute predefined queries to fetch data and generate visualizations.

The data used in this project is from the multi-omics study "Personal Aging Markers and Ageotypes Revealed by Deep Longitudinal Profiling" (Ahadi et al., 2020). The project focuses on a subset of data required to demonstrate database operations.

---

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

---

## Features

1. **Database Creation (`--createdb`)**  
   Creates an SQLite database with tables for Subjects, Visits, Transcriptomics, Metabolomics, and Metabolite Annotations based on `transcriptomics_schema.sql`.
 **Note:** Only the columns and data needed to answer the predefined queries are populated in the database.

2. **Data Loading (`--loaddb`)**  
   Loads example CSV/TSV files into the database. Includes parsing, cleaning, and handling missing values.
**Note:** Only the required data for the queries is inserted.

3. **Data Querying (`--querydb`)**  
   Executes predefined queries. Query #9, for example, generates a scatter plot of Age vs BMI and saves it in the `result/` folder.

---


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

  install dependencies using
  ```bash
    pip install -r requirements.txt
  ```

---
## Notes

- The database uses a wide format for omics data to match the structure of input files.

- Only the columns necessary for the queries are included in the database schema.

- The program is modular: separate scripts handle creation, loading, and querying.

- All example files should be located in the data/ folder. Real datasets can be added locally.

---
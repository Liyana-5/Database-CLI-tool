import sqlite3
import re

#class for inserting datas into DATABASE 
class DBloader:
    #initialize the objects and holds cursor and connection while executing queries to load data into database 
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None
    #establish connection to datbase located at self.db_file
    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def close(self):
        #close connection to datbase by commiting changes 
        if self.conn:
            self.conn.commit()
            self.conn.close()
     #excecute insert statements inside load functions that contains optional parameters read from files 
    def execute_insert(self, insert, params=None):
        if params is None:
            self.cursor.execute(insert)
        else:
            self.cursor.execute(insert, params)
    #convert any 'NA' spaces 'Unknown' or 'unknown' in datafiles into NULL in sqldatbase 
    def missing_values(self, value):
        if value in ['NA', 'unknown', '','Unknown']:
            return None
        return value
    #inserts data into datbase 
    def insert_data(self,insert, data):
        self.execute_insert(insert, data)
    
    #I manually add datas into each tablesand the columns decided upon while creating the schema
    #method to load data into Subject table
    def load_subjects(self, file_path):
        with open(file_path, 'r') as file:
            next(file)#skip header 
            for line in file: 
                # Split the line by commas (subject is from subject.csv file so its is coma seperated file)
                fields = line.strip().split(',')
                #parse and extract all datas required to load into database 
                subject_id = fields[0]
                race = self.missing_values(fields[1])
                sex = self.missing_values(fields[2])
                age = self.missing_values(fields[3])
                bmi = self.missing_values(fields[4])
                ir_is = self.missing_values(fields[6])

                # Insert into Subjects table the values parsed and transformed from the files using INSERT statements make sure table names are correct while writting them
                #OR IGNORE is used to remoe duplicates if any is already inserted
                insert = '''
                    INSERT OR IGNORE INTO Subjects (SubjectID, Race, Sex, Age, BMI, IR_IS)
                    VALUES (?, ?, ?, ?, ?, ?)
                '''
                #inserts correspondind data inro database using insert_data method 
                self.insert_data(insert, (subject_id, race, sex, age, bmi, ir_is))

    def load_visits(self, file_paths):
        #to take all three TSV files we provide as a list of files to load visit table 
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                next(file) 
                for line in file:
                    fields = line.strip().split('\t')
                    sample_id = fields[0]
                    subject_id, visit_id = sample_id.split('-')  # Extract SubjectID and VisitID from SampleID
                    #visit has composite primary key in schema thus no duplicate sample id for a subjectid and visit id will be inserted 
                    insert = '''
                        INSERT OR IGNORE INTO Visits (VisitID, SubjectID, SampleID)
                        VALUES (?, ?, ?)
                    '''
                    self.insert_data(insert, (visit_id, subject_id, sample_id))

     #method to load load only the transcript required for the query into the datbase since no others is required 
    def load_transcriptomics(self, file_path):
        with open(file_path, 'r') as file:
            headers = file.readline().strip().split('\t')  # Read the headers

            # Extract the column index of the specific transcript ID required 
            #this logic to obtain inxes using index method in python was recieved from chatgpt4.o 
            #while headers are read this headers are stored as a list and the position of that headers can be obtained using index method in python
            #python is 0 indexed and the index of A1bG which is the second column of file is going to be 1
            #this index can be used to retrive the infrmation stored about that 
            transcript_index = headers.index('A1BG')

#terate through each lines in the file 
            for line in file:
                fields = line.strip().split('\t')
                sample_id = fields[0]  # Extract the SampleID

                # Get the measurement value for the specific transcript ID
                measurement = self.missing_values(fields[transcript_index])

                # Insert the data into the Transcriptomics table for the specific transcript
                query = f'''
                    INSERT OR REPLACE INTO Transcriptomics (SampleID,A1BG)
                    VALUES (?, ?)
                '''
                self.insert_data(query, (sample_id, measurement))
    #method to load metabolomics table with only sample ids required for query
    def load_metabolomics(self, file_path):
        with open(file_path, 'r') as file:
            next(file)  # Skip header
            for line in file:
                fields = line.strip().split('\t')
                sample_id = fields[0]

                # Insert SampleID into Metabolomics table
                insert = '''
                    INSERT OR IGNORE INTO Metabolomics (SampleID)
                    VALUES (?)
                '''
                self.insert_data(insert, (sample_id,))
    #method to insert data into anotation table 
    def load_metabolite_annotations(self, file_path):
        #function to merge metabolite names with suffixex using regex 
        def merge_metabolite_name(metabolite_name):
            #substitute function iin regex maches any name with "(number)" at the end of the name and replace it with a space 
            return re.sub(r'\(\d+\)$', '', metabolite_name)

        with open(file_path, 'r') as file:
            next(file)  # Skip header

            for line in file:
                # Split and handle missing values in one go
                fields = [self.missing_values(field) for field in line.strip().split(',')]
                #initiate fields 
                peak_id, metabolite_names, kegg_ids, hmdb_ids, chemical_class, pathway_info = fields

                # Split and clean up fields as necessary
                #the logic to assign None if there are no names in fields is taken from chatgpt4.o since there apears to be incorrect entries in KEGG and HMBD entries if not done so 
                #for every name in metabolite name the cleane up is done and the names are split at '|' if there are no names assign None
                metabolite_names = [merge_metabolite_name(name) for name in metabolite_names.split('|')] if metabolite_names else [None]
                kegg_ids = kegg_ids.split('|') if kegg_ids else [None]
                hmdb_ids = hmdb_ids.split('|') if hmdb_ids else [None]

                # Iterate over all possible combinations and insert into database
                for metabolite_name, kegg_id, hmdb_id in zip(metabolite_names, kegg_ids, hmdb_ids):
                    insert = '''
                        INSERT OR IGNORE INTO MetaboliteAnnotations 
                        (MetabolomePeakID, MetaboliteName, KEGG, HMDB,chemicalclass, Pathway)
                        VALUES (?, ?, ?, ?,?, ?)
                    '''
                    self.insert_data(insert, (peak_id, metabolite_name, kegg_id, hmdb_id,chemical_class, pathway_info))
    #method to load all datas into respective tables in database 
    def load_data(self):
        try:
            self.load_subjects('Subject.csv')
            self.load_visits(['HMP_transcriptome_abundance.tsv', 'HMP_proteome_abundance.tsv', 'HMP_metabolome_abundance.tsv'])
            self.load_transcriptomics('HMP_transcriptome_abundance.tsv')
            self.load_metabolomics('HMP_metabolome_abundance.tsv')
            self.load_metabolite_annotations('HMP_metabolome_annotation.csv')
        #capture the error and print it to the terminal
        except Exception as e:
            print(f"Error loading data: {e}")      
import sqlite3
import matplotlib.pyplot as plt

class DBquery:
    def __init__(self, db_file):
        self.db_file = db_file

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
    
    def query_results(self, query):
        # Executes the query and prints results in a tab-separated format
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print("\t".join(str(item) for item in row))
    
    
    #define statements to query the database for specific numbers 
    def execute_query(self, query_number):
        query_dict = {
             #1.Retrieve SubjectID and Age of subjects whose age is greater than 70.
            1: "SELECT SubjectID, Age FROM Subjects WHERE Age > 70",
            #2.Retrieve all female SubjectID who have a healthy BMI (18.5 to 24.9). Sort the results in descending order.
            2: "SELECT SubjectID FROM Subjects WHERE Sex = 'F' AND BMI BETWEEN 18.5 AND 24.9 ORDER BY SubjectID DESC",
            #3.Retrieve the Visit IDs of Subject 'ZNQOVZV'. This query will be easy if the Visit ID information has been correctly parsed and stored into the database
            3: "SELECT VisitID FROM Visits WHERE SubjectID = 'ZNQOVZV'",
            #4.Retrieve distinct SubjectIDs who have metabolomics samples and are insulin-resistant.
            4: """
                SELECT DISTINCT v.SubjectID 
                FROM Visits v
                JOIN Metabolomics m ON v.SampleID = m.SampleID
                JOIN Subjects s ON v.SubjectID = s.SubjectID
                WHERE s.IR_IS = 'IR'
            """,
           #5.	Retrieve the unique KEGG IDs that have been annotated for the following peaks: 
#a.	'nHILIC_121.0505_3.5'
#b.	'nHILIC_130.0872_6.3'
#c.	'nHILIC_133.0506_2.3'
#d.	'nHILIC_133.0506_4.4'

            5: """
                SELECT DISTINCT KEGG
                FROM MetaboliteAnnotations
                WHERE MetabolomePeakID IN ('nHILIC_121.0505_3.5', 'nHILIC_130.0872_6.3', 
                                           'nHILIC_133.0506_2.3', 'nHILIC_133.0506_4.4')
            """,
            #6.Retrieve the minimum, maximum and average age of Subjects
            6: " SELECT MIN(Age),MAX(Age), AVG(Age) FROM Subjects ",
            #7.Retrieve the list of pathways from the annotation data, 
            # and the count of how many times each pathway has been annotated. 
            # Display only pathways that have a count of at least 10. Order the results by the number of annotations in descending order
            7: """
                SELECT Pathway, COUNT(*) AS AnnotationCount
                FROM MetaboliteAnnotations
                WHERE Pathway IS NOT NULL
                GROUP BY Pathway
                HAVING COUNT(*) >= 10
                ORDER BY AnnotationCount DESC
            """,
           #8.	Retrieve the maximum abundance of the transcript 'A1BG' for subject 'ZOZOW1T' across all samples.

            8: """
                 SELECT MAX(A1BG)
                 FROM Transcriptomics
                 WHERE SampleID IN (
                 SELECT SampleID FROM Visits WHERE SubjectID = 'ZOZOW1T'
                 )
             """
        }
        
        #if query number is in the dictionary it executes and prints the query but if the query number is 9 it executes query_9 method 
        if query_number in query_dict:
            query = query_dict[query_number]
            self.query_results(query)
        elif query_number == 9:
            self.query_9()
        else:
            print('invalid number')
       

    def query_9(self):
       # 9.Retrieve the subjects’ age and BMI. If there are NULL values in the Age or BMI columns, that subject should be omitted from the results. 
       #At the same time, generate a scatter plot of age vs BMI using the query results from above.
      query = "SELECT Age, BMI FROM Subjects WHERE Age IS NOT NULL AND BMI IS NOT NULL"
      self.cursor.execute(query)
      results = self.cursor.fetchall()
      
      #print results and generate plot 
      if results:
        # Print results in tabseparated columns 
        for row in results:
            print("\t".join(str(item) for item in row))  # Print each row
        
        # Generate scatter plot
        ages = [row[0] for row in results]
        bmis = [row[1] for row in results]

        plt.figure(figsize=(10, 6))
        plt.scatter(ages, bmis, c='red', alpha=0.5)
        plt.title('Age vs BMI')
        plt.xlabel('Age')
        plt.ylabel('BMI')
        plt.grid(True)
        #save figure to directory
        plt.savefig('age_bmi_scatterplot.png')
        #close plot
        plt.close()
      #if there are no results collected print no data found 
      else:
        print("No data found.")
    #close connection 
    def close(self):
        self.conn.close()

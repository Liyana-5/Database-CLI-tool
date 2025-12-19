-- Subjects table
CREATE TABLE IF NOT EXISTS Subjects (
    SubjectID TEXT PRIMARY KEY,
    Race CHAR(1),
    Sex CHAR(1),
    Age FLOAT,
    BMI FLOAT,
    IR_IS CHAR(2)
);

-- Visits table
CREATE TABLE IF NOT EXISTS Visits (
    VisitID TEXT NOT NULL,
    SubjectID TEXT NOT NULL,
    SampleID TEXT UNIQUE NOT NULL, --only unique sample ids can be added no duplicates
    PRIMARY KEY (SubjectID, VisitID),-- Subject and visitid together  becomes unique for each samples 
    FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
);

-- Transcriptomics table
CREATE TABLE IF NOT EXISTS Transcriptomics (
    SampleID TEXT PRIMARY KEY,  -- Links to SampleID in Visits
    A1BG FLOAT,-- stores measurement for only transcript A1BG required for query
    FOREIGN KEY (SampleID) REFERENCES Visits(SampleID)                 
);

-- Metabolomics table
CREATE TABLE IF NOT EXISTS Metabolomics (
    SampleID TEXT NOT NULL,
    PRIMARY KEY (SampleID),
    FOREIGN KEY (SampleID) REFERENCES Visits(SampleID)
);

-- MetaboliteAnnotations table 
CREATE TABLE IF NOT EXISTS MetaboliteAnnotations (
    MetabolomePeakID TEXT NOT NULL,
    MetaboliteName TEXT,
    KEGG TEXT,
    HMDB TEXT,
    chemicalclass TEXT,
    Pathway TEXT,
    PRIMARY KEY (MetabolomePeakID, MetaboliteName)-- multiple peak can have same same metabolite and vise versa 
);

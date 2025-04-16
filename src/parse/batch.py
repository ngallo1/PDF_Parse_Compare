"""
Parse a directory of pdf files with different parsers and cache the results to a database.

How is the database built:
    1. By instructors on sample data and uploaded to git repository (currently)
    2. By student who donwloads repository and runs it locally on his data (possible)
    3. Hosted database where students upload pdfs that are processed, stored, and viewable by others (future).

"""
from pathlib import Path
# from .parse import pdf_process, PARSERS
import sqlite3
import pickle

# Development: place-holder processing function
def pdf_process(filename, parsername):
    return f"TODO: parse for filename={filename}, and parsername={parsername}"

PARSERS = ["Docling", "LlamaParse", "Mistral"]


def pdf_process_and_cache(conn, filename: str, parsername: str, overwrite=False):
    """
    Process a pdf and cache the result in a database.
    
    
    Currently, we are using default parameters of parser, hence database key is just (filename, parsername)
    Future versions should allow different parameters for the parser (and caching results
    for each parameterization)
    """
    cursor = conn.cursor()

    # Is the pdf parse already in the database
    filename_key = filename.stem
    has_parse = cursor.execute(
        '''SELECT 1 FROM pdf_parse WHERE filename = ? AND parsername = ?''',
        (filename_key, parsername)
    )

    # Do we need to write to databse or not?
    if not has_parse or overwrite:
        print(f"Working on {filename.stem}.pdf with parser {parsername}.....")

        # Result (python object) from the pdf processing algorithm
        result = pdf_process(filename, parsername)
        
        # Serialize response for storate in database
        result_serialized = pickle.dumps(result)

        # Store it in database, overwriting existing parse
        cursor.execute(
            '''REPLACE INTO pdf_parse (filename, parsername, result) VALUES (?, ?, ?)''',
            (filename_key, parsername, result_serialized)
        )
        conn.commit()



def pdf_process_and_cache_batch(conn, filenames: list, parsernames: list, overwrite=False):
    """
    Process a batch of pdfs with a batch of processing methods
    """
    for filename in filenames:
        for parsername in parsernames:
            pdf_process_and_cache(conn, filename, parsername, overwrite)



def create_database(db_path):
    """
    Create SQLite database with a table to cache PDF data.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table for 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pdf_parse (
        filename TEXT,
        parsername TEXT,
        result,
        PRIMARY KEY (filename, parsername)
    )
    ''')
    
    conn.commit()
    return conn




if __name__=="__main__":
    # Sample data from this repository
    DATA_DIRECTORY = Path(".", "data")
    
    # Create a database to store the parse results
    conn = create_database(db_path=DATA_DIRECTORY/"parsed.db")

    # All of the pdf filies in this directory
    pdf_filenames = sorted(list(DATA_DIRECTORY.glob('*.pdf')))
    
    # All of the parsers in our system
    parsernames = PARSERS

    # process and cache the batch
    pdf_process_and_cache_batch(conn, pdf_filenames, parsernames, overwrite=True)

    conn.close()

"""
Compare the results of different parsers
"""
import streamlit as st
import sqlite3


st.header("Compare PDF Parse")
st.write("Compare the PDF parse of different parsers")


from src.database import db_path

with sqlite3.connect(db_path) as conn:
    
    # Get the result of row as value not tuple
    # https://stackoverflow.com/questions/2854011/get-a-list-of-field-values-from-pythons-sqlite3-not-tuples-representing-rows
    conn.row_factory = lambda cursor, row: row[0]

    cursor = conn.cursor()
    n = cursor.execute('''SELECT COUNT (*) from pdf_parse''').fetchone()
    
    filenames = cursor.execute('''SELECT DISTINCT (filename) from pdf_parse''').fetchall()
    parsernames = cursor.execute('''SELECT DISTINCT (parsername) from pdf_parse''').fetchall()

    
    # Select filename and parser result to view
    with st.sidebar:
        filename = st.selectbox("Document Name", options=filenames)
        parsername = st.selectbox("Parser", options=parsernames)
    
    result = cursor.execute(
        '''SELECT (result) from pdf_parse WHERE filename = ? AND parsername = ?''',
        (filename, parsername)
    ).fetchone()
    
    # unpickle data to get python object
    import pickle
    result = pickle.loads(result)

    st.write(result)


def get_markdown(document, parsername):
    def get_markdown_llama(document):
        return "\n\n".join(page.text for page in document)
    
    def get_markdown_mistral(ocr_response):
        return "\n\n".join([page.markdown for page in ocr_response.pages])
    
    def get_markdown_docling(document):
        return document.export_to_markdown()

    markdown_funcs = {
        "Llama": get_markdown_llama,
        "Mistral": get_markdown_mistral,
        "Docling": get_markdown_docling,
    }

    return markdown_funcs[parsername]


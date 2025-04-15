"""
Parse a directory of pdf files with different parsers. Save result to a database.
"""
import os
from pathlib import Path
DATA_DIRECTORY = "<Your data directory>"


def pdf_process_directory(directory, parser_name):
    """
    Process all PDFs in the directory with a specific parser.
    TODO: where to store the results
    """
    # TODO: links to online sources showing how to parse this
    p = Path(directory)
    filenames = sorted(list(p.glob('*.pdf')))

    parse = {
        "Llama": llama_pdf_process,
        "Mistral": mistral_pdf_process,
    }[parser_name]

    documents = {}
    for filename in filenames:
        print(filename.stem)
        documents[filename.stem] = parse(filename)
    return documents


def pdf_parse_with_all_parsers(filename):
    """
    Parse one file with all parsers.
    
    Future Usage: Someone can upload a pdf, run it through all parsers and visualize results with GUI to compare
    TODO: highlight
    """
    pass

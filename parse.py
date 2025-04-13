"""
Parse all of the documents in our database with all of the parsers
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Bring in parsinng libraries
from llama_cloud_services import LlamaParse
from mistralai import Mistral

# Need this?
# from llama_parse import LlamaParse
# from llama_index.core import SimpleDirectoryReader



load_dotenv()

import nest_asyncio; nest_asyncio.apply()  # Need for LlamaParse loop?



def llama_pdf_process(filename):
    """
    Process the pdf with LlamaParse
    """
    return LlamaParse(result_type="markdown").load_data(filename)


def mistral_pdf_process(filename):
    """
    Process the pdf with mistral
    """
    # Mistral sample code
    # https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/ocr/structured_ocr.ipynb#scrollTo=dxefUpm-Idp8

    api_key = None
    client = Mistral(api_key=api_key)

    uploaded_pdf = client.files.upload(
        file={
            "file_name": "hello.pdf",  # <-- need?
            "content": open(filename, "rb"),
        },
        purpose="ocr"
    )  

    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
    return client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        }
    )


def docling_pdf_process(filename):
    pass

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



DATA_DIRECTORY = "<Your data directory>"
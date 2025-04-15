"""
Parse all of the documents in our database with all of the parsers.
"""
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
    # TODO: sample code?
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


def docling_pdf_process(filename, opts=None):
    pass


def pdf_process(service_name, opts=None):
    """
    Main function to process a PDF using one of the services
    """
    pass


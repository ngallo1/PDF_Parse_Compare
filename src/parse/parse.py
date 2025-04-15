"""
Parse all of the documents in our database with all of the parsers.
"""
from dotenv import load_dotenv

# Bring in parsinng libraries
from unstructured.partition.pdf import partition_pdf
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

def unstructured_pdf_process(filename, strategy="fast", opts=None):
    """
    Process a PDF file using unstructured library and return markdown content.
    
    Required Libraries:
        pdfminer.six
        unstructured.partition.pdf
        pi_heif
        unstructured_inference
        pdf2image
    Args:
        filename (str): Path to the PDF file
        opts (dict, optional): Additional options for processing
        
    Returns:
        str: Markdown formatted text content
    """
    
    elements = partition_pdf(
        filename=filename,
        strategy=strategy, 
        extract_images_in_pdf=True
    )
    
    markdown_content = "\n\n".join(str(element) for element in elements)
    
    return markdown_content

def calqwen_pdf_process(filename, opts=None):
    pass

def pdf_process(service_name, opts=None):
    """
    Main function to process a PDF using one of the services
    """
    pass

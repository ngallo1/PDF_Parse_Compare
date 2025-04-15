from unstructured.partition.pdf import partition_pdf


def unstructured_pdf_process(filename, opts=None):
    """
    Process a PDF file using unstructured library and return markdown content.
    
    Args:
        filename (str): Path to the PDF file
        opts (dict, optional): Additional options for processing
        
    Returns:
        str: Markdown formatted text content
    """

    # Extract elements from PDF
    elements = partition_pdf(
        filename=filename,
        strategy="fast", 
        extract_images_in_pdf=True 
    )
    
    # Convert elements to markdown by joining their string representations
    markdown_content = "\n\n".join(str(element) for element in elements)
    
    return markdown_content

print(unstructured_pdf_process("PDF_Parse_Compare\src\data\electrical_001.pdf"))
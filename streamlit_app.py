import streamlit as st
import pickle

# Test
# Test - Bryce
# Test - Bryce 2222222
# Test - Bryce 3

# Test - Nick
# Test - Nick 2
# Test - Nick 3

st.set_page_config(
    page_title="Compare Parsers",
    layout="wide"
)
 
st.header("Compare PDF Parse")

st.write("Compare the PDF parse of different parsers")

# ---------   Data 
@st.cache_data
def load_parsed_documents():
    """Load documents already parsed with different parsers."""
    import pickle

    pickle_filenames = {
        'Docling': './data/docling_docs.pkl',
        'Mistral': './data/mistral_docs.pkl',
        'Llama': './data/llama_docs.pkl',
    }

    parsed_documents = {}
    for parser_name, filename in pickle_filenames.items():
        with open(filename, 'rb') as f:
            parsed_documents[parser_name] = pickle.load(f)

    return parsed_documents


parsed_documents = load_parsed_documents()
parsers = list(parsed_documents.keys())
# TODO: ensure all are the same
DB_DOCUMENT_NAMES = parsed_documents[parsers[0]].keys()

def get_different_parses_of_document(document_name, as_markdown=False):
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

    out = {}
    for parser in parsers:
        out[parser] = parsed_documents[parser][document_name]
        if as_markdown:
            out[parser] = markdown_funcs[parser](out[parser])

    return out

with st.sidebar:
    document_name = st.selectbox("Document Name", options=DB_DOCUMENT_NAMES)
    parser = st.selectbox("Parser", options=parsers)

markdowns = get_different_parses_of_document(document_name, as_markdown=True)
 
# tabs = st.tabs(parsers)
# for parser, tab in zip(parsers, tabs):
#     st.markdown(markdowns[parser])
st.divider()
st.markdown(markdowns[parser])

# print(tabs[0])

#print(documents)
# st.write(document_name)



#st.write(DB_DOCUMENT_NAMES)
#st.write(parsed_documents[parser].keys() for parser in parsers)
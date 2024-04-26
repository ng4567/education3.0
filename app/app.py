import streamlit as st
import pandas as pd
import re
from io import StringIO, BytesIO
from utils import groq_helper
import PyPDF2

def extract_text_from_pdf(pdf_bytes):
    pdf_reader = PyPDF2.PdfReader(pdf_bytes)
    num_pages = len(pdf_reader.pages)
    text = ''
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        text += page_text
    return text

pdf_file = st.file_uploader('Upload your pdf', type=['pdf'])

if pdf_file is not None:
    # Convert the BytesIO object to a buffered reader
    pdf_bytes = BytesIO(pdf_file.getvalue())
    extracted_text = extract_text_from_pdf(pdf_bytes)
    response = groq_helper(f"""Below I will input extracted text from a Math textbook. Return me a list of all the homework problems:

{extracted_text}

Homework problems:

""", max_tokens=8000)
    st.write(response.choices[0].message.content)

# #pdf_file = '../data/hw_problems.pdf'
# extracted_text = extract_text_from_pdf(pdf_file)

# response = groq_helper(f"""Below I will input extracted text from a Math textbook. Return me a list of all the homework problems:
            
#             {extracted_text}
            
#             Homework problems:
#             """, max_tokens=8000)

# st.write(response.choices[0].message.content)


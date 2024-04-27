import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
from utils import groq_helper, set_shared_variable, parse_problems, init_state, extract_text_from_pdf, get_shared_variable

#Simple app to extract the math problems from an uploaded PDF file of a math textbook
def app():
    init_state()

    st.title("Education 3.0")

    # Link to textbook used in testing
    link_to_data = "https://github.com/ng4567/education3.0/blob/main/data/hw_problems.pdf"
    st.markdown(f'<label for="file_uploader">Note: This app is a WIP. It is not guaranteed to work with large files or other textbooks, and so far has only been tested on the following input: <a href="{link_to_data}" target="_blank">Link</a></label>', unsafe_allow_html=True)
    pdf_file = st.file_uploader('Upload your textbook', type=['pdf'])



    if pdf_file is not None:
        # Convert the BytesIO object to a buffered reader
        pdf_bytes = BytesIO(pdf_file.getvalue())
        extracted_text = extract_text_from_pdf(pdf_bytes)
        response = groq_helper(f"""Below I will input extracted text from a Math textbook. Return me a list of all the homework problems:

    {extracted_text}

    Homework problems:

    """, max_tokens=8000)
        st.header("Extracted Homework Problems:")
        st.write(response.choices[0].message.content)
        
        st.subheader("Below are all the parsed algebraic problems:")
        set_shared_variable('textbook_text', response)
        text_extract = get_shared_variable('textbook_text', "YOU DIDN'T UPLOAD A TEXTBOOK")
        
        problems = parse_problems(text_extract.choices[0].message.content)
        set_shared_variable('algebraic_problems', problems)
        
        
        st.write(problems)
        

if __name__ == "__main__":
    app()


# #pdf_file = '../data/hw_problems.pdf'
# extracted_text = extract_text_from_pdf(pdf_file)

# response = groq_helper(f"""Below I will input extracted text from a Math textbook. Return me a list of all the homework problems:
            
#             {extracted_text}
            
#             Homework problems:
#             """, max_tokens=8000)

# st.write(response.choices[0].message.content)


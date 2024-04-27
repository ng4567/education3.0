import streamlit as st 
from utils import parse_problems, get_shared_variable


def app():
    
    st.header("Lesson Planner")
    

    text_extract = get_shared_variable('textbook_text', "YOU DIDN'T UPLOAD A TEXTBOOK")
    
    if text_extract != "YOU DIDN'T UPLOAD A TEXTBOOK":
        st.subheader("Below are all the algebraic problems:")
        
        problems = parse_problems(text_extract.choices[0].message.content)
        
        st.write(problems)
        
        
    else:
        st.write("You must upload a file on the home page for this page to work")
        st.write("YOU DIDN'T UPLOAD A TEXTBOOK")
        st.write("Click here to go back to the homepage and upload one:")
        st.page_link('1-home.py', label="Home Page", icon='🏠')

    
if __name__ == "__main__":
    app()
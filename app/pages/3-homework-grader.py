import streamlit as st 
from utils import get_shared_variable
st.title('Test Grader')

questions = get_shared_variable('questions', [])
if len(questions) > 0:
    st.write('Here are the homework problems you saved:')
    st.write(questions)
else:
    st.write('There are no imported questions!')

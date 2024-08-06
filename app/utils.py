import os
from groq import Groq
from dotenv import load_dotenv
import streamlit as st
import PyPDF2
import re
from typing import Union

load_dotenv()

def groq_helper(prompt: str, **kwargs):
    """
    Helper function to simplify making requests to the Groq API for chat completions.

    Parameters:
    prompt (str): Text of prompt to be inputted to model
    

    Args:
        prompt (str): The input text for the chat completion.
        **kwargs: Optional keyword arguments to customize the chat completion request.
            role (str): The role of the input prompt (e.g., 'user' or 'assistant'). Default is 'user'.
            modelid (str): The ID of the language model to use for the chat completion. Default is 'mixtral-8x7b-32768'.
            temperature (float): The sampling temperature for the language model. Default is 0.7.
            top_p (float): The cumulative probability for top-p sampling. Default is 1.0.
            max_tokens (int): The maximum number of tokens to generate in the chat completion. Default is 500.
            stop_sequences (list or None): The sequences at which to stop generating text. Default is None.
            stream (bool): Whether to stream the chat completion response or not. Default is False.

    Returns:
        A grok chat completion object. Use .choices[0].message.content to get just the text of the return.
    """
        
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    )

    role = kwargs.get('role', 'user')
    modelid = kwargs.get('modelid', 'mixtral-8x7b-32768')
    temperature = kwargs.get('temperature', 0.7)
    top_p = kwargs.get('top_p', 1.0)
    max_tokens = kwargs.get('max_tokens', 2000)
    stop_sequences = kwargs.get('stop_sequences', None)
    stream = kwargs.get('stream', False)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": role,
                "content": prompt,
            }
        ],
        model=modelid,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        stop=stop_sequences,
        stream=stream,
        seed=1234
    )

    return chat_completion

def extract_text_from_pdf(pdf_bytes):
    pdf_reader = PyPDF2.PdfReader(pdf_bytes)
    num_pages = len(pdf_reader.pages)
    text = ''
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        text += page_text
    return text

#shared variables handing with Streamlit Session States
def init_state():
    if "shared_state" not in st.session_state:
        st.session_state.shared_state = {}

    
def set_shared_variable(variable_name: str, value):
    init_state()  # Ensure shared_state is initialized
    st.session_state.shared_state[variable_name] = value

def get_shared_variable(variable_name: str, default_value=None):
    init_state()  # Ensure shared_state is initialized
    return st.session_state.shared_state.get(variable_name, default_value)


def parse_problems(text):
    '''
    return a dictionary with key of problem number and values of the problem from inputted text
    '''
    
    pattern = r'(\d+)\.\s*Solve for ([a-z]):(.+)'
    problems = {}

    for line in text.strip().split('\n'):
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            problem_num = int(match.group(1))
            variable = match.group(2)
            expression = match.group(3).strip()
            problems[problem_num] = expression

    return problems


class question:
    def __init__(self, type: str, problem_number: Union[str, int], problem: str):
        self.type = type
        self.problem_number = problem_number
        self.problem = problem

def parse_questions(response_text):
    questions = []
    pattern = r'(\d+\.)\s*(.+?)\n'
    matches = re.finditer(pattern, response_text, re.MULTILINE)

    for match in matches:
        problem_number = match.group(1).strip('.')
        problem = match.group(2).strip()
        question_type = 'math'  # change this later
        question_obj = question(question_type, problem_number, problem)
        questions.append(question_obj)

    return questions


def parse_homework_problems(homework_str):
    # Define the regex pattern to match the problem number and the problem
    pattern = r'(\d+\.\d+|\d+)\.\s*(.*?)(?=\d+\.\d+|\d+\.\d+|\d+\.$|$)'    
    # Find all matches using the regex pattern
    matches = re.findall(pattern, homework_str, re.DOTALL)
    
    # Create a dictionary from the matches
    problems_dict = {num: problem.strip() for num, problem in matches}
    
    return problems_dict


if __name__ == "__main__":
    init_state()
    
    a = parse_questions(""" 
                
                Exam questions:
                
                1. 4x+b=c
                2. 5x+4=10
                3. 6x+13 = 34
                
                
                """)
    
    print()
    
    
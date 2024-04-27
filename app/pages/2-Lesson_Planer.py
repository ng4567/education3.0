import streamlit as st 
from utils import parse_problems, get_shared_variable, groq_helper


def app():
    
    st.title("Chat with Lesson Planner Assistant:")
    
    

    problems = get_shared_variable('algebraic_problems', {})



    
    if len(problems) > 0:
        st.header("Lesson Planner chatbot:") 
        
        
        if 'msg_counter' not in st.session_state:
            st.session_state.msg_counter = 1
        # Initialize chat history and default message
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"""I am an intelligent AI assistant that can help you plan lessons based on the curriculum in your textbook! Leveraging the power of RAG, I am aware of the contents of your uploaded textbook. For example, here are the algebra problems I was able to parse from it:
                {problems}
                
                """
            })

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        
            
        # React to user input
        if prompt := st.chat_input("What do you want to ask the LLM?"):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            
            
            st.session_state.messages.append({"role": "user", 
                                              "content": prompt,
                                              'user_message_no': st.session_state.msg_counter})
            
            textbook_text = get_shared_variable('textbook_text', 'blank')
            prompt_for_model = f'''
            
            
            You are a helpful assistant that helps math teachers plan lessons. Below is an excerpt from a textbook that a teacher is using to plan a lesson:
        
            {textbook_text}
            
            You will recieve multiple messages throughout the conversation. Here is a list of the previous messages and your responses:
            
            {st.session_state.messages}
            
            Below the teacher will input their query to you:        
            ''' + prompt
            
            
            response = groq_helper(prompt=prompt_for_model)
            llm_response = response.choices[0].message.content
            with st.chat_message("assistant"):
                st.markdown(llm_response)
            # Add LLM response to chat history
            st.session_state.messages.append({"role": "assistant", 
                                              "content": llm_response,
                                              "assistant_msg_counter": st.session_state.msg_counter})
            st.session_state.msg_counter += 1
            print(st.session_state.messages)
    
    
        try:
            print('1')
        except:
            st.error("Unable to call LLM API. Try again later.")
                
        
    else:
        st.write("You must upload a file on the home page for this page to work")
        st.write("YOU DIDN'T UPLOAD A VALID TEXTBOOK")
        st.write("Click here to go back to the homepage and upload one:")
        st.page_link('1-home.py', label="Home Page", icon='🏠')

        st.write("Current Streamlit Session State: ")
        st.write(st.session_state)
        
        
        
        
if __name__ == "__main__":
    app()
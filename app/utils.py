import os
from groq import Groq

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
    groq_api_key = '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'
    os.environ["GROQ_API_KEY"] = groq_api_key
        
    client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    )

    role = kwargs.get('role', 'user')
    modelid = kwargs.get('modelid', 'mixtral-8x7b-32768')
    temperature = kwargs.get('temperature', 0.7)
    top_p = kwargs.get('top_p', 1.0)
    max_tokens = kwargs.get('max_tokens', 500)
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
        stream=stream
    )

    return chat_completion


if __name__ == "__main__":
    response = groq_helper("What is the capital of South Korea?")
    print(response.choices[0].message.content)
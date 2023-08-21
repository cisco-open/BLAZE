from langchain import OpenAI
from langchain import PromptTemplate
import os

openai_key = ""
prompt_dict = {
    "actionables":"Please provide a actionables of the following text",
    "agenda":""
}
def summarize_basic(text):
    print(text)
    llm = OpenAI(temperature=0, openai_api_key=openai_key)
    prompt = """
    Please provide a summary of the following text

    TEXT:
    Philosophy (from Greek: φιλοσοφία, philosophia, 'love of wisdom') \
    is the systematized study of general and fundamental questions, 
    """

    num_tokens = llm.get_num_tokens(prompt)
    print (f"Our prompt has {num_tokens} tokens")
    output = llm(prompt)
    return output


allowed_methods = {
    "summary":summarize_basic
}

import gradio as gr
import requests
import tiktoken

from Kai.answer import format_prompt_for_llama2chat, generate_response_amd, query_db_for_context
from Kai.ingest_data import add_chunk_text_to_db_with_meta
from thunderbird.query_sql_db import get_calander_obj, get_emails_obj

url = f"http://127.0.0.1:8000/chat/"
encoding = tiktoken.encoding_for_model("gpt-4")

# def respond(message, chat_history, query_db):
#     if chat_history == []:
#         chat_history.append({"role": "system", "content": "You're a chatbot designed to run on AMD AI processor"})

#     messages = chat_history
#     messages.append({"role", "user", "content", message})
#     print(query_db)
#     if query_db:
#         context = query_db_for_context(message)
#     else:
#         context = ""
#     if context != "":
#         messages.append({"role": "context", "content": context})
    
#     print(messages)
#     print("\n\n=======Chat History=======\n")
#     print(chat_history)
#     url = f"http://127.0.0.1:8000/chat/"
#     with requests.post(url, json = {"prompt": messages, "max_new_tokens":50}, stream=True) as r:
#         for chunk in r.iter_content(1024):
#             yield chunk

def chat_history_to_prompt(chat_history):
    system_prompt = {"role": "system", "content": "You're a chatbot designed to run on AMD AI processor"}
    if chat_history == []:
        messages_with_system_prompt = [system_prompt]
    else:
        # First one is always system prompt
        messages_with_system_prompt = sum([
            [{"role": "user", "content": exchange[0]}, {"role": "assistant", "content": exchange[1]}] for exchange in chat_history],
             [system_prompt])
    return messages_with_system_prompt

def respond(message, chat_history, query_db):
    print(chat_history)
    print("\n=======Chat History END=======\n")

    # Append chat history into new prompt for LLM as reference
    formatted_prompt = chat_history_to_prompt(chat_history)
    if query_db:
        #Query similar context found in ChromaDB (Emails and calender events)
        print("====> Querying DB :D")
        context, context_subjects, context_links = query_db_for_context(message)
    else:
        context = ""
    messages = formatted_prompt + [{"role": "user", "content": message}]
    if context != "":
        #send context to LLM for emails/calender info related response
        messages.append({"role": "context", "content": context})
    
    print(messages)
    partialText = ""
    contextURL =""
    if len(context_subjects) >0:
        contextURL = f"\n External Reference:"
        for i in range(len(context_subjects)):
            if context_links[i] == "":
                contextURL += f"\n\t- {context_subjects[i]}"
            else:
                contextURL += f"\n\t- <a href=\"{context_links[i]}\" target=\"_blank\">{context_subjects[i]}</a>"
    #Acquire output token size dynamically based on input length
    encoded_tokens = encoding.encode(message, disallowed_special=())
    total_token_limit = 500
    # Calculate the remaining tokens available for the response
    input_length = len(encoded_tokens)
    max_output_tokens = total_token_limit - input_length
    max_output_tokens = min(max_output_tokens, total_token_limit) 
    print(f"Output Token size: {max_output_tokens}, input size: {input_length}")
    
    #sending POST request to backend to get LLAMA3 model responses
    with requests.post(url, json = {"prompt": messages, "max_new_tokens":max_output_tokens}, stream=True) as r:
        for chunk in r.iter_content(1024):
            partialText = chunk.decode('utf-8')
            yield partialText + contextURL
            
            
def store_db_data(is_thunderbird= True):
    if(is_thunderbird):
        print("Storing Emails and Events data into DB...")
        email_objs = get_emails_obj()
        for email in email_objs:
            add_chunk_text_to_db_with_meta(email.get_content(), email.get_meta())
        event_objs = get_calander_obj()
        for event in event_objs:
            add_chunk_text_to_db_with_meta(event.get_content(), event.get_meta())
        print("Today Emails and Events are stored into DB!")
    else:
        print("Future Implementation for other specific email/calender serviceses...")

store_db_data()

demo = gr.ChatInterface(respond,
                        chatbot=gr.Chatbot(sanitize_html=False),
    additional_inputs = [
        gr.Checkbox(label="Query vector DB", value=True)]).queue()

demo.launch(inline=True, server_port=7860)

# import random
# import gradio as gr
# def alternatingly_agree(message, history):
#     print(history)
#     print(message)
#     if len(history) % 2 == 0:
#         return f"Yes, I do think that '{message}'"
#     else:
#         return "I don't think so"
# gr.ChatInterface(alternatingly_agree).launch()

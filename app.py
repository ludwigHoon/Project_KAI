import gradio as gr

from Kai.answer import format_prompt_for_llama2chat, generate_response_amd, query_db_for_context
from Kai.search import search_and_add_to_db


def respond(message, chat_history, query_db):
    print(query_db)
    if query_db:
        context = query_db_for_context(message)
    else:
        context = ""
    print(context)
    history = "\n".join(chat_history[:-3])
    print(history)
    full_prompt = format_prompt_for_llama2chat(message, context, history)

    response = generate_response_amd(full_prompt)
    for temp in response:
        yield temp

demo = gr.ChatInterface(respond,
    additional_inputs = [
        gr.Checkbox(label="Query vector DB", value=True)]).queue()

search_and_add_to_db("intc")

demo.launch()

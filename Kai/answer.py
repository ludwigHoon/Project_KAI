import loguru
from .ingest_data import client
from chromadb.utils import embedding_functions


import os
os.environ['HF_HOME'] = './hf'

def format_prompt_for_llama2chat(
    question,
    context="", # info query froom DB
    history="",
    system_prompt="You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information. Do not use information not provided in context.",
):
    full_prompt = [{"role": "system", "content": "You're a chatbot designed to run on AMD AI processor"}]
    context_string = ""
    if context != "":
        prompt += f"\n\nContext: {context}"
    if history != "":
        prompt += f"\n\nHistory: {history}"
    full_prompt = f"""[INST] <<SYS>>
{system_prompt}
<</SYS>>
{prompt}[/INST]
"""

    # edit so that instead of the stupid string, return: [{"role": "system", "content": "You're a chatbot designed to run on AMD AI processor"},
    # {"role":"user", "content": "What is AMD?
    # context: "},
    # {"role": "assistant", "content": "......."}, ......  <- must end of {"role": "user", "content" : "....."}]
    

    return full_prompt


def query_db_for_context(question, n_results=5, max_distance = 0.5): #using cosine, score range from 0 - 1 (higher score = less semantically similar)
    collection = client.get_or_create_collection(name="KAI", metadata={"hnsw:space": "cosine"}, embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="multi-qa-MiniLM-L6-cos-v1"))
    context = collection.query(
        query_texts=question,
        n_results=n_results,
        include=["documents", "distances", "metadatas"]
    )
    #Filtering documents with a score less than min_score
    filtered_pos = [i for i in range(len(context["distances"][0]))
                    if context["distances"][0][i] <= max_distance]
    print(context)
    docs = [context["documents"][0][i] for i in filtered_pos]
    context_text = "\n\n".join(docs)
    context_subject = [context["metadatas"][0][i]["subject"] for i in filtered_pos]
    context_links = [context["metadatas"][0][i]["thunderlink"] for i in filtered_pos]
    print(f"Context text: {context_text}")
    print(f"\nContext subject and Link: {context_subject}\n\n {context_links}\n\n")
    return context_text, context_subject, context_links


def generate_response_amd(prompt: str):
    # pass the prompt to API: url = f"http://127.0.0.1:8000/chat/"
    # something like:
    # with requests.post(url, json = {"prompt": "What is AMD?"}, stream=True) as r:
    # get response from streaming and push chunks of response to GUI.
    from threading import Thread

    from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer  # To change
    loguru.logger.debug(prompt)
    model_name_or_path = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ" # TheBloke/Llama-2-7B-Chat-AWQ
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="cuda")
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    encodeds = tokenizer(
        prompt,
        return_tensors='pt'
    ).input_ids.cuda()
    print("ENCODED")
    # Generate output
    def generate_and_signal_complete():
        model.generate(encodeds, streamer=streamer, max_new_tokens=1000, do_sample=True)

    t1 = Thread(target=generate_and_signal_complete)
    t1.start()
    print("STARTED thread")
    partial_text = ""
    for new_text in streamer:
        partial_text += new_text
        print(partial_text)
        yield partial_text

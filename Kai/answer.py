import os
os.environ['HF_HOME'] = './hf'
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer # To check
from ingest_data import client
model_name_or_path = "TheBloke/Llama-2-7B-Chat-AWQ" ## Since AMD's is llama2, quantise by 2 different libraries, but on the same principles, so output should be more or less the same

device = "cuda" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained(model_name_or_path)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

question = "Can you tell me something about AMD?"
collection = client.get_or_create_collection(name="KAI")
context = collection.query(
    query_texts=question,
    n_results = 2,
    include=["documents"]
)

context_text = "\n\n".join([a for a in context["documents"][0]])

prompt = f"""Question: {question}
Context:
{context_text}
"""
prompt_template=f'''[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>
{prompt}[/INST]

'''

encodeds = tokenizer(
    prompt_template,
    return_tensors='pt'
).input_ids.cuda()

model.to(device)
# Generate output
generation_output = model.generate(encodeds, streamer=streamer, max_new_tokens=1000, do_sample=True)

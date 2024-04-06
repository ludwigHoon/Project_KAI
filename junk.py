import os
os.environ['HF_HOME'] = './hf'

from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer # To check
from ingest_data import client

model_name_or_path = "TheBloke/Llama-2-7B-Chat-AWQ" ## Since AMD's is llama2, quantise by 2 different libraries, but on the same principles, so output should be more or less the same
# TheBloke/Mistral-7B-Instruct-v0.2-AWQ
device = "cuda" # the device to load the model onto; AMD NPU seems to be "aie" <- whether this would enable the awq model load is unknown
# Whether "aie" device can be used by torch arbitarily is unknown, but if it does,
# it would make sense to also implement custom embedding function for chromadb <- improve efficiency of embedding operation

model = AutoModelForCausalLM.from_pretrained(model_name_or_path)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

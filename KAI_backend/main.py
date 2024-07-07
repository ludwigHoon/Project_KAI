import quantize_and_load as ql
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from threading import Thread
from transformers import TextIteratorStreamer
from pydantic import BaseModel
from typing import Union

app = FastAPI()

class ChatRequest(BaseModel):
    prompt: Union[str, list]
    max_new_tokens: Union[int, None] = 256
    do_sample: Union[bool, None] = True
    temperature: Union[float, None] = 0.7
    top_p: Union[float, None] = 0.9

model, tokenizer = ql.run_model()
#from transformers import AutoModelForCausalLM, AutoTokenizer
#model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
#tokenizer = AutoTokenizer.from_pretrained(model_name)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

def generate_response(formatted_prompt: str, max_new_tokens: int = 1000, do_sample: bool = True, temperature: float = 0.7, top_p: float = 0.9):
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    encodeds = tokenizer(
        formatted_prompt,
        return_tensors='pt'
    ).input_ids

    def generate_and_signal_complete(encodeds, max_new_tokens, do_sample,
        temperature=0.7, top_p=0.9):
        model.generate(encodeds, streamer=streamer, max_new_tokens=max_new_tokens, do_sample=do_sample,
            eos_token_id=terminators, temperature=temperature, top_p=top_p)

    t1 = Thread(target=generate_and_signal_complete, kwargs=dict(encodeds=encodeds, max_new_tokens=max_new_tokens, do_sample=do_sample,
        temperature=temperature, top_p=top_p))

    t1.start()
    partial_text = ""
    lstrip_once = False
    for new_text in streamer:
        partial_text += new_text
        if not lstrip_once:
            partial_text = partial_text.lstrip()
            lstrip_once = True
        print(partial_text)
        yield partial_text

@app.post("/chat/")
async def chat(c_request: ChatRequest):
    formatted_prompt = c_request.prompt
    max_new_tokens = c_request.max_new_tokens
    do_sample = c_request.do_sample
    temperature = c_request.temperature
    top_p = c_request.top_p
    if isinstance(formatted_prompt, list):
        formatted_prompt = tokenizer.apply_chat_template(
            formatted_prompt,
            add_generation_prompt=True,
            tokenize=False)
        formatted_prompt += "<|start_header_id|>assistant<|end_header_id|>"
    print(formatted_prompt)
    return StreamingResponse(
        generate_response(formatted_prompt, max_new_tokens, do_sample, temperature=temperature, top_p=top_p), media_type="text/plain")


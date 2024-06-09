import quantize_and_load as ql
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from threading import Thread
from transformers import TextIteratorStreamer
from pydantic import BaseModel
from typing import Union

app = FastAPI()

class ChatRequest(BaseModel):
    formatted_prompt: str
    max_new_tokens: Union[int, None] = 150
    do_sample: Union[bool, None] = True


def generate_response(formatted_prompt: str, max_new_tokens: int = 1000, do_sample: bool = True):
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    encodeds = tokenizer(
        formatted_prompt,
        return_tensors='pt'
    ).input_ids

    def generate_and_signal_complete(encodeds, max_new_tokens, do_sample):
        model.generate(encodeds, streamer=streamer, max_new_tokens=max_new_tokens, do_sample=do_sample)

    t1 = Thread(target=generate_and_signal_complete, args=(encodeds, max_new_tokens, do_sample))
    t1.start()
    partial_text = ""
    for new_text in streamer:
        partial_text += new_text
        yield partial_text

model, tokenizer = ql.run_model()

@app.post("/chat/")
async def chat(c_request: ChatRequest):
    formatted_prompt = c_request.formatted_prompt
    max_new_tokens = c_request.max_new_tokens
    do_sample = c_request.do_sample
    return StreamingResponse(generate_response(formatted_prompt, max_new_tokens, do_sample), media_type="text/plain")


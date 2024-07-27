import base64
from io import BytesIO
import quantize_and_load as ql
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from threading import Thread
from transformers import TextIteratorStreamer, AutoFeatureExtractor
from PIL import Image
from torchvision import transforms
import numpy as np
from pydantic import BaseModel
from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

app = FastAPI(port = 8000)
# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000", 
    "http://localhost:8000",
    "http://127.0.0.1:8000/feeling",
    "http://127.0.0.1:8000/feeling/",
    "*"
    # Add more origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class ChatRequest(BaseModel):
    prompt: Union[str, list]
    max_new_tokens: Union[int, None] = 256
    do_sample: Union[bool, None] = True
    temperature: Union[float, None] = 0.7
    top_p: Union[float, None] = 0.9

# load and run the llama 3 LLM model
model, tokenizer = ql.run_model()

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

img_model = "Xenova/facial_emotions_image_detection"
def load_img_onnx_model():
    # load onnx quantized facial emotion model from Hunggign face
    import onnxruntime as ort
    from huggingface_hub import hf_hub_download
    feature_extractor = AutoFeatureExtractor.from_pretrained(img_model)
    session = ort.InferenceSession(
        hf_hub_download(repo_id=img_model, filename="onnx/model_fp16.onnx"),
        providers=["VitisAIExecutionProvider"],
        provider_options=[{"config_file":".\\vaip_config.json"}])
    return session, feature_extractor

img_session, extractor = load_img_onnx_model()

def generate_response(formatted_prompt: str, max_new_tokens: int = 1000, do_sample: bool = True, temperature: float = 0.7, top_p: float = 0.9):
    ## uses to response a prompt from user
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

@app.get("/")
def return_home():
    return FileResponse("../KAI_frontend_app/test_gradio_iframe.html")


@app.post("/feeling/")
def feeling_from_image(snapimg: UploadFile):
    return {"emotion":predict_from_image(snapimg.file)}

def predict_from_image(img):
    image = Image.open(img).convert('RGB')
    normalize = transforms.Normalize(mean=extractor.image_mean, std=extractor.image_std)
    transform = transforms.Compose([
        transforms.Resize((extractor.size["height"], extractor.size["height"])),
        # transforms.RandomRotation(90),
        # transforms.RandomAdjustSharpness(2),
        # transforms.RandomHorizontalFlip(0.5),
        transforms.ToTensor(),
        normalize
    ])
    tensor = transform(image)
    batch_tensor = tensor.unsqueeze(0)
    batch_tensor = batch_tensor.float()
    #featured_extracted = extractor(batch_tensor)
    outputs = img_session.run(None, {'pixel_values': np.array(batch_tensor)})
    translated_emotions = ["sad", "disgust", "angry", "neutral", "fear", "surprise", "happy"]
    result = [translated_emotions[np.argmax(a)] for a in outputs][0]
    print(outputs)
    print(result)
    return result
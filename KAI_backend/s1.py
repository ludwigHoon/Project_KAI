from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import torch


from pre_quant import run_awq, apply_awq
from quantizer import real_quantize_model_weight
from qmodule import WQLinear
import qlinear

import sys
from utils import Utils
import gc

model_name = "meta-llama/Meta-Llama-3-8B-Instruct" # "meta-llama/Llama-2-7b-chat-hf" #
AWQ_CACHE = os.environ.get("AWQ_CACHE")
AWQ_FILE = "llama3-instruct-8b-w4-g128.pt" # "llama-2-7b-chat-w4-g128.pt" # 
ckpt_folder = "ckpt/"
ckpt = ckpt_folder + "llama3-instruct-8b-w4-g128.pt" # "llama-2-7b-chat-w4-g128.pt" # 

def quantize_model():
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print(model)
    q_config = {
        "zero_point": True,
        "q_group_size": 128,  }
    awq_result = torch.load(AWQ_CACHE + AWQ_FILE, map_location='cpu')
    apply_awq(model, awq_result)
    real_quantize_model_weight(
        model, w_bit=4, q_config=q_config
    )
    Utils.replace_node( model, 
        WQLinear, 
        qlinear.QLinearPerGrp, 
        (), {'device':'cpu', 'w_bit':4, 'group_size':128} )
    ## Matmul group <- skip for now
    ## Not sure if this causes error: RuntimeError: The size of tensor a (4096) must match
    ## the size of tensor b (524288) at non-singleton dimension 1
    Utils.replace_node( model, 
        torch.nn.Linear, 
        qlinear.QLinearPerGrp, 
        (), {'device':'cpu', 'w_bit':4, 'group_size':32} )
    print(model)
    gc.collect()
    torch.save(model, ckpt)

def run_model():
    if not os.path.exists(ckpt):
        quantize_model()
    model = torch.load(ckpt)
    _ = gc.collect()
    model.eval()
    model = model.to(torch.bfloat16)
    print(model)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    for n, m in model.named_modules():
        if isinstance(m, qlinear.QLinearPerGrp):
            print(f"Preparing weights of layer : {n}")
            m.device = "aie"
            m.quantize_weights()

    prompt = "Translate the following English sentence to French: 'Hello, how are you?'"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
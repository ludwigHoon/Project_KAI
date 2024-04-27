
import torch
import logging
import time
import argparse
import os
import psutil

from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig

model_name = "TheBloke/Mistral-7B-Instruct-v0.2-AWQ"
tokenizer = AutoTokenizer.from_pretrained(model_name)
quantization_config = GPTQConfig(bits=4, dataset = "c4", tokenizer=tokenizer)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", quantization_config=quantization_config)


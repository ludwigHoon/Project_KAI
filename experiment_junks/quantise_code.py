# Export to ONNX and quantise

import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
import os 

# https://huggingface.co/docs/optimum/onnxruntime/usage_guides/quantization


from optimum.onnxruntime import ORTQuantizer
from optimum.onnxruntime.configuration import AutoQuantizationConfig

import onnx 
import onnxruntime as ort
import numpy as np

import time 

import string
import random 


from optimum.exporters.onnx import main_export
from optimum.onnxruntime import ORTModelForCausalLM
from optimum.utils import NormalizedConfigManager
from optimum.exporters import TasksManager

model_id = "microsoft/Phi-3-mini-4k-instruct"

#model = AutoModelForCausalLM.from_pretrained(model_id)
#tokenizer = AutoTokenizer.from_pretrained(model_id)
#model.tokenizer = tokenizer

TasksManager._SUPPORTED_MODEL_TYPE["phi3"] = TasksManager._SUPPORTED_MODEL_TYPE["phi"]
NormalizedConfigManager._conf["phi3"] = NormalizedConfigManager._conf["phi"]


main_export(
    model_name_or_path=model_id,
    task="text-generation-with-past",
    no_post_process=True,
    output=f"./EXP_{model_id.replace('/','_')}",
)


quantizer = ORTQuantizer.from_pretrained(f"./EXP_{model_id.replace('/','_')}", file_name="model.onnx")

dqconfig = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False, use_symmetric_activations=True, 
                                                operators_to_quantize=["MatMul"],
                                                )
model_quantized_path = quantizer.quantize( save_dir=f"./EXP_Q_{model_id.replace('/','_')}", quantization_config=dqconfig )

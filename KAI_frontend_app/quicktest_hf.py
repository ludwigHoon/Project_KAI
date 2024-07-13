# Copyright (C) 2023 Advanced Micro Devices, Inc. All rights reserved.

import os
import numpy as np
import onnxruntime as ort
from pathlib import Path
from optimum.amd.ryzenai import RyzenAIModelForImageClassification
from transformers import ViTImageProcessor, ViTForImageClassification

model = "test_model.onnx"

path = r'voe-4.0-win_amd64'
providers = ['VitisAIExecutionProvider']
cache_dir = Path(__file__).parent.resolve()
provider_options = [{
            'config_file': os.path.join('..', path, 'vaip_config.json'),
            'cacheDir': str(cache_dir),
            'cacheKey': 'modelcachekey_quick'
        }]

print("ONX running ...")
quantized_model_path = "Xenova/facial_emotions_image_detection"
processor = ViTImageProcessor.from_pretrained(quantized_model_path)
model2 = ViTForImageClassification.from_pretrained(quantized_model_path)

model = RyzenAIModelForImageClassification.from_pretrained(quantized_model_path, vaip_config='vaip_config.json',provider='CPUExecutionProvider',file_name="onnx/model_quantized.onnx")
try:
    session = ort.InferenceSession(model2, providers=providers,
                               provider_options=provider_options)
except Exception as e:
    print(e)
    print("Test Failed")

def preprocess_random_image():
    image_array = np.random.rand(3, 32, 32).astype(np.float32)
    return np.expand_dims(image_array, axis=0)

# inference on random image data
input_data = preprocess_random_image()
try:
    outputs = session.run(None, {'input': input_data})
except Exception as e:
    print(e)
    print("Test Failed")
else:
    print("Test Passed")


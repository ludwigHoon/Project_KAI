# Source:https://huggingface.co/docs/optimum/v1.17.1/en/amd/ryzenai/overview

import os
from pathlib import Path
import numpy as np
import requests
from PIL import Image
from torchvision import transforms

# from optimum.amd.ryzenai import RyzenAIModelForImageClassification
from transformers import AutoFeatureExtractor, pipeline, ImageFeatureExtractionMixin


# url = "http://images.cocodataset.org/val2017/000000039769.jpg"
# url = "https://www.shutterstock.com/image-photo/studio-image-emotional-clueless-young-260nw-1887053947.jpg"
# image = Image.open(requests.get(url, stream=True).raw)


url = "./test_image/disgust.png"
image = Image.open(url).convert('RGB')

# Define the transformation
transform = transforms.Compose([
    transforms.ToTensor(),  # Convert the image to a tensor with shape (C, H, W) and values in range [0, 1]
])
# Apply the transformation
tensor = transform(image)
# Add a batch dimension
batch_tensor = tensor.unsqueeze(0) 

# Convert the tensor to float type
batch_tensor = batch_tensor.float()


# See [quantize.py](https://huggingface.co/mohitsha/transformers-resnet18-onnx-quantized-ryzen/blob/main/quantize.py) for more details on quantization.
# quantized_model_path = "mohitsha/transformers-resnet18-onnx-quantized-ryzen"
#from transformers import AutoImageProcessor, AutoModelForImageClassification

#processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
# model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")
quantized_model_path = "Xenova/facial_emotions_image_detection" 
# quantized_model_path = "amd/retinaface" 

# The path and name of the runtime configuration file. A default version of this runtime configuration
# file can be found in the Ryzen AI VOE package, extracted during installation under the name `vaip_config.json`.
vaip_config = ".\\vaip_config.json"
vaip_config =".\\voe-4.0-win_amd64\\vaip_config.json"
local_quantized_model_path = "./models/model_fp16.onnx"

#CPUExecutionProvider
#can work but not on Vitis AI executor, only Azure(cloud) or CPU execution providers
# model = RyzenAIModelForImageClassification.from_pretrained(quantized_model_path, vaip_config=vaip_config, provider='VitisAIExecutionProvider',file_name="onnx/model.onnx")
# model = RyzenAIModelForImageClassification.from_pretrained(quantized_model_path, vaip_config=vaip_config, provider='VitisAIExecutionProvider',file_name="weights/RetinaFace_int.onnx")
feature_extractor = AutoFeatureExtractor.from_pretrained(quantized_model_path)
featured_extracted = feature_extractor(batch_tensor)



print(feature_extractor)
# cls_pipe = pipeline("image-classification", model=model, feature_extractor=feature_extractor)
# outputs = cls_pipe(image)
# print(outputs)

# imgFE= ImageFeatureExtractionMixin()
# img_nd = imgFE.normalize(image=image,mean = feature_extractor.image_mean[0], std= feature_extractor.image_std[0] , rescale=feature_extractor.do_rescale)
# #===========================================================
# try to quantize lcoally using VitisAI
# import onnxruntime as ort
# cache_dir = Path(__file__).parent.resolve()
# providers = ['VitisAIExecutionProvider']
# provider_options = [{
#             'config_file': os.path.join('.', 'vaip_config.json'),
#             'cacheDir': str(cache_dir),
#             'cacheKey': 'modelcachekey_quick'
#         }]

# from onnxruntime.quantization import shape_inference

# shape_inference.quant_pre_process(
#     input_model_path= "./models/model_fp16.onnx",
#     output_model_path ="./models/model_fp16_quantized.onnx")
# session = ort.InferenceSession(local_quantized_model_path, providers=providers,
#                                provider_options=provider_options)

# outputs = session.run('temp.out', {'input': image})
import onnxruntime as ort
session = ort.InferenceSession(
    local_quantized_model_path,
    providers=["VitisAIExecutionProvider"],
    provider_options=[{"config_file":".\\voe-4.0-win_amd64\\vaip_config.json"}])

outputs = session.run(None, {'pixel_values': featured_extracted['pixel_values']})
translated_emotions = ["sad", "disgust", "angry", "neutral", "fear", "surprise", "happy"]
print([translated_emotions[np.argmin(a)] for a in outputs])
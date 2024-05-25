from optimum.onnxruntime import ORTModelForCausalLM
from optimum.utils import NormalizedConfigManager
from optimum.exporters import TasksManager
import os
import onnxruntime as ort
from transformers import AutoTokenizer

TasksManager._SUPPORTED_MODEL_TYPE["phi3"] = TasksManager._SUPPORTED_MODEL_TYPE["phi"]
NormalizedConfigManager._conf["phi3"] = NormalizedConfigManager._conf["phi"]

dev = os.getenv("DEVICE")
if dev == "stx":
    p = psutil.Process()
    p.cpu_affinity([0, 1, 2, 3])

provider = "VitisAIExecutionProvider"
provider_options = {'config_file': 'C:/Users/kai/Documents/GitHub/RyzenAI-SW/example/transformers/models/opt-onnx/vaip_config.json'}

sess_options = ort.SessionOptions()


#sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED

# Set Vitis AI as the execution provider
# Assuming 'VitisAIExecutionProvider' is the provider's name, adjust if necessary
#sess_options.execution_mode = ort.ExecutionMode.ORT_PARALLEL

# Create an InferenceSession with Vitis AI Execution Provider
#session = ort.InferenceSession("./EXP_QQ_microsoft_Phi-3-mini-4k-instruct/model_quantized.onnx", sess_options=sess_options, providers=[provider], provider_options=[provider_options])

provider2 = "CPUExecutionProvider"
provider_options2 = {} 
sess_options2 = ort.SessionOptions()
prompt = "How to build a house?"

model = ORTModelForCausalLM.from_pretrained("./EXP_Q_microsoft_Phi-3-mini-4k-instruct", provider=provider,use_cache=True, use_io_binding=False, session_options=sess_options, provider_options=provider_options)
tokenizer = AutoTokenizer.from_pretrained("./EXP_Q_microsoft_Phi-3-mini-4k-instruct")


model2 = ORTModelForCausalLM.from_pretrained("./EXP_Q_microsoft_Phi-3-mini-4k-instruct", provider=provider2,use_cache=True, use_io_binding=False, session_options=sess_options2, provider_options=provider_options2)
tokenizer2 = AutoTokenizer.from_pretrained("./EXP_Q_microsoft_Phi-3-mini-4k-instruct")



inputs = tokenizer(prompt, return_tensors="pt") 
generate_ids = model.generate(inputs.input_ids, max_length=30)
response = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(response)

input("WAIT ")

inputs = tokenizer2(prompt, return_tensors="pt") 
generate_ids = model2.generate(inputs.input_ids, max_length=30)
response = tokenizer2.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(response)

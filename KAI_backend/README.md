# Steps to reproduce
1. Setup RyzenAI, run this:
    ```
    git lfs install
    cd RyzenAI-SW\example\transformers\ext
    git clone https://huggingface.co/datasets/mit-han-lab/awq-model-zoo awq_cache
    ```
2. Edit the first line `setup_link.bat`: Replace `<Path to RyzenAI>` to the actual path of RyzenAI folder in line 1:`SET AMD_DIR=<Path to RyzenAI>\example\transformers`
3. Run `setup_link.bat` to setup symlink to ryzenAI's dependencies
4. Run the following:
    ```
    conda env create --file=env.yaml
    conda activate kai_be
    setup.bat
    pip install ops\cpp --force-reinstall
    ```
5. Start the background service with: `python -m uvicorn main:app` (available at: 127.0.0.1:8000)

Test codes:
```python
import requests

url = f"http://127.0.0.1:8000/chat/"
with requests.post(url, json = {"prompt": "What is AMD?"}, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk)

messages = [{"role": "system", "content": "You're a chatbot designed to run on AMD AI processor"},
    {"role":"user", "content": "What is AMD?"}]
with requests.post(url, json = {"prompt": messages}, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk)

```
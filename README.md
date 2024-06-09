# Project details
- To-do: Change embedding to this model: multi-qa-MiniLM-L6-cos-v1 (https://www.sbert.net/docs/pretrained_models.html) 
- https://weaviate.io/blog/cross-encoders-as-reranker <-- maybe implement reranker
- To-do: swap the pytorch and transformer to this: https://github.com/amd/RyzenAI-SW/blob/main/example/transformers/README.md

- Potentially-reusable:
    - https://github.com/raydelvecchio/vlite-v2/blob/master/vlite2/ingestors.py
    - https://github.com/weaviate/Verba  <--- reusing
    - https://www.sbert.net/examples/applications/computing-embeddings/README.html 
    - calendar stuff, haven't read too closely: https://www.nearform.com/insights/using-google-calendar-with-natural-language-via-langchain/
    - This can get email from outlook, asssume user signed in and stuff, I'd rather use this and not have to worry about syncing, syncing should be handled by outlook.
    ```python
    import win32com.client
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6) # "6" refers to the index of a folder - in this case,
                                        # the inbox. You can change that number to reference
                                        # any other folder
    messages = inbox.Items
    message = messages.GetLast()
    body_content = message.body
    print(body_content)
    ```
    - Potentially the same thing can be done for calendar stored in outlook, user can login with other email providers, should be platform-independent enough.
---

## Interesting resources:
- IDK how NPU work yet, but potentially split it between CPU and NPU: https://huggingface.co/blog/accelerate-large-models
- Unknown if the `from modeling_llama_amd import LlamaForCausalLM, LlamaAttention` are limited to LLAMA2 architecture, if not, other awq models may be used: https://huggingface.co/TheBloke?search_models=awq&sort_models=created#models
- If only the specific architecture and not all awq quantised models were supported, may have to quantise and convert to ONNX format with vitis quantisation tool: https://ryzenai.docs.amd.com/en/latest/vai_quant/vai_q_onnx.html but may have to check if the resulting models have incompatible operators, because not all were supported?!: https://ryzenai.docs.amd.com/en/latest/modelcompat.html
- https://onnxruntime.ai/docs/execution-providers/Vitis-AI-ExecutionProvider.html
- https://huggingface.co/docs/transformers/main/en/quantization?fuse=supported+architectures

#### Activeloop Deep Memory
RAG Database for AI? https://github.com/activeloopai/deeplake/tree/main
tutorial from langchain: https://python.langchain.com/docs/integrations/retrievers/activeloop
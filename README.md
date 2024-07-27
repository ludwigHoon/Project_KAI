# Project - AI HarmonyCare 
**AI HarmonyCare** is software that utilizes advanced AI models for facial expression recognition and email/calendar retrieval & summarization. It offers two main features:
1. Recommand break based on the real time user emotion via facial expression recognition
2. Interact with a LLM agent to get summary of interested latest emails and today calender events updates

With the **AMD Ryzen AI enabled PC**, the powerful CPU and NPU enable seamless parallel processing of frequent facial recognition tasks alongside the Llama 3 Large Language Model (LLM). This setup, combined with Retrieval-Augmented Generation (RAG) capabilities using a vector database like ChromaDB, ensures efficient and intelligent system performance

## 1.0 Setting up
Basic dependencies:
1. Git [[Get Git for Windows]](https://git-scm.com/download/win)
2. Anaconda [[Get Anaconda for windows]](https://docs.anaconda.com/anaconda/install/windows/) 

### 1.1 AMD Ryzen AI NPU driver setup
Follow the steps in the link for [[AMD Ryzen AI NPU driver installation steps]](https://ryzenai.docs.amd.com/en/latest/inst.html)

### 1.2 AMD Ryzen AI Software Platform Setup
1. Go to [[AMD Ryzen AI software Platform Github]](https://github.com/amd/RyzenAI-SW)
2. setup repository clone requirement.
3. Clone the repository using commands below:
```
git clone https://github.com/amd/RyzenAI-SW.git
```
4. Record down the cloned repository local directory needed in later section 1.3, sample directory <code>C:\AMD_setup_demo\RyzenAI-SW</code>

### 1.3 Getting AI HarmonyCare source code
1. Acquire permission access to [[AI HarmonyCare Github]](https://github.com/ludwigHoon/Project_KAI)
    - contact #1: ldwgkshoon@gmail.com
    - contact #2: yzc95127@gmail.com

2. Select a directory and clone the [[AI HarmonyCare Github Repository]](https://github.com/ludwigHoon/Project_KAI)
    ``` 
    git clone https://github.com/ludwigHoon/Project_KAI.git
    ```

3.  At the cloned repository, update the file <code>PROJECT_KAI\KAI_backend\setup_link.bat</code>, at line 1, replace the <code>\<Ryzen-SW local Directory\></code> to the directory in Section 1.2 Step 4
    ```
    SET AMD_DIR=<Ryzen-SW local Directory>\example\transformers
    ```
    Example:
    ```
    SET AMD_DIR=C:\github\RyzenAI-SW\example\transformers
    ```

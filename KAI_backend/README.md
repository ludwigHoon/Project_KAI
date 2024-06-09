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

@echo off
@REM ENV_NAME is conda enviroment name, it should be setup once and reuse in next run
@REM YAML_FILE is conda enviroment dependecies list
SET ENV_NAME=kai_be2
SET YAML_FILE=env.yaml

@REM Record starting DIR
pushd %~dp0

:: Check if the environment exists
call conda deactivate

:: create symbolic linking to RyzenAI-SW\example\transformers local cloned repository
:: you may require to setup the RyzenAI-SW enviroment
call ./KAI_backend/setup_link.bat

:: Check if the target environment exists
SET "ENV_EXIST="
for /f "delims=" %%a in ('conda env list ^| findstr /C:"%ENV_NAME%"') do (
    SET "ENV_EXIST=%%a"
)

IF "%ENV_EXIST%" == "" (
    :: Check if the script is running with administrator privileges
    @REM openfiles >nul 2>&1
    @REM if %errorlevel% neq 0 (
    @REM     :: Not running as administrator, so restart with elevated privileges
    @REM     echo Run this run.bat file in a administrator terminal to setup new conda enviroment!!
    @REM     echo try again! Exiting...
    @REM     EXIT /B
    @REM )
    cd KAI_backend
    echo Creating the environment from %YAML_FILE%
    call conda env create -f %YAML_FILE%
    echo Activating the new environment: %ENV_NAME%
    call conda activate %ENV_NAME%
    call setup.bat
    call pip install --force-reinstall huggingface-hub==0.23.4
    call pip install ops\cpp --force-reinstall
    cd ryzen-ai-sw-1.1
    call pip install vai_q_onnx-1.16.0+69bc4f2-py2.py3-none-any.whl
    call pip install onnxruntime
    cd voe-4.0-win_amd64
    pip install voe-0.1.0-cp39-cp39-win_amd64.whl
    pip install onnxruntime_vitisai-1.15.1-cp39-cp39-win_amd64.whl
    python installer.py
    cd ../../../
) else (
    echo Activating the existing environment: %ENV_NAME%
    call conda activate %ENV_NAME%
    call ./KAI_backend/setup.bat
)

cd ./KAI_backend
:: "ckpt" folder used to store Quantized model
mkdir ckpt
@REM python -m uvicorn main:app /b
@echo "Starting LLM backend..." 
start "LLM-service" call python -m uvicorn main:app --reload
cd ..
@echo "Starting Gradio Chatbot..." 
start "Gradio-Chat-service" call python app.py
@REM Reset back to starting dir
popd
pause
@echo "Exiting Services..." 
taskkill /fi "WindowTitle eq LLM-service"
taskkill /fi "WindowTitle eq Gradio-Chat-service"
exit

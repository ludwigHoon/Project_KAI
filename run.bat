@echo off
@REM ENV_NAME is conda enviroment name, it should be setup once and reuse in next run
@REM YAML_FILE is conda enviroment dependecies list
SET ENV_NAME=kai_be
SET YAML_FILE=env.yaml

@REM Record starting DIR
pushd %~dp0

:: Check if the environment exists
call conda deactivate

@REM create symbolic linking to RyzenAI-SW\example\transformers local cloned repository
@REM you may require to setup the RyzenAI-SW enviroment
call ./KAI_backend/setup_link.bat

:: Check if the target environment exists
SET "ENV_EXIST="
for /f "delims=" %%a in ('conda env list ^| findstr /C:"%ENV_NAME%"') do (
    SET "ENV_EXIST=%%a"
)

IF "%ENV_EXIST%" == "" (
    echo Creating the environment from %YAML_FILE%
    call conda env create -f %YAML_FILE%
    echo Activating the new environment: %ENV_NAME%
    call conda activate %ENV_NAME%
) else (
    echo Activating the existing environment: %ENV_NAME%
    call conda activate %ENV_NAME%
)

call ./KAI_backend/setup.bat

cd ./KAI_backend
mkdir ckpt
python -m uvicorn main:app

@REM Reset back to starting dir
popd

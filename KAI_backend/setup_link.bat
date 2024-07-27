SET AMD_DIR=C:\github\RyzenAI-SW\example\transformers
SET RYZENAI_SW_DIR=C:\Users\kai\Downloads\ryzen-ai-sw-1.1
SET PWD=%~dp0

mklink /D %PWD%ryzen-ai-sw-1.1 %RYZENAI_SW_DIR%
mklink /D %PWD%third_party %AMD_DIR%\third_party
mklink /D %PWD%ops %AMD_DIR%\ops
mklink /D %PWD%tools %AMD_DIR%\tools
mklink /D %PWD%onnx-ops %AMD_DIR%\onnx-ops
mklink /D %PWD%ext %AMD_DIR%\ext
mklink /D %PWD%dll %AMD_DIR%\dll
mklink /D %PWD%xclbin %AMD_DIR%\xclbin
SET AMD_DIR=C:\Users\kai\RyzenAI-SW\example\transformers
SET PWD=%~dp0

mklink /D %PWD%third_party %AMD_DIR%\third_party
mklink /D %PWD%ops %AMD_DIR%\ops
mklink /D %PWD%tools %AMD_DIR%\tools
mklink /D %PWD%onnx-ops %AMD_DIR%\onnx-ops
mklink /D %PWD%ext %AMD_DIR%\ext
mklink /D %PWD%dll %AMD_DIR%\dll
mklink /D %PWD%xclbin %AMD_DIR%\xclbin
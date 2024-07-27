@echo off
echo Please enter your RyzenAI SW Cloned repository's transformers directory: 
echo Note: Clone from github https://github.com/amd/RyzenAI-SW/tree/main/example/transformers
echo Note: The sample full transformers path is "C:\github\RyzenAI-SW\example\transformers"
set /p AMD_DIR=RyzenAI_transformers_dir: 
echo RyzenAI transformers directory set to %AMD_DIR%!
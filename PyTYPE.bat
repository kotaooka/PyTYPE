@echo off
where /q python
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b
)
if not exist PyTYPE.py (
    echo PyTYPE.py does not exist. Please check the file path and try again.
    exit /b
)
python PyTYPE.py

pause
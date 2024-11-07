@echo off

REM Check if a file argument is provided
if "%~1"=="" (
    echo Usage: %0 filename.syp
    exit /b 1
)

set input_file=%~1

REM Check if the file exists
if not exist "%input_file%" (
    echo File not found: %input_file%
    exit /b 1
)

REM Translate Syptonic
python Syptonic.py "%input_file%"

if NOT "%~2"=="-c" (
    REM Run the generated Python file
    python "%~dpn1.py"
)

if "%~2"=="-d" (
    REM Delete newly generated Python file
    del "%~dpn1.py"
)

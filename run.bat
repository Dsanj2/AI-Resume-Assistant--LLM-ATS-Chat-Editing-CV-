@echo off
REM ----------------------------
REM AI CV Generator Launcher
REM ----------------------------

REM Set paths
SET VENV_DIR=venv
SET OLLAMA_PORT=11434
SET APP_FILE=app.py

REM Activate virtual environment
IF EXIST "%VENV_DIR%\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%VENV_DIR%\Scripts\activate.bat"
) ELSE (
    echo Virtual environment not found! Please create it with:
    echo python -m venv venv
    exit /b
)

REM Check if Ollama server is running
netstat -ano | findstr :%OLLAMA_PORT% >nul
IF %ERRORLEVEL% NEQ 0 (
    echo Starting Ollama server on port %OLLAMA_PORT%...
    start "" "ollama" serve
    timeout /t 5 >nul
) ELSE (
    echo Ollama server already running on port %OLLAMA_PORT%.
)

REM Run Streamlit app
echo Starting Streamlit app...
streamlit run %APP_FILE%
pause

@echo off
:: The Dark Fantasy World - Startup Script
:: This batch file automatically starts the game.

@echo ========================================
@echo   THE DARK FANTASY WORLD
@echo ========================================
@echo.
@echo Starting the game...
@echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.6 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Navigate to the game directory and start the game
cd /d "%~dp0"
python main.py

:: Pause after the game ends (optional)
pause
